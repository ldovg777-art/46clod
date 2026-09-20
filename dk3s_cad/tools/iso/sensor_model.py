# -*- coding: utf-8 -*-
"""3D-модель датчика концентрации ДК-3С-210АВ для изометрии (FreeCAD, freecadcmd).

Размеры — из таблицы параметров dk3s_cad/src/dk3s_drawing_readable.lsp (g_dk3s_*, общий вид 302123.000 ВО),
внутреннее устройство узла ввода — по чертежам ЭКОР: корпус 714.761.000 (Ø32,2 под гильзу, поясок Ø20,8,
конус 120°, камера Ø30 H12, резьба M33x2-6F глубиной 20, 52,5 от правого торца до пояска), гайка нажимная
714.541.000 (M33x2 x20, S36, всего 30, Ø20,8), грундбукса 711.171.000 (Ø29,5/Ø20,8 x9), втулка
фторопластовая 715412.001 (сальник: буртик Ø29 длиной 30, шейка Ø20,5, длина 95 — из расчёта прочности).
Узел наконечника — tip_model_v2 (Fig. 4/5 техописания K1).

По техописанию K1 (лист 16, стр. 4–5, 45): торец гильзы открыт, скоба крестовая (вторая дужка видна ребром по
оси), боковые отверстия — под 90° к фронтальному ряду, перфорация только у торца (до 53 мм); мостики — трубки Ø6
(как трубка РЭ), в жгуте три трубки лежат треугольником: РЭ спереди, мостики за ней; сквозь фторопластовую
втулку проходят все три; вспомогательный электрод — стенка аппарата, на датчике только его токоотвод Ø3.
Условно (нет чертежа): стенка гильзы 2 мм; каналы во втулке; положение наконечника по глубине и путь трубки РЭ
внутри гильзы; концы мостиков (в зоне перфорации). Ось датчика — X (x = z листа, от вершины скобы), плоскость
электродов сравнения — XZ (r листа -> Z), главный вид — взгляд из -Y, провод ВЭ — снизу (-Z).
"""
import math

import FreeCAD as App
import Part

V = App.Vector
XD = V(1, 0, 0)

# --- из таблицы параметров LISP (мм)
GUARD_H, GUARD_W, GUARD_D, GUARD_R = 15.6, 28.0, 2.0, 4.0
TIP_OFF, TIP_D, TIP_S, TIP_LEN, TIP_CONE, TIP_NOSE_D, TIP_VIS = 5.5, 7.0, 6.35, 18.3, 3.5, 1.8, 3.7
TIP_CYL_L, TIP_HEX_L, SHANK_D, SHANK_L = 12.5, 5.8, 5.0, 15.0
WE_D, WE_LEN = 1.4, 2.0
TUBE_D, TUBE_ID = 6.0, 5.0
Z_SLEEVE, SLEEVE_D = 15.6, 32.0
SLEEVE_WALL = 2.0                              # условно; торец гильзы открыт (лист 16)
HOLE_D, HOLE_Z1, HOLE_PITCH, HOLE_N, HOLE_SIDE_N, HOLE_SIDE_ANG = 6.0, 25.5, 20.0, 3, 2, 90.0
Z_SHELL, SHELL_D, SHELL_CH = 224.8, 42.0, 1.0
Z_RELIEF, RELIEF_D, Z_PLATE, PLATE_D = 253.8, 39.0, 258.8, 59.0
Z_HEX1, HEX1_S, HEX1_E, Z_CYL = 265.8, 46.0, 52.0, 285.8
CYL_D, Z_GROOVE, GROOVE_D, Z_HEX2, HEX2_S, HEX2_E, Z_NECK = 33.0, 293.2, 30.0, 296.6, 36.0, 41.0, 306.6
NECK_D, Z_STEP, STEP_D, Z_TAPER, TAPER_D1, TAPER_D2 = 20.8, 314.6, 18.8, 315.6, 16.0, 15.4
Z_TAG, TAG_W, Z_TAG_END = 325.2, 16.0, 335.1
BRIDGE_D = 6.0                                 # мостики — трубки Ø6 (лист 16, развилка у ЭС)
Z_CLAMP1, Z_CLAMP2, CLAMP_L, CLAMP_D = 367.0, 467.2, 7.6, 13.6
Z_BEND, Z_WE_END = 476.0, 483.7
CONN_COLLAR_D, CONN_COLLAR_L, CONN_BODY_D, CONN_BODY_L, CONN_PIN_D, CONN_PIN_L, CONN_TIP_L = 8.0, 2.0, 6.5, 14.0, 2.5, 14.0, 1.0
SE_R, SE_D, Z_SE_START, Z_SE_END = -24.6, 3.0, 283.7, 481.9
RE_R, RE_D, Z_RE, RE_SEG1, RE_NECK, RE_NECK_D, RE_SEG2, RE_GAP = 22.8, 20.0, 521.7, 24.1, 3.0, 16.0, 34.0, 1.0

