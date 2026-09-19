# -*- coding: utf-8 -*-
"""update_iso_section.py iso_section.lsp — заменить раздел 11 (изометрия) в src/dk3s_drawing_readable.lsp
между метками ISO BEGIN / ISO END на свежесгенерированный build_iso_lsp.py.

Полный цикл обновления изометрии (из папки dk3s_cad):
    freecadcmd tools/iso/sensor_iso_fc.py ПАПКА            -> ПАПКА/sensor_iso_cut.json, sensor_model.step
    python tools/iso/build_iso_lsp.py ПАПКА/sensor_iso_cut.json tools/iso/sensor_labels.json ПАПКА/iso.lsp
    python tools/iso/update_iso_section.py ПАПКА/iso.lsp
    python tools/lisp_cyr_escape.py src/dk3s_drawing_readable.lsp > dk3s_drawing.lsp
    python tools/lispcheck/run_dk3s.py --out . --png-width 10000
"""
import sys
from pathlib import Path

CRLF = chr(13) + chr(10)
LF = chr(10)
BEGIN = ";;; === ISO BEGIN (раздел генерируется tools/iso/build_iso_lsp.py) ==="
END = ";;; === ISO END ==="

src = Path(__file__).resolve().parents[2] / "src" / "dk3s_drawing_readable.lsp"
s = src.read_bytes().decode("utf-8").replace(CRLF, LF)
iso = Path(sys.argv[1]).read_bytes().decode("utf-8").replace(CRLF, LF).rstrip(LF)
i, j = s.index(BEGIN), s.index(END)
s = s[:i] + BEGIN + LF + iso + LF + s[j:]
src.write_bytes(s.replace(LF, CRLF).encode("utf-8"))
print("раздел изометрии обновлён:", src)
