# -*- coding: utf-8 -*-
"""freecadcmd export_3d_html.py — 3D-модель датчика ДК-3С-210АВ в одном HTML-файле (three.js, вращение мышью).

Строит модель sensor_model.build() и тесселирует каждую деталь ПО ГРАНЯМ (face.tessellate): внутри грани
нормали сглаживаются, на рёбрах между гранями остаются острыми. Детали из m.CUT_PARTS выгружаются дважды —
целиком и с вырезом четверти, как в sensor_iso_fc.py (s.cut(box): настоящие тела с гранями сечения, не клиппинг).
Координаты — Float32Array, индексы — Uint16/Uint32, всё в base64 внутри HTML. three.js подключается importmap'ом
с cdn.jsdelivr.net — при открытии страницы нужен интернет; сам скрипт ничего не скачивает.

Запуск (путь вывода — через переменную окружения: лишние аргументы freecadcmd пытается открыть как файлы):
    set DK3S_HTML_OUT=C:/путь/Датчик_ДК-3С_3D.html
    "C:/Users/<user>/AppData/Local/Programs/FreeCAD 1.1/bin/freecadcmd.exe" export_3d_html.py
Без переменной — sys.argv[-1], если он оканчивается на .html, иначе Датчик_ДК-3С_3D.html в текущей папке.
Допуски тесселяции: DK3S_LIN — линейный, мм (по умолчанию 0.01), DK3S_ANG — угловой, градусы (по умолчанию 8).
При 0.01 / 8° окружности делятся на 90–120 отрезков, всего около 83 тыс. треугольников, HTML около 1,7 МБ
(19.09.2026: сборка 1,3 с; объём сеток совпадает с объёмом тел до 0,09 %).
Если скрипт запускает кто-то, кроме пользователя, пока модель правят параллельно: freecadcmd импортирует файл как
модуль и пишет __pycache__ рядом — запускать через exec из своей папки (см. html3d_work/run_export.py сессии 19.09).
"""
import base64
import datetime
import json
import math
import os
import re
import sys
import time

sys.dont_write_bytecode = True          # не оставлять __pycache__ рядом с моделью
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import FreeCAD as App  # noqa: E402
import MeshPart  # noqa: E402
import Part  # noqa: E402
import numpy as np  # noqa: E402
import sensor_model as m  # noqa: E402

V = App.Vector
THREE_VER = "0.160.0"                   # версия three.js на cdn.jsdelivr.net
MODEL_VERSION = "v1.3.2"                # последняя правка геометрии sensor_model.py (узел сальника без зазоров)
LIN = float(os.environ.get("DK3S_LIN", "0.01"))
ANG = float(os.environ.get("DK3S_ANG", "8"))
EDGE_ANGLE = 25                         # порог угла для тёмных рёбер (THREE.EdgesGeometry), градусы
STEEL = "08Х18Н10Т"
PCS = " (2 шт.)"                    # неразрывный пробел: «шт.)» не уходит на отдельную строку списка

# Контакты выводов (штыри разъёмов) — в цвета токоотводов по ТТ п. 6 чертежа: RE1 синий, RE2 белый, WE красный,
# SE чёрный. Какой электрод сравнения «1», в документах не задано: ES1_SIDE = +1 — ЭС1 верхний (+Z), ЭС2 нижний;
# -1 — наоборот (поменять местами — только эта константа).
ES1_SIDE = +1
CONTACT_BOX_H = 5.0                     # полуширина ящика вокруг оси штыря, мм: шире штыря Ø2,5, уже шага выводов
_ES = {1: "верхнего электрода сравнения (+Z)", -1: "нижнего электрода сравнения (−Z)"}

GROUPS = ["Наконечник и защитная гильза", "Узел ввода (сальник)", "Жгут, мостики, электроды",
          "Контакты выводов — цвета токоотводов (ТТ п. 6)"]
GROUP_NOTES = {3: "ЭС1 — %s электрод сравнения, ЭС2 — %s. Какой из них первый, в документах не задано — принято "
                  "условно." % (("верхний (+Z)", "нижний (−Z)") if ES1_SIDE > 0 else ("нижний (−Z)", "верхний (+Z)"))}