# --- узел ввода по чертежам ЭКОР (от левого торца корпуса Z_SHELL)
BORE_SLEEVE_D, BORE_SLEEVE_L = 32.2, 6.3        # расточка под гильзу
LAND_D = 20.8                                   # поясок, конец пояска = 52,5 от правого торца
Z_LAND_END = Z_CYL - 52.5                       # 233,3
CHAMBER_D = 30.0                                # камера сальника Ø30 H12
UNDERCUT_D, UNDERCUT_L = 34.0, 4.5              # проточка под выход резьбы
THREAD_L = 20.0                                 # M33x2-6F
NUT_L = 30.0                                    # гайка нажимная: всего 30
Z_NUT0 = Z_NECK - NUT_L                         # 276,6 — торец гайки в корпусе
GLAND_D, GLAND_ID, GLAND_L = 29.5, 20.8, 9.0
# шайба пружинная (гровер) 20 65Г ГОСТ 6402-70, нормальная: d 20,5 +0,84, s = b = 4,5 ±0,15 — между грундбуксой
# и гайкой (табл. 1 ГОСТ, сверено с официальным изданием 19.09.2026; «(5,0)» в скобках — старый размер, только до
# 01.01.85 — до v1.3.1 модель по ошибке брала его).
# В чертежах ЭКОР её нет, ставится по факту (Леонид, 19.09.2026): стопорит гайку и упруго поджимает втулку —
# при остывании фторопласт сжимается, натяг и герметичность сохраняются. Гайка — на месте по общему виду,
# пакет без зазоров: седло -> втулка (буртик 29,9 при 30 по чертежу) -> грундбукса -> шайба -> гайка.
GROVER_D, GROVER_S, GROVER_B = 20.5, 4.5, 4.5
GROVER_ID = GROVER_D + 0.2                      # +0,2: не совпадать с шейкой втулки Ø20,5 (удаление линий)
GROVER_SPLIT_ANG = 135.0                        # разрез шайбы — к зрителю (угол от +Y к +Z)
BUSH_L, BUSH_NECK_D, BUSH_COLLAR_D, BUSH_COLLAR_L = 95.0, 20.5, 29.0, 30.0
Z_BUSH_TOP = Z_TAPER                            # торец втулки (фаска до Ø18,8); «конус Ø16 -> Ø15,4» общего вида —
                                                # это сходящиеся к жгуту трубки, а не деталь (канал Ø6 на Ø11 вышел бы из него)
BUSH_CH_R = 11.0 / 2.0                          # каналы 3 x Ø6 по окружности Ø11 (чертёж 715412.001, vault 07.09.2026)
Z_BUSH0 = Z_BUSH_TOP - BUSH_L                   # 230,2
BRIDGE_END_X = 40.0                            # условно: концы мостиков в зоне перфорации (0…53 мм от торца)
# жгут: три трубки Ø6 треугольником (сторона 6,1), РЭ спереди (-Y), мостики за ней на ±3,05 по Z
TRI = 6.3                                       # трубки Ø6 с зазором 0,3 (каналы Ø6,1 не касаются)
WE_Y = -TRI / math.sqrt(3.0)                    # -3,52
BR_Y, BR_Z = TRI / (2.0 * math.sqrt(3.0)), TRI / 2.0
TIP_Y = -5.0                                    # условно: наконечник по глубине (на виде — смещение 5,5 вверх)

T30 = math.tan(math.radians(30.0))
T60 = math.tan(math.radians(60.0))


def revolve(profile):
    """Тело вращения вокруг оси X из замкнутого профиля [(x, r), ...] в плоскости XZ."""
    pts = [V(x, 0, r) for x, r in profile]
    return Part.Face(Part.makePolygon(pts + [pts[0]])).revolve(V(0, 0, 0), XD, 360)


def cyl(d, x1, x2, z0=0.0, y0=0.0):
    return Part.makeCylinder(d / 2.0, x2 - x1, V(x1, y0, z0), XD)


