# -*- coding: utf-8 -*-
"""rebuild_iso_all.py — пересборка всего, что строится из 3D-модели датчика, одной командой, с проверками.

    python tools/rebuild_iso_all.py --out ПАПКА [--publish]

 1. FreeCAD: tools/iso/sensor_iso_fc.py -> ПАПКА/sensor_iso_cut.json, sensor_model.step
 2. раздел 11 LISP (изометрия): build_iso_lsp.py + update_iso_section.py
 3. dk3s_drawing.lsp из читаемого исходника (lisp_cyr_escape.py) + обратная проверка — должно совпасть байт в байт
 4. run_dk3s.py: лист (DXF, DWG, размеры строит ODA, превью 10000 px) и малое превью 2400 px
 5. check_text_fit.py по листу — обычный, строгий и «как в nanoCAD 5.1» (--nano), нарушений должно быть 0
 6. отдельный лист изометрии: build_sensor_iso_dxf.py -> размеры строит ODA -> DWG; проверка надписей
 7. --publish: в «Мой диск\\AutoCAD» — DWG изометрии, STEP, скрипты модели в _скрипты_изометрии (прежние файлы —
    в ПАПКА/backup), сверка хешей, галерея.
Останавливается на первой ошибке. Версию в шапке LISP, README и коммит делать руками.
Пути: FreeCAD — переменная FREECADCMD или %LOCALAPPDATA%\\Programs\\FreeCAD 1.1\\bin\\freecadcmd.exe;
ODA — как в run_dk3s.py (ODA_CONVERTER или Program Files\\ODA)."""
import argparse
import collections
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent            # dk3s_cad/tools
ROOT = HERE.parent                                # dk3s_cad
ISO, LC = HERE / "iso", HERE / "lispcheck"
AUTOCAD = Path(r"C:\Users\ldovg\Мой диск\AutoCAD")
SCRIPTS = ("sensor_model.py", "sensor_iso_fc.py", "build_sensor_iso_dxf.py", "sensor_labels.json")
ISO_DWG, STEP = "Датчик_ДК-3С_изометрия_вырез.dwg", "Датчик_ДК-3С.step"
PY = sys.executable
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
sys.path.insert(0, str(LC))
from run_dk3s import find_oda, oda_recompute  # noqa: E402

T0 = time.time()
REPORT = []


def step(msg):
    print("[%5.1f с] %s" % (time.time() - T0, msg), flush=True)


def fail(msg):
    print("ОШИБКА: " + msg, flush=True)
    sys.exit(1)


def run(cmd, cwd=ROOT, stdout_file=None):
    """Запуск с захватом вывода; код возврата != 0 — остановка."""
    cmd = [str(c) for c in cmd]
    if stdout_file is not None:
        with open(stdout_file, "wb") as f:
            r = subprocess.run(cmd, cwd=cwd, env=ENV, stdout=f, stderr=subprocess.PIPE)
        err = r.stderr.decode("utf-8", "replace")
        out = ""
    else:
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True)
        out, err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    if r.returncode != 0:
        fail("%s -> код %d\n%s\n%s" % (" ".join(cmd), r.returncode, out[-2000:], err[-2000:]))
    return out + err


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def text_fit(dxf):
    res = []
    for extra in ([], ["--margin", "-0.15"], ["--nano"]):     # --nano: как рисует nanoCAD 5.1 (26.09.2026)
        out = run([PY, LC / "check_text_fit.py", dxf] + extra)
        m = re.search(r"нарушений:\s*(\d+)", out)
        if not m:
            fail("check_text_fit: не нашёл итог\n" + out[-1500:])
        n = int(m.group(1))
        res.append(n)
        if n:
            fail("check_text_fit %s %s: нарушений %d\n%s" % (dxf, " ".join(extra), n, out[-3000:]))
    return res


def find_freecad():
    for c in (os.environ.get("FREECADCMD"),
              Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "FreeCAD 1.1" / "bin" / "freecadcmd.exe",
              shutil.which("freecadcmd")):
        if c and Path(c).is_file():
            return str(c)
    fail("freecadcmd не найден (задайте FREECADCMD)")