# ключ модели, название, примечание, цвет, группа, род материала (для освещения).
# Материалы — по техтребованиям чертежа (dk3s_drawing.lsp, п. 2, 3, 5, 8); где материала в документах нет,
# цвет условный. РЭ — рабочий электрод. Ключи c_* — контакты, выделенные из re / we_conn / se (split_contacts).
PARTS = [
    ("guard", "Защитная скоба", "крестовая, проволока Ø2", "#c3c8ce", 0, "steel"),
    ("tip", "Наконечник", "фторопласт", "#efe8d3", 0, "ptfe"),
    ("we", "Рабочий электрод (РЭ)", "проволока Ø1,4, выступ 2 мм", "#c79d42", 0, "metal"),
    ("sleeve", "Защитная гильза", "Ø32, перфорация Ø6", "#cdd2d7", 0, "steel"),
    ("body", "Корпус", "714.761.000, сталь " + STEEL, "#c6cbd1", 1, "steel"),
    ("bush", "Втулка фторопластовая", "715412.001, фторопласт Ф-4Д", "#f4efe1", 1, "ptfe"),
    ("gland", "Грундбукса", "711.171.000, сталь " + STEEL, "#d2d6db", 1, "steel"),
    ("grover", "Шайба пружинная (гровер)", "шайба 20 65Г ГОСТ 6402-70", "#7d838b", 1, "steel"),
    ("nut", "Гайка нажимная", "714.541.000, сталь " + STEEL, "#bec4cb", 1, "steel"),
    ("tube", "Трубка токоотвода РЭ", "защитная трубка Ø6, фторопласт", "#ebe3cc", 2, "ptfe"),
    ("bridges", "Электролитические мостики" + PCS, "трубки Ø6", "#94b89d", 2, "other"),
    ("clamps", "Хомуты" + PCS, "", "#bba98a", 2, "other"),
    ("tag", "Бирка", "", "#d9ca8b", 2, "other"),
    ("we_conn", "Разъём РЭ", "без штыря — он в «Контакт РЭ»", "#b3aba0", 2, "other"),
    ("re", "Электроды сравнения" + PCS, "Ø20, с разъёмами без штырей", "#a79fca", 2, "other"),
    ("se", "Токоотвод вспомогательного электрода", "провод Ø3 и разъём без штыря; сам электрод — стенка аппарата",
     "#97a1ac", 2, "other"),
    ("c_re1", "Контакт ЭС1 (синий)", "штырь Ø2,5 разъёма " + _ES[ES1_SIDE], "#2f6bd8", 3, "contact"),
    ("c_re2", "Контакт ЭС2 (белый)", "штырь Ø2,5 разъёма " + _ES[-ES1_SIDE], "#ffffff", 3, "contact"),
    ("c_se", "Контакт ВЭ (чёрный)", "штырь Ø2,5 разъёма токоотвода вспомогательного электрода", "#1c1e22", 3,
     "contact"),
    ("c_we", "Контакт РЭ (красный)", "штырь Ø2,5 разъёма рабочего электрода", "#d2392c", 3, "contact"),
]


def out_path():
    p = os.environ.get("DK3S_HTML_OUT", "").strip()
    if not p and len(sys.argv) > 1 and sys.argv[-1].lower().endswith(".html"):
        p = sys.argv[-1]
    if not p:
        p = os.path.join(os.getcwd(), "Датчик_ДК-3С_3D.html")
    return os.path.abspath(p)


def model_version():
    """Версия ГЕОМЕТРИИ модели для подписи внизу страницы: MODEL_VERSION или переменная DK3S_MODEL_VERSION.
    README пакета нумерует и правки только чертежа (1.3.3 — размер на изометрии), поэтому номер оттуда
    не берётся, а лишь сверяется: если в README версия новее, печатается напоминание проверить MODEL_VERSION."""
    ver = os.environ.get("DK3S_MODEL_VERSION", "").strip() or MODEL_VERSION
    try:
        with open(os.path.join(HERE, "..", "..", "README.md"), encoding="utf-8") as f:
            mm = re.search(r"Что изменено в версии (\d+(?:\.\d+)+)", f.read())
        if mm and "v" + mm.group(1) != ver:
            print("NOTE: README latest version is v%s, footer says %s - update MODEL_VERSION "
                  "if sensor_model.py changed since" % (mm.group(1), ver))
    except OSError:
        pass
    return ver


def is_section(f):
    """Грань сечения выреза: плоскость y=0 (z>0) или z=0 (y<0) — как cut_faces() в sensor_iso_fc.py."""
    if f.Surface.TypeId != "Part::GeomPlane":
        return False
    n = f.normalAt(0, 0)
    c = f.CenterOfMass
    if abs(abs(n.z) - 1) < 1e-6 and abs(c.z) < 1e-6 and c.y < 0:
        return True
    return abs(abs(n.y) - 1) < 1e-6 and abs(c.y) < 1e-6 and c.z > 0