def hex_prism(s, e, x1, x2, chamfer_at=None, ang0=90.0):
    """Шестигранник S=s (по углам e) от x1 до x2; углы — вверх/вниз (ang0=90), как «вид по углам»;
    фаска 30° до Ø s на торце chamfer_at (x1 или x2)."""
    pts = [V(x1, e / 2 * math.cos(math.radians(ang0 + a)), e / 2 * math.sin(math.radians(ang0 + a))) for a in range(0, 360, 60)]
    prism = Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(x2 - x1, 0, 0))
    if chamfer_at is None:
        return prism
    c = (e - s) / 2.0 * T30                      # глубина фаски у рёбер
    L = x2 - x1
    if chamfer_at == x2:
        prof = [(x1, 0.0), (x1, e / 2 + 1), (x2 - c - 1 * T30, e / 2 + 1), (x2, s / 2.0), (x2, 0.0)]
    else:
        prof = [(x2, 0.0), (x2, e / 2 + 1), (x1 + c + 1 * T30, e / 2 + 1), (x1, s / 2.0), (x1, 0.0)]
    return prism.common(revolve(prof))


def pipe(segs, d, plane="xz", c=0.0):
    """Трубка/проволока Ø d по траектории: сегменты ("L", (x1, v1), (x2, v2)) или
    ("A", (x1, v1), (xm, vm), (x2, v2)) в плоскости XZ (v — это z, y = c) или XY (v — это y, z = c)."""
    P3 = (lambda x, v: V(x, c, v)) if plane == "xz" else (lambda x, v: V(x, v, c))
    edges = []
    for sg in segs:
        if sg[0] == "L":
            edges.append(Part.makeLine(P3(*sg[1]), P3(*sg[2])))
        else:
            edges.append(Part.Arc(P3(*sg[1]), P3(*sg[2]), P3(*sg[3])).toShape())
    path = Part.Wire(edges)
    e0 = edges[0]
    prof = Part.Wire(Part.makeCircle(d / 2.0, e0.valueAt(e0.FirstParameter), e0.tangentAt(e0.FirstParameter)))
    return path.makePipeShell([prof], True, True)


def s_bend_segs(x1, z1, x2, z2):
    """Сегменты S-образного изгиба от (x1, z1) к (x2, z2), касательные вдоль X
    (как dk3s_draw_bend: две дуги одного радиуса, перегиб посередине)."""
    dx, dz = x2 - x1, z2 - z1
    sg = 1.0 if dz > 0 else -1.0
    R = (dx * dx + dz * dz) / (4.0 * abs(dz))
    th = math.atan2(dx / 2.0, R - abs(dz) / 2.0)
    p1 = lambda f: (x1 + R * math.sin(f), z1 + sg * (R - R * math.cos(f)))
    p2 = lambda f: (x2 - R * math.sin(f), z2 - sg * (R - R * math.cos(f)))
    return [("A", p1(0.0), p1(th / 2), p1(th)), ("A", p2(th), p2(th / 2), p2(0.0))]


# каналы втулки: (y, z) центров — РЭ к -Y, мостики через 120°
CH_WE = (-BUSH_CH_R, 0.0)
CH_BR = [(BUSH_CH_R * 0.5, BUSH_CH_R * math.sqrt(3) / 2), (BUSH_CH_R * 0.5, -BUSH_CH_R * math.sqrt(3) / 2)]


def chain(pts, d):
    """Трубка Ø d по ломаной через точки pts (цилиндры, в изломах — шары того же диаметра)."""
    s = None
    for a, b in zip(pts, pts[1:]):
        c = Part.makeCylinder(d / 2.0, (b - a).Length, a, b - a)
        s = c if s is None else s.fuse(c)
    for q in pts[1:-1]:
        s = s.fuse(Part.makeSphere(d / 2.0, q))
    return s.removeSplitter()


def connector(x0, z0, y0=0.0):
    x1 = x0 + CONN_COLLAR_L
    x2 = x1 + CONN_BODY_L
    x3 = x2 + 1.0 + CONN_PIN_L
    rp = CONN_PIN_D / 2.0
    s = cyl(CONN_COLLAR_D, x0, x1, z0, y0).fuse(cyl(CONN_BODY_D, x1, x2, z0, y0)).fuse(cyl(CONN_PIN_D, x2, x3, z0, y0))
    s = s.fuse(Part.makeCone(rp, 0.4 * rp, CONN_TIP_L, V(x3, y0, z0), XD))
    return s.removeSplitter()


