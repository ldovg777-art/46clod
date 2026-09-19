# -*- coding: utf-8 -*-
"""build_sensor_iso_dxf.py ВЫХОД.dxf sensor_iso_cut.json — DXF приведённой изометрии датчика ДК-3С-210АВ
с вырезом четверти. Проекция FreeCAD (projectEx из (-1,-1,1)) повёрнута на +60°: ось датчика идёт вверх
вправо под 30°, плоскость мостиков и электродов сравнения — вертикальна. Масштаб 1:2."""
import json
import math
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

d = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "sensor_iso_cut.json", encoding="utf-8"))
E = d["edges"]
K = 1.0 / math.sqrt(2.0 / 3.0)       # ГОСТ 2.317: приведённая изометрия (коэффициент 1)
S = 0.5                              # масштаб изображения 1:2
A = math.radians(60.0)               # поворот картинки: ось Z модели — вертикаль листа
ca, sa = math.cos(A), math.sin(A)
rot = lambda p: (p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca)
vis = [pl for n in ("hard", "outline") for pl in E[n]]
pts = [rot(p) for pl in vis for p in pl]
x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
MARGIN_X, MARGIN_Y = 10.0, 30.0


def T(p):
    q = rot(p)
    return ((q[0] - x0) * K * S + MARGIN_X, (q[1] - y0) * K * S + MARGIN_Y)


doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.MM
doc.layers.add("ISO_CONTOUR", color=7, lineweight=50)
doc.layers.add("ISO_HATCH", color=7, lineweight=18)
doc.layers.add("ISO_AXIS", color=7, lineweight=18, linetype="CENTER")
doc.layers.add("ISO_TEXT", color=7, lineweight=25)
st = doc.styles.add("GOST", font="GOST.shx")
st.dxf.oblique = 15.0
msp = doc.modelspace()
for pl in vis:
    msp.add_lwpolyline([T(p) for p in pl], dxfattribs={"layer": "ISO_CONTOUR"})
nh = 0
for key, segs in E["hatch"].items():
    for a, b in segs:
        msp.add_line(T(a), T(b), dxfattribs={"layer": "ISO_HATCH"})
        nh += 1
a, b = E["axis"][0]
msp.add_line(T(a), T(b), dxfattribs={"layer": "ISO_AXIS", "ltscale": 0.5})

# --- выноски с полками: точка на детали (модель, мм) -> излом на листе -> полка и надпись над ней
o, Mx = d["map"]["O"], d["map"]["M"]


def T3(x, y, z):
    return T((o[0] + Mx[0][0] * x + Mx[0][1] * y + Mx[0][2] * z, o[1] + Mx[1][0] * x + Mx[1][1] * y + Mx[1][2] * z))


H = 3.5                               # высота надписей выносок, мм листа
NARROW = set(".,:;!'\"()-Iil1")


def text_w(s):
    """Ширина по ГОСТ 2.304 тип Б с запасом, как dk3s_text_w в LISP."""
    w = 0.0
    for c in s:
        w += 0.8 if (c.isupper()) else 0.6 if c == " " else 0.45 if c in NARROW else 0.7
    return (w + 0.27) * H * 1.08


def leader(p3, knee, txt, sgn):
    pt = T3(*p3)
    g = 0.3 * H
    w = text_w(txt)
    end = (knee[0] + sgn * (w + g), knee[1])
    msp.add_lwpolyline([(pt[0] - 0.35, pt[1], 0.7, 0.7, 1.0), (pt[0] + 0.35, pt[1], 0.7, 0.7, 1.0)],
                       format="xyseb", close=True, dxfattribs={"layer": "ISO_TEXT"})   # точка на детали
    msp.add_line(pt, knee, dxfattribs={"layer": "ISO_TEXT"})
    msp.add_line(knee, end, dxfattribs={"layer": "ISO_TEXT"})
    t = msp.add_text(txt, height=H, dxfattribs={"layer": "ISO_TEXT", "style": "GOST"})
    if sgn > 0:
        t.set_placement((knee[0] + g, knee[1] + 0.25 * H), align=TA.LEFT)
    else:
        t.set_placement((knee[0] - g, knee[1] + 0.25 * H), align=TA.BOTTOM_RIGHT)


LABELS = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else []
for lab in LABELS:
    leader(tuple(lab["p"]), tuple(lab["knee"]), lab["text"], lab["dir"])

w = (max(p[0] for p in pts) - x0) * K * S
h = (max(p[1] for p in pts) - y0) * K * S
t = msp.add_text("Датчик концентрации ДК-3С-210АВ. Изометрия с вырезом (1:2)", height=5.0,
                 dxfattribs={"layer": "ISO_TEXT", "style": "GOST"})
t.set_placement((MARGIN_X, 16.0), align=TA.LEFT)
notes = ["Приведённая изометрия по ГОСТ 2.317. Вырезана четверть гильзы, корпуса, грундбуксы, гайки нажимной,",
         "фторопластовой втулки и шайбы; трубки, наконечник, скоба и токоотвод ВЭ не рассечены (ГОСТ 2.305).",
         "Шайба пружинная 20 65Г ГОСТ 6402-70 (гровер) стопорит гайку и упруго поджимает втулку: при остывании",
         "фторопласт сжимается, а натяг и герметичность сохраняются. В чертежах ЭКОР её нет — ставится по факту.",
         "Втулка — по чертежу 715412.001 (3 канала Ø6 на Ø11), мостики — трубки Ø6 (техописание K1, лист 16).",
         "Условно (разреза датчика в документации нет): стенка гильзы 2 мм, путь трубки РЭ и концы мостиков в гильзе."]
for i, s in enumerate(notes):
    t2 = msp.add_text(s, height=3.0, dxfattribs={"layer": "ISO_TEXT", "style": "GOST"})
    t2.set_placement((MARGIN_X, 10.0 - 4.5 * i), align=TA.LEFT)
# граница поля чертежа (тонкая рамка вокруг изображения и надписей)
from ezdxf import bbox as _bbox  # noqa: E402
ext = _bbox.extents(msp)                   # точный габарит (с надписями)
fx0, fy0, fx1, fy1 = ext.extmin.x - 6.0, ext.extmin.y - 6.0, ext.extmax.x + 6.0, ext.extmax.y + 6.0
doc.layers.add("ISO_FRAME", color=7, lineweight=35)
msp.add_lwpolyline([(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)], close=True, dxfattribs={"layer": "ISO_FRAME"})
doc.saveas(sys.argv[1])
print(f"saved {sys.argv[1]}: {len(vis)} contour polylines, {nh} hatch lines, picture {w:.1f} x {h:.1f} mm")