def b64(arr):
    return base64.b64encode(arr.tobytes()).decode("ascii")


def mesh(shape, cut):
    """Сетка детали по граням: вершины не общие между гранями (острые рёбра), общие внутри грани.
    Грани сечения — в конце, с индекса sec (в JS — отдельная группа с чуть более тёмным цветом)."""
    s = shape.copy()
    # разбиение всей детали сразу: общие рёбра соседних граней делятся одинаково (без щелей); угловой допуск
    # MeshPart'а задаёт гладкость тонких цилиндров, face.tessellate дальше берёт уже готовое разбиение
    MeshPart.meshFromShape(Shape=s, LinearDeflection=LIN, AngularDeflection=math.radians(ANG), Relative=False)
    faces = ([], [])
    nsec = 0
    for f in s.Faces:
        pts, tris = f.tessellate(LIN)
        if not tris:
            continue
        sec = bool(cut and is_section(f))
        nsec += sec
        faces[1 if sec else 0].append((pts, tris))
    P, I = [], []
    nv = 0
    sec_start = 0
    for gi, grp in enumerate(faces):
        for pts, tris in grp:
            P.append(np.array([(p.x, p.y, p.z) for p in pts], dtype=np.float64))
            I.append(np.asarray(tris, dtype=np.int64).reshape(-1, 3) + nv)
            nv += len(pts)
        if gi == 0:
            sec_start = sum(len(i) for i in I) * 3
    pos = np.concatenate(P)
    idx = np.concatenate(I)
    assert idx.min() >= 0 and idx.max() < nv
    a, b, c = pos[idx[:, 0]], pos[idx[:, 1]], pos[idx[:, 2]]
    vol_mesh = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)   # проверка ориентации треугольников
    i32 = nv > 65535
    g = {"pos": b64(pos.astype("<f4")), "idx": b64(idx.astype("<u4" if i32 else "<u2")), "i32": i32,
         "sec": int(sec_start), "nv": int(nv), "nt": int(len(idx)), "vol": round(float(s.Volume), 2)}
    return g, vol_mesh, nsec


def split_contacts(P):
    """Контакты выводов отдельными телами: штырь Ø m.CONN_PIN_D с конусом на конце разъёма (connector() модели)
    у we_conn, se и каждого из двух электродов сравнения (re). Начало штыря — по вершинам его цилиндрической
    грани радиуса CONN_PIN_D/2 вдоль X, ось — по Surface.Center; ящик по X от начала штыря до конца вывода:
    штырь = s.common(ящик), остаток детали = s.cut(ящик). Возвращает новый словарь деталей."""
    rp = m.CONN_PIN_D / 2.0
    Q = dict(P)
    pins = {}
    for key, expect in (("we_conn", 1), ("se", 1), ("re", 2)):
        s = P[key]
        axes = []
        for f in s.Faces:
            srf = f.Surface
            if (srf.TypeId == "Part::GeomCylinder" and abs(srf.Radius - rp) < 1e-6
                    and abs(abs(srf.Axis.x) - 1.0) < 1e-9):
                axes.append((min(v.Point.x for v in f.Vertexes), srf.Center.y, srf.Center.z))
        assert len(axes) == expect, ("contact pins", key, axes)
        rest = s
        for x0, yc, zc in axes:
            box = Part.makeBox(s.BoundBox.XMax - x0 + 5.0, 2 * CONTACT_BOX_H, 2 * CONTACT_BOX_H,
                               V(x0, yc - CONTACT_BOX_H, zc - CONTACT_BOX_H))
            pin = s.common(box)
            rest = rest.cut(box)
            pins.setdefault(key, []).append((zc, pin, x0))
        dv = rest.Volume + sum(p.Volume for _, p, _ in pins[key]) - s.Volume
        print("CONTACT %-7s pins %d, pin volume %s mm3, start x %s, volume balance %+.4f mm3" % (
            key, len(axes), [round(p.Volume, 2) for _, p, _ in pins[key]], [round(x, 2) for _, _, x in pins[key]], dv))
        assert abs(dv) < 1e-3 * s.Volume
        Q[key] = rest
    Q["c_we"] = pins["we_conn"][0][1]
    Q["c_se"] = pins["se"][0][1]
    for zc, pin, _ in pins["re"]:
        Q["c_re1" if zc * ES1_SIDE > 0 else "c_re2"] = pin
    return Q


