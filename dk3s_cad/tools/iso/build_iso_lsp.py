# -*- coding: utf-8 -*-
"""build_iso_lsp.py sensor_iso_cut.json sensor_labels.json ВЫХОД.lsp — изометрия датчика для листа общего вида.

Берёт проекцию FreeCAD (sensor_iso_fc.py: видимые рёбра, штриховка разрезов, ось) и выноски, переводит в мм
бумаги (приведённая изометрия ГОСТ 2.317, коэффициент 1,2247, масштаб 1:2, картинка повёрнута на +60° — как
build_sensor_iso_dxf.py) и пишет раздел LISP: функцию dk3s_draw_iso с вызовами dk3s_iso_pl (полилиния),
dk3s_iso_ln (отрезок) и dk3s_leader (выноска). Полилинии упрощаются (Дуглас — Пекер, допуск 0,02 мм бумаги).
Координаты — мм бумаги от левого нижнего угла картинки; на лист их переносит dk3s_iso_p (начало g_dk3s_iso_x/y,
масштаб листа g_dk3s_scale_den). Раздел генерируется — руками не править, менять модель и выноски."""
import json
import math
import sys

K = 1.0 / math.sqrt(2.0 / 3.0)
S = 0.5
A = math.radians(60.0)
CA, SA = math.cos(A), math.sin(A)
TOL = 0.02                                   # допуск упрощения, мм бумаги
# выноски, которые на листе общего вида не повторяются (эти детали подписаны на главном виде)
SKIP = {"Защитная скоба", "Электрод сравнения (2 шт.)", "Токоотвод вспомогательного электрода"}


def rot(p):
    return (p[0] * CA - p[1] * SA, p[0] * SA + p[1] * CA)


def dp(pts, tol):
    """Упрощение ломаной (Дуглас — Пекер)."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    best, bi = -1.0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        d = abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / L if L > 1e-12 else math.hypot(p[0] - a[0], p[1] - a[1])
        if d > best:
            best, bi = d, i
    if best <= tol:
        return [a, b]
    return dp(pts[:bi + 1], tol)[:-1] + dp(pts[bi:], tol)


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    labels = json.load(open(sys.argv[2], encoding="utf-8"))
    E = d["edges"]
    o, M = d["map"]["O"], d["map"]["M"]
    vis = [pl for n in ("hard", "outline") for pl in E[n]]
    allp = [rot(p) for pl in vis for p in pl]
    x0, y0 = min(p[0] for p in allp), min(p[1] for p in allp)

    def T(p):
        q = rot(p)
        return ((q[0] - x0) * K * S, (q[1] - y0) * K * S)

    def T3(x, y, z):
        return T((o[0] + M[0][0] * x + M[0][1] * y + M[0][2] * z, o[1] + M[1][0] * x + M[1][1] * y + M[1][2] * z))

    f = lambda v: f"{v:.2f}".rstrip("0").rstrip(".") if abs(v) > 0.004 else "0"
    out = [";;; ---------------------------------------------------------------------------",
           ";;; 11. ИЗОМЕТРИЯ С ВЫРЕЗОМ — СГЕНЕРИРОВАНО tools/iso/build_iso_lsp.py из модели FreeCAD",
           ";;;     (tools/iso/sensor_model.py -> sensor_iso_fc.py). Руками не править: менять модель и выноски.",
           ";;; ---------------------------------------------------------------------------",
           "(defun dk3s_draw_iso ()"]
    npts = 0
    for pl in vis:
        pts = dp([T(p) for p in pl], TOL)
        npts += len(pts)
        out.append("  (dk3s_iso_pl '(" + " ".join(f(c) for p in pts for c in p) + "))")
    nh = 0
    for key, segs in E["hatch"].items():
        for a, b in segs:
            pa, pb = T(a), T(b)
            out.append(f"  (dk3s_iso_ln {f(pa[0])} {f(pa[1])} {f(pb[0])} {f(pb[1])} g_dk3s_lay_thin)")
            nh += 1
    a, b = E["axis"][0]
    pa, pb = T(a), T(b)
    out.append(f"  (dk3s_iso_ln {f(pa[0])} {f(pa[1])} {f(pb[0])} {f(pb[1])} g_dk3s_lay_axis)")
    nl = 0
    for lab in labels:
        if lab["text"] in SKIP:
            continue
        pt = T3(*lab["p"])
        # колени выносок заданы в координатах листа изометрии (build_sensor_iso_dxf.py: поля 10 и 30 мм)
        kx, ky = lab["knee"][0] - 10.0, lab["knee"][1] - 30.0
        txt = lab["text"].replace('"', '\\"')
        out.append(f"  (dk3s_leader (dk3s_iso_p {f(pt[0])} {f(pt[1])}) (dk3s_iso_p {f(kx)} {f(ky)}) {lab['dir']} \"{txt}\")")
        nl += 1
    # размеры (sensor_iso_fc.py, точки модели): угол размерной линии и наклон выносных — по проекции;
    # группа 52 в CAD — добавка к повороту (опыт с ODA 19.09.2026); число автоматическое — вдоль осей длины истинные
    nd = 0
    g = lambda v: f"{v:.4f}"
    for dm in d.get("dims", []):
        P1, P2, PD, PT = (T3(*dm[k]) for k in ("p1", "p2", "pd", "pt"))
        rot_deg = math.degrees(math.atan2(P2[1] - P1[1], P2[0] - P1[0]))
        q = T3(*(a + b for a, b in zip(dm["p1"], dm["ext"])))
        ext_deg = math.degrees(math.atan2(q[1] - P1[1], q[0] - P1[0]))
        obl = (ext_deg - rot_deg + 180.0) % 360.0 - 180.0
        out.append(f"  (dk3s_dim_obl (dk3s_iso_p {g(P1[0])} {g(P1[1])}) (dk3s_iso_p {g(P2[0])} {g(P2[1])}) "
                   f"(dk3s_iso_p {g(PD[0])} {g(PD[1])}) {rot_deg:.2f} {obl:.2f} \"\" "
                   f"(dk3s_iso_p {g(PT[0])} {g(PT[1])}))   ; {dm['name']}")
        nd += 1
    out.append(")")
    w = (max(p[0] for p in allp) - x0) * K * S
    h = (max(p[1] for p in allp) - y0) * K * S
    out.append(f";;; картинка {w:.1f} x {h:.1f} мм бумаги; полилиний {len(vis)}, точек {npts}, штриховка {nh}, выносок {nl}, "
               f"размеров {nd}")
    open(sys.argv[3], "w", encoding="utf-8", newline="\r\n").write("\n".join(out) + "\n")
    print(f"iso lsp: {len(vis)} polylines, {npts} points, {nh} hatch lines, {nl} leaders, {nd} dims, "
          f"picture {w:.1f} x {h:.1f} mm")


if __name__ == "__main__":
    main()