def guard():
    """Скоба крестовая: две П-образные дужки из проволоки Ø2 — в плоскостях XZ и XY (вторая на листе 16
    видна ребром — полоса 2 мм по оси)."""
    rw = GUARD_D / 2.0
    w2 = GUARD_W / 2.0 - rw                       # осевая линия ног (13)
    rb = GUARD_R - rw                             # радиус гиба по осевой (3)
    xb, zb = rw + rb, w2 - rb                     # центры гибов (4, ±10)
    c45 = rb * math.cos(math.radians(45))
    segs = [("L", (Z_SLEEVE, w2), (xb, w2)), ("A", (xb, w2), (xb - c45, zb + c45), (rw, zb)),
            ("L", (rw, zb), (rw, -zb)), ("A", (rw, -zb), (xb - c45, -zb - c45), (xb, -w2)),
            ("L", (xb, -w2), (Z_SLEEVE, -w2))]
    return pipe(segs, GUARD_D, "xz").fuse(pipe(segs, GUARD_D, "xy")).removeSplitter()


def tip():
    """Наконечник (фторопласт) с рабочим электродом; ось — X, носик к скобе; центр (TIP_Y, TIP_OFF)."""
    zh = Z_SLEEVE - TIP_VIS                       # 11,9: начало шестигранника (к скобе)
    zc = zh - TIP_CONE                            # торец носика
    zw = zc - WE_LEN                              # конец электрода
    x_cyl = zh + TIP_HEX_L                        # 17,7: конец шестигранника, начало цилиндра Ø7
    x_face = zh + TIP_LEN                         # 30,2: торец тела = конец трубки (14,6 мм за торцом гильзы)
    e = TIP_S / math.cos(math.radians(30))
    body = cyl(TIP_D, x_cyl, x_face, TIP_OFF, TIP_Y)
    pts = [V(zc, TIP_Y + e / 2 * math.cos(math.radians(a)), TIP_OFF + e / 2 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    hexp = Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(x_cyl - zc, 0, 0))
    hexp = hexp.common(cyl(TIP_D, zc, x_cyl, TIP_OFF, TIP_Y))
    slope = (TIP_D / 2 - TIP_NOSE_D / 2) / TIP_CONE
    cone = Part.makeCone(TIP_NOSE_D / 2, TIP_D / 2 + slope * (x_cyl - zh), x_cyl - zc, V(zc, TIP_Y, TIP_OFF), XD)
    body = body.fuse(hexp.common(cone))
    body = body.fuse(cyl(SHANK_D, x_face, x_face + SHANK_L, TIP_OFF, TIP_Y)).removeSplitter()
    we = cyl(WE_D, zw, zc + 0.3, TIP_OFF, TIP_Y)
    return body, we, x_face


def build():
    P = {}
    P["guard"] = guard()
    tip_body, we, x_face = tip()
    P["tip"] = tip_body
    P["we"] = we
    # защитная гильза: открытый торец, перфорация у торца (фронтальный ряд к зрителю главного вида -Y,
    # боковые — под 90°, в шахматном порядке)
    ro = SLEEVE_D / 2.0
    x_end = Z_SHELL + BORE_SLEEVE_L               # гильза до дна расточки корпуса
    sleeve = cyl(SLEEVE_D, Z_SLEEVE, x_end).cut(cyl(SLEEVE_D - 2 * SLEEVE_WALL, Z_SLEEVE - 1, x_end + 1))
    for i in range(HOLE_N):
        x = HOLE_Z1 + i * HOLE_PITCH
        sleeve = sleeve.cut(Part.makeCylinder(HOLE_D / 2, ro + 1, V(x, 0, 0), V(0, -1, 0)))
    for i in range(HOLE_SIDE_N):
        x = HOLE_Z1 + HOLE_PITCH / 2 + i * HOLE_PITCH
        for sg in (1, -1):
            a = math.radians(HOLE_SIDE_ANG) * sg
            sleeve = sleeve.cut(Part.makeCylinder(HOLE_D / 2, ro + 1, V(x, 0, 0), V(0, -math.cos(a), math.sin(a))))
    P["sleeve"] = sleeve
    # корпус 714.761.000: снаружи M42x3 (фаска 1), проточка, фланец Ø59, шестигранник S46 (фаска 30° справа)
    outer = revolve([(Z_SHELL, 0.0), (Z_SHELL, SHELL_D / 2 - SHELL_CH), (Z_SHELL + SHELL_CH, SHELL_D / 2),
                     (Z_RELIEF, SHELL_D / 2), (Z_RELIEF, RELIEF_D / 2), (Z_PLATE, RELIEF_D / 2),
                     (Z_PLATE, PLATE_D / 2), (Z_HEX1, PLATE_D / 2), (Z_HEX1, 0.0)])
    outer = outer.fuse(hex_prism(HEX1_S, HEX1_E, Z_HEX1, Z_CYL, chamfer_at=Z_CYL)).removeSplitter()
    x_cone = Z_LAND_END + (CHAMBER_D - LAND_D) / 2.0 / T60
    x_thr = Z_CYL - THREAD_L
    inner = revolve([(Z_SHELL - 1, 0.0), (Z_SHELL - 1, BORE_SLEEVE_D / 2), (Z_SHELL + BORE_SLEEVE_L, BORE_SLEEVE_D / 2),
                     (Z_SHELL + BORE_SLEEVE_L, LAND_D / 2), (Z_LAND_END, LAND_D / 2), (x_cone, CHAMBER_D / 2),
                     (x_thr - UNDERCUT_L, CHAMBER_D / 2), (x_thr - UNDERCUT_L, UNDERCUT_D / 2), (x_thr, UNDERCUT_D / 2),
                     (x_thr, CYL_D / 2 + 0.05), (Z_CYL + 1, CYL_D / 2 + 0.05), (Z_CYL + 1, 0.0)])
    body = outer.cut(inner)
    body = body.cut(cyl(SE_D, Z_CYL - 7.0, Z_CYL + 1, SE_R))      # отверстие Ø3 x7 под токоотвод ВЭ
    P["body"] = body
    # деталь S36 (гайка нажимная 714.541.000, наружная резьба M33x2): резьба до канавки, канавка Ø30,
    # шестигранник S36 с фаской 30° снаружи
    nut = revolve([(Z_NUT0, NECK_D / 2 + 0.05), (Z_NUT0, CYL_D / 2), (Z_GROOVE, CYL_D / 2), (Z_GROOVE, GROOVE_D / 2),
                   (Z_HEX2, GROOVE_D / 2), (Z_HEX2, NECK_D / 2 + 0.05)])
    nut = nut.fuse(hex_prism(HEX2_S, HEX2_E, Z_HEX2, Z_NECK, chamfer_at=Z_NECK).cut(cyl(NECK_D + 0.1, Z_HEX2 - 1, Z_NECK + 1)))
    P["nut"] = nut.removeSplitter()
    # шайба пружинная (гровер) у торца гайки: кольцо с косым разрезом (на изометрии рассечена вместе с узлом)
    x_w0 = Z_NUT0 - GROVER_S
    ring = cyl(GROVER_D + 2 * GROVER_B, x_w0, Z_NUT0).cut(cyl(GROVER_ID, x_w0 - 1, Z_NUT0 + 1))
    slot = Part.makeBox(GROVER_S + 4.0, GROVER_B + 6.0, 1.2, V(x_w0 - 2.0, GROVER_ID / 2 - 3.0, -0.6))
    slot.rotate(V(x_w0 + GROVER_S / 2, 0, 0), V(0, 1, 0), 15.0)          # косой разрез
    slot.rotate(V(0, 0, 0), XD, GROVER_SPLIT_ANG - 90.0)                  # радиальная ось Y -> к зрителю
    P["grover"] = ring.cut(slot)
    # грундбукса 711.171.000 между буртиком втулки и шайбой; конус 120° к втулке
    x_g1 = x_w0 - GLAND_L
    P["gland"] = revolve([(x_g1, GLAND_ID / 2 + 1.2 * T60), (x_g1, GLAND_D / 2), (x_w0, GLAND_D / 2),
                          (x_w0, GLAND_ID / 2), (x_g1 + 1.2, GLAND_ID / 2)])
    # втулка фторопластовая 715412.001 (сальник): шейка Ø20,5, буртик Ø29 x30 с конусом 120° на седло корпуса;
    # снаружи гайки — шейка Ø20,8, ступень Ø18,8, конус Ø16 -> Ø15,4 (как на общем виде)
    rn, rc = BUSH_NECK_D / 2, BUSH_COLLAR_D / 2
    # без зазоров (замечание Леонида 19.09.2026, v1.3.2; до этого стояли технологические 0,3 мм): конус буртика
    # лежит на седле корпуса (совпадает с ним от Ø20,8 до Ø29), торец буртика упирается в грундбуксу.
    # Буртик выходит 29,9 при 30 по чертежу 715412.001 — пакет с гровером 4,5 сходится с положением гайки.
    x_c0 = Z_LAND_END - (LAND_D / 2 - rn) / T60    # начало конуса буртика на шейке Ø20,5 — внутри пояска Ø20,8
    x_c1 = x_c0 + (rc - rn) / T60
    x_c2 = x_g1
    bush = revolve([(Z_BUSH0, 0.0), (Z_BUSH0, rn), (x_c0, rn), (x_c1, rc), (x_c2, rc), (x_c2, rn), (Z_NECK, rn),
                    (Z_NECK, NECK_D / 2), (Z_STEP, NECK_D / 2), (Z_STEP, STEP_D / 2), (Z_BUSH_TOP, STEP_D / 2),
                    (Z_BUSH_TOP, 0.0)])
    # три канала Ø6 по окружности Ø11 (чертёж 715412.001): РЭ — к зрителю главного вида (-Y), мостики за ней
    ch = cyl(TUBE_D + 0.1, Z_BUSH0 - 1, Z_BUSH_TOP + 1, CH_WE[1], CH_WE[0])
    for c in CH_BR:
        ch = ch.fuse(cyl(BRIDGE_D + 0.1, Z_BUSH0 - 1, Z_BUSH_TOP + 1, c[1], c[0]))
    P["bush"] = bush.cut(ch)
    # трубка токоотвода РЭ Ø6: от торца тела наконечника до низа втулки — прямая с малым наклоном (условно),
    # дальше в жгуте спереди до разъёма; хомуты и бирка охватывают жгут
    P["tube"] = chain([V(x_face, TIP_Y, TIP_OFF), V(Z_BUSH0, CH_WE[0], CH_WE[1]), V(Z_BUSH_TOP, CH_WE[0], CH_WE[1]),
                       V(Z_TAG, WE_Y, 0.0), V(Z_WE_END, WE_Y, 0.0)], TUBE_D)
    P["clamps"] = cyl(CLAMP_D, Z_CLAMP1, Z_CLAMP1 + CLAMP_L).fuse(cyl(CLAMP_D, Z_CLAMP2, Z_CLAMP2 + CLAMP_L))
    P["tag"] = cyl(TAG_W, Z_TAG, Z_TAG_END)
    P["we_conn"] = connector(Z_WE_END, 0.0, WE_Y)
    # мостики Ø6: от концов в зоне перфорации (условно) через втулку, в жгуте за трубкой РЭ, S-изгиб к ЭС
    br = []
    for sg, c in zip((1, -1), CH_BR):
        z = sg * BR_Z
        inner = chain([V(BRIDGE_END_X, c[0], c[1]), V(Z_BUSH_TOP, c[0], c[1]), V(Z_TAG, BR_Y, z)], BRIDGE_D)
        segs = [("L", (Z_TAG, z), (Z_BEND, z))] + s_bend_segs(Z_BEND, z, Z_RE, sg * RE_R)
        br.append(inner.fuse(pipe(segs, BRIDGE_D, "xz", BR_Y)).removeSplitter())
    P["bridges"] = br[0].fuse(br[1])
    # электроды сравнения — на осях мостиков (по глубине y = BR_Y)
    res = []
    for sg in (1, -1):
        z0 = sg * RE_R
        x1, x2, x3, x4 = Z_RE, Z_RE + RE_SEG1, Z_RE + RE_SEG1 + RE_NECK, Z_RE + RE_SEG1 + RE_NECK + RE_SEG2
        r = cyl(RE_D, x1, x2, z0, BR_Y).fuse(cyl(RE_NECK_D, x2, x3, z0, BR_Y)).fuse(cyl(RE_D, x3, x4, z0, BR_Y))
        r = r.fuse(cyl(CONN_BODY_D, x4, x4 + RE_GAP, z0, BR_Y)).fuse(connector(x4 + RE_GAP, z0, BR_Y))
        res.append(r.removeSplitter())
    P["re"] = res[0].fuse(res[1])
    # токоотвод вспомогательного электрода (из отверстия в шестиграннике корпуса) и его разъём
    P["se"] = cyl(SE_D, Z_SE_START, Z_SE_END, SE_R).fuse(connector(Z_SE_END, SE_R)).removeSplitter()
    return P


# детали, которые рассекаются вырезом (ГОСТ 2.305: трубки, проволока, провода не рассекаются)
CUT_PARTS = ("sleeve", "body", "nut", "gland", "grover", "bush")   # шайба рассечена: так видно, где она стоит
X_CUT0, X_CUT1 = Z_SLEEVE - 1.0, Z_BUSH_TOP + 0.5
