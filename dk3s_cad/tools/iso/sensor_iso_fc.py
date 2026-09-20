# -*- coding: utf-8 -*-
"""freecadcmd sensor_iso_fc.py [папка] — изометрия датчика ДК-3С-210АВ с вырезом четверти (модель sensor_model).

Вырезается четверть корпусных деталей, обращённая к зрителю (взгляд из (-1,-1,1): область y<0, z>0) —
гильза, корпус, грундбукса, гайка, фторопластовая втулка. Трубки, мостики, скоба, наконечник, провод —
не рассекаются (ГОСТ 2.305). Штриховка разрезов по ГОСТ 2.317 (плоскость y=0 — диагональ (1,0,1),
z=0 — диагональ (1,-1,0)); металл — одинарная, смежные детали — разным шагом и сдвигом; фторопласт —
«в клетку» (ГОСТ 2.306). Выход: sensor_iso_cut.json (рёбра, штриховка, ось), sensor_model.step."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = sys.argv[-1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[-1]) else HERE

import FreeCAD as App  # noqa: E402
import Part  # noqa: E402
import TechDraw  # noqa: E402
import sensor_model as m  # noqa: E402

V = App.Vector
direction = V(-1, -1, 1)
NAMES = ["hard", "smooth", "seam", "outline", "iso", "hard_h", "smooth_h", "seam_h", "outline_h", "iso_h"]

P = m.build()
Part.makeCompound(list(P.values())).exportStep(os.path.join(OUT, "sensor_model.step"))


def pair(a, b):
    r = TechDraw.projectEx(Part.makeLine(a, b), direction)
    vs = [v for c in r if c is not None and not c.isNull() for v in c.Vertexes]
    return (vs[0].X, vs[0].Y), (vs[1].X, vs[1].Y)


o, ex = pair(V(0, 0, 0), V(10, 0, 0))
_, ey = pair(V(0, 0, 0), V(0, 10, 0))
_, ez = pair(V(0, 0, 0), V(0, 0, 10))
M = [[(ex[0] - o[0]) / 10, (ey[0] - o[0]) / 10, (ez[0] - o[0]) / 10],
     [(ex[1] - o[1]) / 10, (ey[1] - o[1]) / 10, (ez[1] - o[1]) / 10]]


def Pj(p):
    return [round(o[0] + M[0][0] * p.x + M[0][1] * p.y + M[0][2] * p.z, 5),
            round(o[1] + M[1][0] * p.x + M[1][1] * p.y + M[1][2] * p.z, 5)]


def project(shape):
    out = {}
    for name, comp in zip(NAMES, TechDraw.projectEx(shape, direction)):
        polys = []
        if comp is not None and not comp.isNull():
            for edge in comp.Edges:
                n = max(2, int(edge.Length / 0.25) + 1)
                polys.append([[round(q.x, 4), round(q.y, 4)] for q in edge.discretize(n)])
        out[name] = polys
    return out


def cut_faces(solid):
    res = []
    for f in solid.Faces:
        if f.Surface.TypeId != "Part::GeomPlane":
            continue
        n = f.normalAt(0, 0)
        c = f.CenterOfMass
        if abs(abs(n.z) - 1) < 1e-6 and abs(c.z) < 1e-6 and c.y < 0:
            res.append(("xy", f))
        elif abs(abs(n.y) - 1) < 1e-6 and abs(c.y) < 1e-6 and c.z > 0:
            res.append(("xz", f))
    return res


def hatch(face, plane, pitch, shift=0.0, cross=False):
    dirs = [V(1, -1, 0) if plane == "xy" else V(1, 0, 1)]
    if cross:
        dirs.append(V(1, 1, 0) if plane == "xy" else V(1, 0, -1))
    segs = []
    bb = face.BoundBox
    for d in dirs:
        d = V(d)
        d.normalize()
        step = pitch * math.sqrt(2)
        span = max(bb.XLength, bb.YLength, bb.ZLength) + 5.0
        x = bb.XMin - span + shift * step
        while x < bb.XMax + span:
            base = V(x, 0, 0)
            com = face.common(Part.makeLine(base - d * (span * 2), base + d * (span * 2)))
            for ed in com.Edges:
                segs.append([Pj(ed.Vertexes[0].Point), Pj(ed.Vertexes[-1].Point)])
            x += step
    return segs


# вырез четверти корпусных деталей
R = 40.0
box = Part.makeBox(m.X_CUT1 - m.X_CUT0, R, R, V(m.X_CUT0, -R, 0.0))
HATCH = {"sleeve": (1.4, 0.0, False), "body": (3.0, 0.0, False), "gland": (1.6, 0.35, False),
         "grover": (1.1, 0.15, False), "nut": (2.2, 0.5, False), "bush": (2.4, 0.0, True)}
shapes, hatches, nfaces = [], {}, {}
for k, s in P.items():
    if k in m.CUT_PARTS:
        c = s.cut(box)
        shapes.append(c)
        pitch, shift, cross = HATCH[k]
        fl = cut_faces(c)
        nfaces[k] = len(fl)
        hatches[k] = [seg for plane, f in fl for seg in hatch(f, plane, pitch, shift, cross)]
    else:
        shapes.append(s)
edges = project(Part.makeCompound(shapes))
ax = TechDraw.projectEx(Part.makeLine(V(-4.0, 0, 0), V(m.Z_TAG + 4.0, 0, 0)), direction)
edges["axis"] = [[[round(v.X, 4), round(v.Y, 4)] for c in ax if c is not None and not c.isNull() for v in c.Vertexes]]
edges["hatch"] = hatches
# размеры на изометрии — точки модели из констант sensor_model (правка модели двигает и размер).
# Толщина гровера: по нижней плоскости разреза z=0 (там сечение шайбы видно между грундбуксой и гайкой),
# выносные — вдоль -Y (ГОСТ 2.317: параллельно аксонометрической оси), размерная линия — в 10 мм бумаги
# (20 мм модели при 1:2) от наибольшего радиуса корпуса (углы шестигранника S46), ГОСТ 2.307; число — за
# стрелкой со стороны гайки (там свободно; сверху над корпусом идут выноски).
x_w0 = m.Z_NUT0 - m.GROVER_S
r_w = m.GROVER_D / 2.0 + m.GROVER_B
r_dim = m.HEX1_E / 2.0 + 20.0
dims = [{"name": "толщина гровера", "p1": [x_w0, -r_w, 0.0], "p2": [m.Z_NUT0, -r_w, 0.0],
         "pd": [x_w0, -r_dim, 0.0], "pt": [m.Z_NUT0 + 12.0, -r_dim, 0.0], "ext": [0.0, -1.0, 0.0]}]
with open(os.path.join(OUT, "sensor_iso_cut.json"), "w", encoding="utf-8") as f:
    json.dump({"edges": edges, "map": {"O": o, "M": M}, "dims": dims}, f)
print("SENSOR_ISO_OK", {k: len(v) for k, v in edges.items() if k not in ("hatch",) and v},
      "| cut faces", nfaces, "| hatch", {k: len(v) for k, v in hatches.items()},
      "| check axis end", Pj(V(m.Z_TAG + 4.0, 0, 0)), edges["axis"][0][-1])