def main():
    t0 = time.time()
    dst = out_path()
    P = split_contacts(m.build())
    keys = [p[0] for p in PARTS]
    assert sorted(keys) == sorted(P.keys()), ("parts mismatch", sorted(P.keys()))
    R = 40.0
    box = Part.makeBox(m.X_CUT1 - m.X_CUT0, R, R, V(m.X_CUT0, -R, 0.0))
    parts, tot_t, tot_v, worst = [], 0, 0, 0.0
    for key, name, note, color, group, kind in PARTS:
        s = P[key]
        full, vm, _ = mesh(s, False)
        worst = max(worst, abs(vm - s.Volume) / s.Volume)
        rec = {"key": key, "name": name, "note": note, "color": color, "group": group, "kind": kind,
               "full": full, "cut": None}
        msg = "full %6d tri" % full["nt"]
        tot_t += full["nt"]
        tot_v += full["nv"]
        if key in m.CUT_PARTS:
            sc = s.cut(box)
            cut, vmc, nsec = mesh(sc, True)
            worst = max(worst, abs(vmc - sc.Volume) / sc.Volume)
            rec["cut"] = cut
            tot_t += cut["nt"]
            tot_v += cut["nv"]
            msg += " | cut %6d tri, section faces %d" % (cut["nt"], nsec)
        parts.append(rec)
        print("PART %-8s %s" % (key, msg))
    ver = model_version()
    built = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    data = {"model": "dk3s_cad/tools/iso/sensor_model.py", "version": ver, "lin": LIN, "ang": ANG,
            "edgeAngle": EDGE_ANGLE, "groups": GROUPS, "groupNotes": GROUP_NOTES, "cutParts": list(m.CUT_PARTS),
            "triangles": tot_t, "parts": parts}
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (TEMPLATE.replace("__THREE_VER__", THREE_VER).replace("__VERSION__", ver)
            .replace("__BUILT__", built).replace("__DATA__", js))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("EXPORT_3D_HTML_OK parts=%d triangles=%d vertices=%d lin=%g ang=%g version=%s"
          % (len(parts), tot_t, tot_v, LIN, ANG, ver))
    print("  mesh volume vs solid volume: worst relative deviation %.4f%%" % (worst * 100))
    print("  size %.2f MB, time %.1f s, out %s" % (os.path.getsize(dst) / 1e6, time.time() - t0, ascii(dst)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Датчик ДК-3С-210АВ — 3D-модель</title>
<style>
  :root {
    --bg: #eef0f3; --panel: #ffffff; --ink: #1d232b; --muted: #5f6773;
    --line: #d8dce2; --btn: #f7f8fa; --btn-line: #c3c9d2; --hover: #e8eef7; --hover-line: #9db3d3;
  }
  * { box-sizing: border-box; }
  [hidden] { display: none !important; }
  html, body { margin: 0; }
  body {
    min-height: 100vh; display: flex; flex-direction: column;
    background: var(--bg); color: var(--ink);
    font: 14px/1.4 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  }
  header { background: var(--panel); border-bottom: 1px solid var(--line); padding: 10px 16px; }
  h1 { margin: 0; font-size: 18px; font-weight: 600; }
  .app {
    flex: 1 1 auto; min-height: 0; display: grid;
    grid-template-columns: minmax(0, 1fr) 320px; grid-template-rows: minmax(0, 1fr);
  }
  .stage { display: flex; flex-direction: column; min-width: 0; min-height: 0; }
  .toolbar {
    display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px;
    padding: 8px 12px; background: var(--panel); border-bottom: 1px solid var(--line);
  }
  button {
    font: inherit; padding: 5px 12px; border: 1px solid var(--btn-line); border-radius: 6px;
    background: var(--btn); color: var(--ink); cursor: pointer;
  }
  button:hover { background: var(--hover); border-color: var(--hover-line); }
  button:active { transform: translateY(1px); }
  .sep { width: 1px; height: 22px; background: var(--line); margin: 0 4px; }
  .toggle { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; user-select: none; }
  .toggle input { margin: 0; width: 16px; height: 16px; }
  .view {
    position: relative; flex: 1 1 auto; min-height: 0; overflow: hidden;
    background: radial-gradient(ellipse at 50% 38%, #ffffff 0%, #f0f2f5 55%, #e1e5ea 100%);
  }
  .view canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; outline: none; }
  .status {
    position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
    padding: 24px; text-align: center; color: var(--muted); font-size: 15px; pointer-events: none;
  }
  .status.err { color: #9b2c2c; background: rgba(255, 255, 255, .85); }
  .hint {
    position: absolute; left: 10px; right: 10px; bottom: 8px; font-size: 12px; color: #4a525d;
    pointer-events: none; text-shadow: 0 1px 0 rgba(255, 255, 255, .9);
  }
  .hint .touch { display: none; }
  @media (hover: none) and (pointer: coarse) {
    .hint .mouse { display: none; }
    .hint .touch { display: inline; }
  }
  .side {
    background: var(--panel); border-left: 1px solid var(--line);
    padding: 12px 14px 16px; overflow-y: auto; min-height: 0;
  }
  .side h2 {
    font-size: 15px; margin: 0 0 4px; display: flex; align-items: center;
    justify-content: space-between; gap: 8px;
  }
  .side h2 button { padding: 2px 9px; font-size: 12px; font-weight: 400; }
  .grp { font-size: 12px; color: var(--muted); margin: 10px 0 2px; font-weight: 600; }
  .grp-note { font-size: 11.5px; color: var(--muted); margin: 0 0 4px; line-height: 1.3; }
  ul.parts { list-style: none; margin: 0; padding: 0; }
  ul.parts label {
    display: grid; grid-template-columns: auto auto 1fr; align-items: start; gap: 8px;
    padding: 4px 4px; border-radius: 5px; cursor: pointer;
  }
  ul.parts label:hover { background: #f2f4f7; }
  ul.parts input { margin: 2px 0 0; width: 15px; height: 15px; }
  .sw { width: 15px; height: 15px; border-radius: 3px; border: 1px solid rgba(0, 0, 0, .28); margin-top: 2px; }
  .nm small { display: block; color: var(--muted); font-size: 11.5px; line-height: 1.3; }
  .note { font-size: 12px; color: var(--muted); margin: 10px 0 0; }
  footer {
    background: var(--panel); border-top: 1px solid var(--line);
    padding: 6px 16px; font-size: 11px; color: var(--muted);
  }
  @media (min-width: 761px) {
    body { height: 100vh; height: 100dvh; overflow: hidden; }
  }
  @media (max-width: 760px) {
    header { padding: 8px 12px; }
    h1 { font-size: 16px; }
    .app { grid-template-columns: minmax(0, 1fr); grid-template-rows: auto auto; }
    .toolbar { padding: 6px 8px; }
    .toolbar button { padding: 6px 10px; }
    .sep { display: none; }
    .view { flex: none; height: 62vh; height: 62svh; min-height: 280px; }
    .side { border-left: 0; border-top: 1px solid var(--line); overflow: visible; }
    footer { padding: 6px 12px; }
  }
</style>
</head>
<body>
<header><h1>Датчик ДК-3С-210АВ — 3D-модель</h1></header>
<main class="app">
  <section class="stage">
    <div class="toolbar" role="toolbar" aria-label="Виды">
      <button type="button" data-view="iso" title="Взгляд из направления (−1, −1, 1), как на изометрии чертежа">Изометрия</button>
      <button type="button" data-view="front" title="Главный вид чертежа — взгляд из −Y">Спереди</button>
      <button type="button" data-view="top" title="Взгляд сверху, из +Z">Сверху</button>
      <button type="button" data-view="reset" title="Вид, масштаб, вырез и детали — как при открытии страницы">Сброс</button>
      <span class="sep" aria-hidden="true"></span>
      <label class="toggle" title="Корпусные детали — с вырезанной четвертью"><input type="checkbox" id="cut" checked> Вырез четверти</label>
    </div>
    <div class="view" id="view">
      <div class="status" id="status">Загрузка библиотеки three.js…</div>
      <div class="hint" id="hint" hidden>
        <span class="mouse">Левая кнопка мыши — вращение · колесо — масштаб · правая кнопка — сдвиг · двойной щелчок — центр вращения в эту точку</span>
        <span class="touch">Один палец — вращение · два пальца — масштаб и сдвиг</span>
      </div>
    </div>
  </section>
  <aside class="side">
    <h2>Детали <button type="button" id="all">Показать все</button></h2>
    <div id="parts"></div>
    <p class="note">Цвета: светло-серый — сталь 08Х18Н10Т; тёмно-серый — сталь 65Г; слоновая кость — фторопласт;
      контакты выводов — цвета токоотводов по ТТ п. 6 чертежа (с тёмным контуром); остальные цвета условные.
      Плоскости разреза чуть темнее.</p>
    <p class="note">Вырез рассекает гильзу, корпус, втулку, грундбуксу, гровер и гайку; трубки, мостики и скобу
      не рассекает (ГОСТ 2.305).</p>
  </aside>
</main>
<footer>Модель: dk3s_cad/tools/iso/sensor_model.py (__VERSION__). Внутри гильзы трубки показаны условно. Файл собран __BUILT__.</footer>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@__THREE_VER__/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@__THREE_VER__/examples/jsm/"
  }
}
</script>
<script type="application/json" id="dk3s-data">__DATA__</script>
<script type="module">
const statusEl = document.getElementById('status');
function showStatus(text, isError) {
  statusEl.textContent = text;
  statusEl.classList.toggle('err', !!isError);
  statusEl.hidden = false;
}
function why(e) { return e && e.message ? e.message : String(e); }

function b64buf(s) {
  const bin = atob(s);
  const n = bin.length;
  const u8 = new Uint8Array(n);
  for (let i = 0; i < n; i++) u8[i] = bin.charCodeAt(i);
  return u8.buffer;
}

async function main() {
  let THREE, OrbitControls;
  try {
    THREE = await import('three');
    ({ OrbitControls } = await import('three/addons/controls/OrbitControls.js'));
  } catch (e) {
    showStatus('Не удалось загрузить библиотеку three.js с cdn.jsdelivr.net. При открытии страницы нужен интернет ' +
      'и современный браузер (Chrome, Edge, Firefox или Safari не старше 2023 г.). Причина: ' + why(e), true);
    return;
  }
  showStatus('Построение модели…');
  await new Promise((r) => setTimeout(r, 0));

  const data = JSON.parse(document.getElementById('dk3s-data').textContent);
  const view = document.getElementById('view');
  const cutBox = document.getElementById('cut');

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch (e) {
    showStatus('Браузер не смог включить 3D-графику (WebGL). Попробуйте другой браузер или включите аппаратное ' +
      'ускорение. Причина: ' + why(e), true);
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  view.insertBefore(renderer.domElement, view.firstChild);

  // сцена: ось датчика — X, вертикаль — Z (как на чертеже), мм
  const UP = new THREE.Vector3(0, 0, 1);
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 20000);
  camera.up.copy(UP);
  scene.add(camera);
  const hemi = new THREE.HemisphereLight(0xffffff, 0x9ea6b0, 1.7);
  hemi.position.set(0, 0, 1);
  scene.add(hemi);
  // свет «от наблюдателя» (привязан к камере): слева сверху и слабый справа
  const key = new THREE.DirectionalLight(0xffffff, 2.1);
  key.position.set(-0.7, 0.9, 1.2);
  key.target.position.set(0, 0, -1);
  camera.add(key, key.target);
  const fill = new THREE.DirectionalLight(0xffffff, 0.55);
  fill.position.set(0.9, -0.5, 0.8);
  fill.target.position.set(0, 0, -1);
  camera.add(fill, fill.target);

  const KIND = {
    steel: { roughness: 0.45, metalness: 0.15 },
    metal: { roughness: 0.35, metalness: 0.3 },
    ptfe: { roughness: 0.8, metalness: 0.0 },
    other: { roughness: 0.6, metalness: 0.05 },
    contact: { roughness: 0.45, metalness: 0.0 },
  };
  const edgeMat = new THREE.LineBasicMaterial({ color: 0x1f252c, transparent: true, opacity: 0.55 });
  // тёмный контур силуэта постоянной толщины в пикселях (обратные грани, раздутые по нормали в экранной
  // плоскости) — у контактов выводов: белый штырь ЭС2 виден и на светлом фоне
  const outlineMat = new THREE.ShaderMaterial({
    uniforms: { uColor: { value: new THREE.Color(0x15191e) }, uWidth: { value: 1.6 }, uRes: { value: new THREE.Vector2(1, 1) } },
    vertexShader: [
      'uniform float uWidth;',
      'uniform vec2 uRes;',
      'void main() {',
      '  vec4 clip = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
      '  vec2 n = (normalMatrix * normal).xy;',
      '  float l = length(n);',
      '  if (l > 1e-5) clip.xy += n / l * uWidth * 2.0 / uRes * clip.w;',
      '  gl_Position = clip;',
      '}',
    ].join('\n'),
    fragmentShader: 'uniform vec3 uColor;\nvoid main() { gl_FragColor = vec4(uColor, 1.0); }',
    side: THREE.BackSide,
  });

  function buildMesh(g, mats, outline) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(b64buf(g.pos)), 3));
    const idx = g.i32 ? new Uint32Array(b64buf(g.idx)) : new Uint16Array(b64buf(g.idx));
    geo.setIndex(new THREE.BufferAttribute(idx, 1));
    geo.computeVertexNormals();          // вершины общие только внутри грани: гладко в грани, остро на рёбрах
    geo.addGroup(0, g.sec, 0);
    if (g.sec < idx.length) geo.addGroup(g.sec, idx.length - g.sec, 1);   // грани сечения
    geo.computeBoundingSphere();
    const mesh = new THREE.Mesh(geo, mats);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo, data.edgeAngle), edgeMat);
    edges.raycast = () => {};
    mesh.add(edges);
    if (outline) {
      const hull = new THREE.Mesh(geo, outlineMat);
      hull.raycast = () => {};
      mesh.add(hull);
    }
    scene.add(mesh);
    return mesh;
  }

  // детали и список с флажками
  const parts = [];
  const box = document.getElementById('parts');
  data.groups.forEach((gname, gi) => {
    const h = document.createElement('div');
    h.className = 'grp';
    h.textContent = gname;
    const ul = document.createElement('ul');
    ul.className = 'parts';
    box.append(h);
    if (data.groupNotes && data.groupNotes[gi]) {
      const note = document.createElement('p');
      note.className = 'grp-note';
      note.textContent = data.groupNotes[gi];
      box.append(note);
    }
    box.append(ul);
    for (const p of data.parts.filter((q) => q.group === gi)) {
      const base = new THREE.Color(p.color);
      const k = KIND[p.kind] || KIND.other;
      const m0 = new THREE.MeshStandardMaterial({ color: base, roughness: k.roughness, metalness: k.metalness,
        polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
      const m1 = m0.clone();
      m1.color = base.clone().multiplyScalar(0.84);
      const ol = p.kind === 'contact';
      const rec = { key: p.key, name: p.name, full: buildMesh(p.full, [m0, m1], ol), cut: p.cut ? buildMesh(p.cut, [m0, m1], ol) : null };
      const li = document.createElement('li');
      const lab = document.createElement('label');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = true;
      cb.dataset.key = p.key;
      const sw = document.createElement('span');
      sw.className = 'sw';
      sw.style.background = p.color;
      const nm = document.createElement('span');
      nm.className = 'nm';
      nm.textContent = p.name;
      if (p.note) {
        const sm = document.createElement('small');
        sm.textContent = p.note;
        nm.appendChild(sm);
      }
      lab.append(cb, sw, nm);
      li.appendChild(lab);
      ul.appendChild(li);
      cb.addEventListener('change', applyVisibility);
      rec.input = cb;
      parts.push(rec);
    }
  });

  function applyVisibility() {
    const cutOn = cutBox.checked;
    for (const p of parts) {
      const on = p.input.checked;
      if (p.cut) {
        p.full.visible = on && !cutOn;
        p.cut.visible = on && cutOn;
      } else {
        p.full.visible = on;
      }
    }
    renderNow();
  }
  function visibleMeshes() {
    const out = [];
    for (const p of parts) for (const m of [p.full, p.cut]) if (m && m.visible) out.push(m);
    return out;
  }

  // камера и управление: ЛКМ — вращение, колесо — масштаб, ПКМ — сдвиг; касания — встроено в OrbitControls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.12;
  controls.screenSpacePanning = true;
  controls.zoomToCursor = true;
  controls.minZoom = 0.2;
  controls.maxZoom = 80;

  const CAM_DIST = 2000;
  let half = 100;                        // половина высоты кадра при zoom = 1, мм
  const aspect = () => Math.max(1, view.clientWidth) / Math.max(1, view.clientHeight);
  function updateFrustum() {
    const a = aspect();
    camera.left = -half * a;
    camera.right = half * a;
    camera.top = half;
    camera.bottom = -half;
    camera.updateProjectionMatrix();
  }

  const VIEWS = {
    iso: new THREE.Vector3(-1, -1, 1),      // как изометрия чертежа (sensor_iso_fc.py)
    front: new THREE.Vector3(0, -1, 0),     // главный вид — из -Y
    top: new THREE.Vector3(0, -0.001, 1),   // из +Z; малый наклон держит ось X вправо, +Y вверх экрана
  };
  // вид из направления dir (от объекта к наблюдателю): кадр по видимым деталям.
  // Пока пользователь не тронул камеру, кадр пересчитывается при каждом изменении размера области просмотра
  // (вкладка ещё раскладывается, поворот телефона, изменение окна); после вращения/масштаба/сдвига — нет.
  let autoFit = true;
  let lastDir = VIEWS.iso;
  function setView(dir) {
    lastDir = dir;
    autoFit = true;
    if (!view.clientWidth || !view.clientHeight) return;     // размера ещё нет — кадр сделает resize()
    // погасить инерцию вращения/сдвига: иначе её остаток довернёт камеру после нажатия кнопки вида
    controls.enableDamping = false;
    controls.update();
    controls.enableDamping = true;
    const d = dir.clone().normalize();
    const f = d.clone().negate();
    const right = new THREE.Vector3().crossVectors(f, UP).normalize();
    const upv = new THREE.Vector3().crossVectors(right, f).normalize();
    let meshes = visibleMeshes();
    if (!meshes.length) meshes = parts.map((p) => p.full);
    let u0 = Infinity, u1 = -Infinity, v0 = Infinity, v1 = -Infinity, w0 = Infinity, w1 = -Infinity;
    for (const mesh of meshes) {
      const a = mesh.geometry.attributes.position.array;
      for (let i = 0; i < a.length; i += 3) {
        const x = a[i], y = a[i + 1], z = a[i + 2];
        const u = x * right.x + y * right.y + z * right.z;
        const v = x * upv.x + y * upv.y + z * upv.z;
        const w = x * d.x + y * d.y + z * d.z;
        if (u < u0) u0 = u;
        if (u > u1) u1 = u;
        if (v < v0) v0 = v;
        if (v > v1) v1 = v;
        if (w < w0) w0 = w;
        if (w > w1) w1 = w;
      }
    }
    const target = new THREE.Vector3()
      .addScaledVector(right, (u0 + u1) / 2)
      .addScaledVector(upv, (v0 + v1) / 2)
      .addScaledVector(d, (w0 + w1) / 2);
    half = Math.max((v1 - v0) / 2, (u1 - u0) / (2 * aspect())) * 1.08 + 1;
    camera.zoom = 1;
    updateFrustum();
    controls.target.copy(target);
    camera.position.copy(target).addScaledVector(d, CAM_DIST);
    camera.lookAt(target);
    controls.update();
    renderNow();
  }

  // отрисовка по требованию: при движении мыши/касаний и затухании инерции
  let pending = false;
  function frame() {
    pending = false;
    const moving = controls.update();
    renderer.render(scene, camera);
    if (moving) requestRender();
  }
  function requestRender() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(frame);
    }
  }
  function renderNow() { renderer.render(scene, camera); }
  controls.addEventListener('change', requestRender);

  function resize() {
    const w = view.clientWidth, h = view.clientHeight;
    if (!w || !h) return;
    // плотность пикселей — заново при каждом изменении (масштаб Windows, перенос окна на другой монитор)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);    // размер холста на экране задаёт CSS (absolute, 100 %) — без обратной связи
    outlineMat.uniforms.uRes.value.set(w, h);   // толщина контура — в CSS-пикселях
    if (autoFit) {
      setView(lastDir);
      return;
    }
    updateFrustum();                  // вертикальный масштаб сохраняется, ширина кадра — по новой пропорции
    renderNow();
  }
  controls.addEventListener('start', () => { autoFit = false; });
  new ResizeObserver(resize).observe(view);

  // двойной щелчок — центр вращения в точку детали под курсором
  const raycaster = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  renderer.domElement.addEventListener('dblclick', (ev) => {
    const r = renderer.domElement.getBoundingClientRect();
    ndc.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
    const hit = raycaster.intersectObjects(visibleMeshes(), false)[0];
    if (!hit) return;
    const delta = hit.point.clone().sub(controls.target);
    controls.target.add(delta);
    camera.position.add(delta);
    autoFit = false;
    controls.update();
    renderNow();
  });

  cutBox.addEventListener('change', applyVisibility);
  document.getElementById('all').addEventListener('click', () => {
    for (const p of parts) p.input.checked = true;
    applyVisibility();
  });
  document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => {
    const v = b.dataset.view;
    if (v === 'reset') {
      cutBox.checked = true;
      for (const p of parts) p.input.checked = true;
      applyVisibility();
      setView(VIEWS.iso);
    } else {
      setView(VIEWS[v]);
    }
  }));

  applyVisibility();
  resize();                             // первый кадр — изометрия по всей модели (или при первом ненулевом размере)
  statusEl.hidden = true;
  document.getElementById('hint').hidden = false;
  // для проверки из консоли браузера
  window.dk3s = { THREE, scene, camera, controls, renderer, parts, setView, VIEWS, renderNow,
    state: () => ({ autoFit, half }), data: { triangles: data.triangles, version: data.version } };
}

main().catch((e) => {
  console.error(e);
  showStatus('Ошибка при построении модели: ' + why(e), true);
});
</script>
</body>
</html>
"""

# freecadcmd исполняет файл не как __main__ — вызов безусловный (как в sensor_iso_fc.py)
main()
