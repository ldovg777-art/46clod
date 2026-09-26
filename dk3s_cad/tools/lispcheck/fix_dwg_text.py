# -*- coding: utf-8 -*-
"""python tools/lispcheck/fix_dwg_text.py ФАЙЛ.dwg [...] [--check-only] — надписи на месте в nanoCAD 5.1 для готовых DWG.
DWG -> DXF (ODA) -> fix_text_insert (точка 10 выровненных надписей по CS_Gost2304.shx; надписи, у которых CAD уже
посчитал точку 10, не трогает) -> DWG 2013 (ODA). Проверки: check_text_fit --nano до и после, состав примитивов
и тексты те же, версия AC1027. Файл заменяется только если всё сошлось и нарушений стало не больше."""
import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile

LC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LC)
import ezdxf  # noqa: E402
from run_dk3s import find_oda, fix_text_insert  # noqa: E402

ODA = find_oda("auto")


def oda(src_dir, dst_dir, fmt, flt):
    subprocess.run([ODA, src_dir, dst_dir, "ACAD2013", fmt, "0", "1", flt], check=True, timeout=600)


def nano_check(dxf):
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(LC, "check_text_fit.py"), dxf, "--nano"],
                       capture_output=True, text=True, encoding="utf-8")
    m = re.search(r"нарушений:\s*(\d+)", r.stdout)
    return int(m.group(1)) if m else -1, r.stdout


def sig(doc):
    msp = doc.modelspace()
    return (dict(collections.Counter(e.dxftype() for e in msp)),
            sorted(e.dxf.text for e in msp.query("TEXT")), sorted(e.text for e in msp.query("MTEXT")))


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check-only" in sys.argv
    tmp = tempfile.mkdtemp(prefix="fixtxt_")
    d_in, d_dxf, d_fix, d_dwg, d_back = (os.path.join(tmp, n) for n in ("in", "dxf", "fix", "dwg", "back"))
    for d in (d_in, d_dxf, d_fix, d_dwg, d_back):
        os.makedirs(d)
    for i, f in enumerate(files):
        shutil.copy2(f, os.path.join(d_in, f"d{i:02d}.dwg"))
    oda(d_in, d_dxf, "DXF", "*.DWG")
    for i, f in enumerate(files):
        doc = ezdxf.readfile(os.path.join(d_dxf, f"d{i:02d}.dxf"))
        n, src = fix_text_insert(doc.modelspace())
        doc.saveas(os.path.join(d_fix, f"d{i:02d}.dxf"))
    oda(d_fix, d_dwg, "DWG", "*.DXF")
    oda(d_dwg, d_back, "DXF", "*.DWG")
    for i, f in enumerate(files):
        before, _ = nano_check(os.path.join(d_dxf, f"d{i:02d}.dxf"))
        after, rep = nano_check(os.path.join(d_back, f"d{i:02d}.dxf"))
        a = ezdxf.readfile(os.path.join(d_dxf, f"d{i:02d}.dxf"))
        b = ezdxf.readfile(os.path.join(d_back, f"d{i:02d}.dxf"))
        same = sig(a) == sig(b)
        new = os.path.join(d_dwg, f"d{i:02d}.dwg")
        ver = open(new, "rb").read(6).decode()
        moved = sum(1 for e in b.modelspace().query("TEXT") if (e.dxf.get("halign", 0) or e.dxf.get("valign", 0))
                    and e.dxf.hasattr("align_point") and (e.dxf.insert - e.dxf.align_point).magnitude > 1e-6)
        ok = same and ver == "AC1027" and 0 <= after <= max(before, 0)
        print(f"{'ЗАМЕНЁН' if ok and not check_only else ('проверен' if ok else 'НЕ заменён')}: {f}\n"
              f"   nanoCAD-нарушений: было {before}, стало {after}; состав тот же: {same}; версия {ver}; "
              f"выровненных надписей с точкой 10: {moved}")
        if after:
            print("   " + "\n   ".join(rep.strip().splitlines()[2:8]))
        if ok and not check_only:
            shutil.copy2(new, f)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
