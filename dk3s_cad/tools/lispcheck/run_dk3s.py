#!/usr/bin/env python3
"""
run_dk3s.py — прогон dk3s_drawing.lsp через мини-интерпретатор AutoLISP без CAD.
Результат: DXF (можно открыть в nanoCAD) и PNG для визуальной проверки.

Использование:
    python3 tools/lispcheck/run_dk3s.py [--fail DIMENSION,DIMSTYLE] [--out dir]
--fail   имитировать отказ entmake для указанных типов (проверка запасных путей)
"""
import argparse
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolisp_mini import Interp, DxfBackend, LispError, sym  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lsp", default=os.path.join(os.path.dirname(__file__), "..", "..", "dk3s_drawing.lsp"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "out"))
    ap.add_argument("--fail", default="")
    ap.add_argument("--png-width", type=int, default=6000)
    ap.add_argument("--no-png", action="store_true")
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
    print("saved", dxf)
    if not args.no_png:
        png = os.path.join(args.out, "dk3s_preview.png")
        backend.render_png(png, width_px=args.png_width)
        print("saved", png)


if __name__ == "__main__":
    main()
