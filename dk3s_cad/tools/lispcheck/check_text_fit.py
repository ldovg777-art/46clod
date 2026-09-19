# -*- coding: utf-8 -*-
"""Проверка надписей чертежа (DXF) на выход за графы и рамку, наложения и пересечения линиями.

Ширина надписи оценивается с запасом по пропорциям шрифта ГОСТ 2.304 тип Б (так же, как dk3s_text_w
в LISP): прописная 0,8h, строчная и цифра 0,7h, пробел 0,6h, узкие знаки 0,45h, знак номера 1,0h,
плюс вынос наклона 15 градусов 0,27h; всё умножается на коэффициент ширины надписи (группа 41).
Проверяются TEXT пространства модели против LINE, LWPOLYLINE, ARC, CIRCLE и других TEXT.
Размеры (DIMENSION) не проверяются — их текст размещает CAD.

    python check_text_fit.py чертёж.dxf [--margin 0.1] [--list]
Код возврата 0 — нарушений нет, 1 — есть (список печатается).
"""
import argparse
import math
import sys

import ezdxf

NARROW = set(".,:;!'\"()-Iil")
FONT_K = 1.08          # запас по ширине, как g_dk3s_font_k в LISP


def char_w(c):
    if c == "№":
        return 1.0
    if ("A" <= c <= "Z") or ("А" <= c <= "Я") or c == "Ё":
        return 0.8
    if c == " ":
        return 0.6
    if c in NARROW:
        return 0.45
    return 0.7


def text_box(t, margin):
    """Прямоугольник надписи: 4 угла в координатах модели (сжат на margin*h внутрь)."""
    s = t.dxf.text
    h = t.dxf.height
    wf = t.dxf.get("width", 1.0)
    w = h * (sum(char_w(c) for c in s) + 0.27) * wf * FONT_K
    hj, vj = t.dxf.get("halign", 0), t.dxf.get("valign", 0)
    x0 = {0: 0.0, 1: -w / 2.0, 2: -w, 4: -w / 2.0}.get(hj, 0.0)
    y0 = {0: 0.0, 1: 0.0, 2: -h / 2.0, 3: -h}.get(vj, 0.0)
    m = margin * h
    mb = m if m > 0 else 0.1 * h          # снизу не расширяем: там полка и своя выноска
    loc = [(x0 + m, y0 + mb), (x0 + w - m, y0 + mb), (x0 + w - m, y0 + h - m), (x0 + m, y0 + h - m)]
    p = t.dxf.align_point if (hj or vj) and t.dxf.hasattr("align_point") else t.dxf.insert
    a = math.radians(t.dxf.get("rotation", 0.0))
    ca, sa = math.cos(a), math.sin(a)
    return [(p.x + x * ca - y * sa, p.y + x * sa + y * ca) for x, y in loc]


def seg_cross(p1, p2, q1, q2):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(q1, q2, p1), orient(q1, q2, p2)
    d3, d4 = orient(p1, p2, q1), orient(p1, p2, q2)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def box_hit_seg(box, a, b):
    if inside(a, box) or inside(b, box):
        return True
    return any(seg_cross(box[i], box[(i + 1) % 4], a, b) for i in range(4))


def boxes_overlap(b1, b2):
    if any(inside(p, b2) for p in b1) or any(inside(p, b1) for p in b2):
        return True
    return any(seg_cross(b1[i], b1[(i + 1) % 4], b2[j], b2[(j + 1) % 4]) for i in range(4) for j in range(4))


def segments(msp):
    """Все отрезки модели (дуги и окружности — ломаной), с описанием источника."""
    out = []
    for e in msp:
        t = e.dxftype()
        if t == "LINE":
            out.append(((e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y), f"LINE {e.dxf.layer}"))
        elif t == "LWPOLYLINE":
            pts = [(p[0], p[1]) for p in e.get_points("xy")]
            if e.closed:
                pts.append(pts[0])
            w = e.dxf.get("const_width", 0.0)
            if len(pts) == 3 and w > 0 and e.closed:      # закрашенная точка выноски
                continue
            for a, b in zip(pts, pts[1:]):
                out.append((a, b, f"LWPOLYLINE {e.dxf.layer}"))
        elif t in ("ARC", "CIRCLE"):
            c, r = e.dxf.center, e.dxf.radius
            a1, a2 = (math.radians(e.dxf.start_angle), math.radians(e.dxf.end_angle)) if t == "ARC" else (0.0, 2 * math.pi)
            if a2 <= a1:
                a2 += 2 * math.pi
            n = max(8, int((a2 - a1) / (math.pi / 36)))
            pts = [(c.x + r * math.cos(a1 + (a2 - a1) * i / n), c.y + r * math.sin(a1 + (a2 - a1) * i / n)) for i in range(n + 1)]
            for a, b in zip(pts, pts[1:]):
                out.append((a, b, f"{t} {e.dxf.layer}"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dxf")
    ap.add_argument("--margin", type=float, default=0.1, help="сжатие прямоугольника надписи внутрь, доля h; отрицательное — запас наружу (кроме низа)")
    ap.add_argument("--list", action="store_true", help="напечатать все надписи с оценкой ширины")
    a = ap.parse_args()
    doc = ezdxf.readfile(a.dxf)
    msp = doc.modelspace()
    texts = [t for t in msp.query("TEXT") if t.dxf.text.strip()]
    boxes = [(t, text_box(t, a.margin)) for t in texts]
    segs = segments(msp)
    bad = []
    for t, b in boxes:
        xs, ys = [p[0] for p in b], [p[1] for p in b]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        for p, q, src in segs:
            if max(p[0], q[0]) < bx0 or min(p[0], q[0]) > bx1 or max(p[1], q[1]) < by0 or min(p[1], q[1]) > by1:
                continue
            if box_hit_seg(b, p, q):
                bad.append(f"пересечение: «{t.dxf.text}» ({t.dxf.insert.x:.0f},{t.dxf.insert.y:.0f}) и {src} "
                           f"({p[0]:.0f},{p[1]:.0f})-({q[0]:.0f},{q[1]:.0f})")
                break
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes_overlap(boxes[i][1], boxes[j][1]):
                bad.append(f"наложение надписей: «{boxes[i][0].dxf.text}» и «{boxes[j][0].dxf.text}»")
    if a.list:
        for t, b in boxes:
            xs = [p[0] for p in b]
            print(f"  «{t.dxf.text}» h={t.dxf.height:g} wf={t.dxf.get('width', 1.0):.2f} ширина~{max(xs)-min(xs):.1f}")
    print(f"надписей: {len(texts)}, отрезков: {len(segs)}, нарушений: {len(bad)}")
    for s in bad:
        print("  " + s)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