def dims_summary(dxf):
    """Размеры листа: сколько и что написано у повёрнутых (изометрия) — текст из блока, как его построил ODA."""
    import ezdxf
    doc = ezdxf.readfile(str(dxf))
    dims = list(doc.modelspace().query("DIMENSION"))
    iso = []
    for d in dims:
        ang = d.dxf.get("angle", 0.0)
        if abs(ang) > 0.01 and abs(ang - 90.0) > 0.01:
            blk = doc.blocks.get(d.dxf.get("geometry")) if d.dxf.get("geometry") else None
            txt = [e.plain_text() if e.dxftype() == "MTEXT" else e.dxf.text for e in (blk or []) if e.dxftype() in ("MTEXT", "TEXT")]
            iso.append("угол %.1f, наклон %.1f, измерено %.3f, на листе %s" % (
                ang, d.dxf.get("oblique_angle", 0.0), d.get_measurement(), txt))
    return len(dims), iso


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="папка для промежуточных файлов")
    ap.add_argument("--publish", action="store_true", help="разложить результат в «Мой диск\\AutoCAD» и обновить галерею")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    step("1. FreeCAD: модель, вырез, проекция")
    log = run([find_freecad(), ISO / "sensor_iso_fc.py", out])
    ok = [ln for ln in log.splitlines() if "SENSOR_ISO_OK" in ln]
    if not ok or not (out / "sensor_iso_cut.json").is_file():
        fail("FreeCAD не дал SENSOR_ISO_OK\n" + log[-3000:])
    REPORT.append("FreeCAD: " + ok[0][:160])

    step("2. раздел 11 LISP")
    REPORT.append(run([PY, ISO / "build_iso_lsp.py", out / "sensor_iso_cut.json", ISO / "sensor_labels.json",
                       out / "iso.lsp"]).strip())
    run([PY, ISO / "update_iso_section.py", out / "iso.lsp"])

    step("3. dk3s_drawing.lsp + обратная проверка")
    src = ROOT / "src" / "dk3s_drawing_readable.lsp"
    run([PY, HERE / "lisp_cyr_escape.py", src], stdout_file=ROOT / "dk3s_drawing.lsp")
    run([PY, HERE / "lisp_cyr_escape.py", "--decode", ROOT / "dk3s_drawing.lsp"], stdout_file=out / "roundtrip.lsp")
    if (out / "roundtrip.lsp").read_bytes() != src.read_bytes():
        fail("обратное преобразование LISP не совпало с исходником")
    REPORT.append("LISP: обратная проверка — идентично")

    step("4. лист: интерпретатор + ODA, превью 10000 и 2400")
    log = run([PY, LC / "run_dk3s.py", "--out", ROOT, "--png-width", "10000"])
    m = re.search(r"entities:\s*(\d+)", log)
    if not m or "recomputed by ODA" not in log:
        fail("run_dk3s: нет итога или размеры не пересчитаны ODA\n" + log[-2000:])
    REPORT.append("лист: entities %s, размеры построил ODA" % m.group(1))
    run([PY, LC / "run_dk3s.py", "--out", out / "small", "--png-width", "2400"])
    shutil.copy2(out / "small" / "dk3s_preview.png", ROOT / "dk3s_preview_small.png")

    step("5. проверка надписей листа")
    n = text_fit(ROOT / "dk3s_drawing.dxf")
    nd, iso = dims_summary(ROOT / "dk3s_drawing.dxf")
    REPORT.append("лист: нарушений %s; размеров %d" % (n, nd))
    REPORT.extend("  размер на изометрии: " + s for s in iso)

    step("6. отдельный лист изометрии: DXF -> размеры ODA -> DWG")
    REPORT.append(run([PY, ISO / "build_sensor_iso_dxf.py", out / "iso_sheet.dxf", out / "sensor_iso_cut.json",
                       ISO / "sensor_labels.json"]).strip().split("\n")[-1])
    oda = find_oda("auto")
    if not oda:
        fail("ODA File Converter не найден")
    dxf_oda, dwg_oda, tmp = oda_recompute(oda, str(out / "iso_sheet.dxf"))
    shutil.copy2(dxf_oda, out / "iso_sheet_oda.dxf")
    shutil.copy2(dwg_oda, out / ISO_DWG)
    shutil.rmtree(tmp, ignore_errors=True)
    import ezdxf
    ca = collections.Counter(e.dxftype() for e in ezdxf.readfile(str(out / "iso_sheet.dxf")).modelspace())
    cb = collections.Counter(e.dxftype() for e in ezdxf.readfile(str(out / "iso_sheet_oda.dxf")).modelspace())
    if ca != cb:
        fail("состав листа изометрии изменился в ODA: %s -> %s" % (dict(ca), dict(cb)))
    n2 = text_fit(out / "iso_sheet_oda.dxf")
    nd2, iso2 = dims_summary(out / "iso_sheet_oda.dxf")
    REPORT.append("лист изометрии: %s; нарушений %s" % (dict(cb), n2))
    REPORT.extend("  размер: " + s for s in iso2)

    if a.publish:
        step("7. в папку AutoCAD + галерея")
        bk = out / "backup"
        (bk / "_скрипты_изометрии").mkdir(parents=True, exist_ok=True)
        pairs = [(out / ISO_DWG, AUTOCAD / ISO_DWG), (out / "sensor_model.step", AUTOCAD / STEP)]
        pairs += [(ISO / s, AUTOCAD / "_скрипты_изометрии" / s) for s in SCRIPTS]
        for s, d in pairs:
            if d.exists():
                shutil.copy2(d, bk / d.relative_to(AUTOCAD))
            shutil.copy2(s, d)
            if sha(s) != sha(d):
                fail("хеш не совпал после копирования: " + str(d))
        REPORT.append("папка AutoCAD: %d файлов заменено, хеши совпали; прежние — в %s" % (len(pairs), bk))
        log = run([PY, "-X", "utf8", AUTOCAD / "_Обновить_галерею.py"], cwd=AUTOCAD)
        g = [ln for ln in log.splitlines() if ln.startswith("Готово")]
        if not g:
            fail("галерея: нет строки «Готово»\n" + log[-2000:])
        REPORT.append("галерея: " + g[0])

    step("готово")
    print("\n".join(["", "ИТОГ (%.0f с):" % (time.time() - T0)] + REPORT))


if __name__ == "__main__":
    main()
