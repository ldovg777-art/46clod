#!/usr/bin/env python3
"""
run_dk3s.py — прогон dk3s_drawing.lsp через мини-интерпретатор AutoLISP без CAD.
Результат: DXF (можно открыть в nanoCAD) и PNG для визуальной проверки.

Использование:
    python3 tools/lispcheck/run_dk3s.py [--fail DIMENSION,DIMSTYLE] [--out dir] [--oda auto|off|путь]
--fail   имитировать отказ entmake для указанных типов (проверка запасных путей)
--oda    размеры пересчитывает ODA File Converter — движок, на котором построен nanoCAD
         (по умолчанию auto: если установлен). Интерпретатор рисует размеры средствами ezdxf,
         а они ставят числа не так, как nanoCAD (вертикальные — справа от линии, невлезающие —
         по центру); ODA ставит их как CAD. Тогда DXF и PNG — с размерами ODA, плюс DWG.
"""
import argparse
import glob
import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolisp_mini import Interp, DxfBackend, LispError, sym  # noqa: E402


def find_oda(arg):
    """Путь к ODAFileConverter.exe или None."""
    if arg == "off":
        return None
    if arg and arg != "auto":
        return arg if os.path.isfile(arg) else None
    env = os.environ.get("ODA_CONVERTER")
    if env and os.path.isfile(env):
        return env
    found = sorted(glob.glob(os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"),
                                          "ODA", "ODAFileConverter*", "ODAFileConverter.exe")))
    return found[-1] if found else None


def oda_recompute(oda, dxf_path):
    """Блоки размеров убираются, ODA строит их заново (DXF -> DWG с аудитом -> DXF).
    Заданное положение числа (флаг 128, группа 11) сохраняется. Возвращает (dxf, dwg, временная папка)."""
    import ezdxf
    tmp = tempfile.mkdtemp(prefix="dk3s_oda_")
    src, mid, back = (os.path.join(tmp, n) for n in ("in", "dwg", "back"))
    for d in (src, mid, back):
        os.makedirs(d)
    doc = ezdxf.readfile(dxf_path)
    names = []
    for dim in doc.modelspace().query("DIMENSION"):
        names.append(dim.dxf.get("geometry"))
        dim.dxf.discard("geometry")
        if not dim.dxf.get("dimtype", 0) & 128:
            dim.dxf.discard("text_midpoint")
    for n in names:
        if n and n in doc.blocks:
            doc.blocks.delete_block(n, safe=False)
    doc.saveas(os.path.join(src, "dk3s_drawing.dxf"))
    for a, b, fmt, flt in ((src, mid, "DWG", "*.DXF"), (mid, back, "DXF", "*.DWG")):
        # ACAD2013 (AC1027): nanoCAD 5.1 не открывает DWG 2018 (опыт 26.09.2026), чертежи Андрея — тоже 2013
        subprocess.run([oda, a, b, "ACAD2013", fmt, "0", "1", flt], check=True, timeout=300)
    dxf, dwg = os.path.join(back, "dk3s_drawing.dxf"), os.path.join(mid, "dk3s_drawing.dwg")
    if not (os.path.isfile(dxf) and os.path.isfile(dwg)):
        raise RuntimeError("ODA не создал файлы в " + tmp)
    return dxf, dwg, tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lsp", default=os.path.join(os.path.dirname(__file__), "..", "..", "dk3s_drawing.lsp"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "out"))
    ap.add_argument("--fail", default="")
    ap.add_argument("--png-width", type=int, default=6000)
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--oda", default="auto", help="auto | off | путь к ODAFileConverter.exe")
    args = ap.parse_args()

    fail = [t for t in args.fail.split(",") if t]
    backend = DxfBackend(fail_types=fail)
    log = io.StringIO()
    interp = Interp(backend, out=log)
    src = open(args.lsp, encoding="utf-8").read()
    try:
        interp.run(src)
        interp.eval_top([sym("C:DK3S")])
    except LispError as e:
        print("LISP ERROR:", e)
        print(log.getvalue())
        sys.exit(1)
    print("LISP output:", log.getvalue().strip())
    print("entities:", backend.counts)
    if backend.unsupported:
        print("unsupported:", sorted(set(backend.unsupported)))
    print("commands:", [c[0] for c in interp.command_log])
    os.makedirs(args.out, exist_ok=True)
    dxf = os.path.join(args.out, "dk3s_drawing.dxf")
    backend.save(dxf)
    oda = find_oda(args.oda)
    if oda:
        import ezdxf
        oda_dxf, oda_dwg, tmp = oda_recompute(oda, dxf)
        shutil.copyfile(oda_dxf, dxf)
        shutil.copyfile(oda_dwg, os.path.join(args.out, "dk3s_drawing.dwg"))
        shutil.rmtree(tmp, ignore_errors=True)
        backend.doc = ezdxf.readfile(dxf)            # PNG — с размерами, построенными ODA
        backend.msp = backend.doc.modelspace()
        print("dimensions: recomputed by ODA File Converter (" + oda + "), DWG saved")
    else:
        print("dimensions: ezdxf rendering (ODA File Converter not found) — "
              "positions of dimension texts may differ from nanoCAD")
    print("saved", dxf)
    if not args.no_png:
        png = os.path.join(args.out, "dk3s_preview.png")
        from ezdxf import bbox                       # границы — по габариту листа (А3, А2 ...), с полем 10
        e = bbox.extents(backend.msp, fast=True)
        backend.render_png(png, width_px=args.png_width, xlim=(e.extmin.x - 10, e.extmax.x + 10),
                           ylim=(e.extmin.y - 10, e.extmax.y + 10))
        print("saved", png)


if __name__ == "__main__":
    main()
