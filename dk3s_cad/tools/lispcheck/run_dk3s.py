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


# Шрифт, которым nanoCAD 5.1 рисует стиль GOST.shx: своего GOST.shx у него нет, берёт запасной FONTALT =
# CS_Gost2304.shx (ProgramData\Nanosoft\nanoCAD 5.1\SHX). Длины строк по его глифам сверены со снимком экрана
# Леонида 26.09.2026 — расхождение около 2 %.
SHX_GLOB = os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"), "Nanosoft", "nanoCAD*", "SHX",
                        "CS_Gost2304.shx")


def text_measure():
    """Функция длины строки (текст, высота, сжатие) -> мм и доля нижнего выноса от высоты.
    CS_Gost2304.shx, если найден; иначе — шрифт ezdxf по умолчанию (приблизительно)."""
    found = sorted(glob.glob(SHX_GLOB))
    if found:
        from ezdxf.fonts import shapefile
        shx = shapefile.readfile(found[-1])
        gc = shapefile.GlyphCache(shx)
        return (lambda t, h, w: gc.get_text_length(t, h, w)), shx.descender / shx.cap_height, found[-1]
    from ezdxf.fonts import fonts
    return (lambda t, h, w: fonts.make_font("txt.shx", h, w).text_width(t)), 0.3, "шрифт ezdxf по умолчанию"


def fix_text_insert(msp):
    """Точка вставки (10) выровненного TEXT — начало строки на базовой линии, как её считает CAD.
    Интерпретатор и ezdxf пишут в 10 ту же точку, что в 11 (точку выравнивания). AutoCAD и ezdxf сами пересчитывают
    по 11, а nanoCAD 5.1 рисует строку от 10: центрированные надписи уезжали вправо на полстроки (26.09.2026).
    Возвращает (исправлено надписей, чем меряли)."""
    import math
    measure, desc, src = text_measure()
    n = 0
    for e in msp.query("TEXT"):
        h, v = e.dxf.get("halign", 0), e.dxf.get("valign", 0)
        if (h == 0 and v == 0) or h in (3, 5) or not e.dxf.hasattr("align_point"):
            continue
        a = e.dxf.align_point
        if (e.dxf.insert - a).magnitude > 1e-6:      # точку 10 уже посчитал CAD — не трогать
            continue
        hh, wf = e.dxf.height, e.dxf.get("width", 1.0)
        w = measure(e.plain_text(), hh, wf)
        dx = {0: 0.0, 1: -w / 2.0, 2: -w, 4: -w / 2.0}.get(h, 0.0)
        dy = -hh / 2.0 if h == 4 else {0: 0.0, 1: desc * hh, 2: -hh / 2.0, 3: -hh}.get(v, 0.0)
        r = math.radians(e.dxf.get("rotation", 0.0))
        e.dxf.insert = (a[0] + dx * math.cos(r) - dy * math.sin(r), a[1] + dx * math.sin(r) + dy * math.cos(r), a[2])
        n += 1
    return n, src


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
    fix_text_insert(doc.modelspace())
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
