"""
Block Diagram — Power Supply Circuit for Transmitters
DEEPAK K1 — GP Plant, India  |  421457.103E1

Style: matching K1 Technical Description Fig.5 (clean B&W technical drawing)

Shows voltage drop chain:
  SCADA Ekor Box (24VDC) ──Cable 9 (250m)──> Connection Box
                                                ├── Cable 3 (15m) ──> Transmitter №1
                                                └── Cable 4 (15m) ──> Transmitter №2
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Расчётные данные (паспортное: 8 Вт / 24 В = 0.35 А) ─────────
rho_20 = 0.0175
alpha_cu = 0.00393
temp = 65  # worst case

rho_t = rho_20 * (1 + alpha_cu * (temp - 20))

I_tx = 0.350       # А — паспортное потребление одного трансмиттера
I_cab9 = 2 * I_tx  # А — суммарный ток в Cable 9

R9_one = rho_t * 250 / 1.5
R3_one = rho_t * 15 / 1.5

dU_cab9 = 2 * R9_one * I_cab9
dU_cab3 = 2 * R3_one * I_tx

V_source = 24.0
V_connbox = V_source - dU_cab9
V_T1 = V_connbox - dU_cab3
V_T2 = V_connbox - dU_cab3

P_cab9 = dU_cab9 * I_cab9
P_cab3 = dU_cab3 * I_tx

# ── Matplotlib setup ─────────────────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(22, 16))
ax.set_xlim(-1.5, 22.5)
ax.set_ylim(-2.5, 17)
ax.set_aspect('equal')
ax.axis('off')

# Шрифты в стиле документации
font_title = {'family': 'serif', 'weight': 'bold', 'size': 15}
font_block = {'family': 'serif', 'weight': 'bold', 'size': 11}
font_label = {'family': 'serif', 'size': 9}
font_value = {'family': 'monospace', 'weight': 'bold', 'size': 10}
font_small = {'family': 'serif', 'size': 8}
font_cable = {'family': 'monospace', 'weight': 'bold', 'size': 9}

# ── Цвета ────────────────────────────────────────────────────────
C_BG = '#FFFFFF'
C_BLOCK = '#FFFFFF'
C_LINE = '#000000'
C_ZONE = '#666666'
C_CABLE = '#333333'
C_WARN = '#CC0000'
C_OK = '#006600'
C_ACCENT = '#0055AA'

fig.patch.set_facecolor(C_BG)


# ═══════════════════════════════════════════════════════════════════
# ЗАГОЛОВОК (вынесен над зонами)
# ═══════════════════════════════════════════════════════════════════
ax.text(10.5, 16.3,
        'Block Diagram \u2014 Power Supply Circuit for Transmitters',
        fontdict={'family': 'serif', 'weight': 'bold', 'size': 16},
        ha='center', va='bottom')
ax.text(10.5, 15.9,
        'DEEPAK K1 \u2014 GP Plant, India  |  421457.103E1  |  '
        f'Worst case: {temp}\u00b0C',
        fontdict={'family': 'serif', 'size': 10, 'style': 'italic'},
        ha='center', va='top')


# ═══════════════════════════════════════════════════════════════════
# ЗОНЫ (пунктирные границы — как на Fig.5)
# ═══════════════════════════════════════════════════════════════════

# Зона 1: Central Control Room
zone1 = mpatches.FancyBboxPatch(
    (0, 5.5), 5.8, 9.5, boxstyle="round,pad=0.3",
    linewidth=1.5, edgecolor=C_ZONE, facecolor='#FAFAFA',
    linestyle=(0, (8, 4)))
ax.add_patch(zone1)
ax.text(2.9, 15.2, 'Central Control Room',
        fontdict={**font_label, 'style': 'italic'},
        ha='center', va='center', color=C_ZONE,
        bbox=dict(boxstyle='square,pad=0.15', facecolor='#FAFAFA',
                  edgecolor='none'))

# Зона 2: Technological area
zone2 = mpatches.FancyBboxPatch(
    (8.5, 3.0), 5.8, 12.0, boxstyle="round,pad=0.3",
    linewidth=1.5, edgecolor=C_ZONE, facecolor='#FAFAFA',
    linestyle=(0, (8, 4)))
ax.add_patch(zone2)
ax.text(11.4, 15.2, 'Technological Area',
        fontdict={**font_label, 'style': 'italic'},
        ha='center', va='center', color=C_ZONE,
        bbox=dict(boxstyle='square,pad=0.15', facecolor='#FAFAFA',
                  edgecolor='none'))

# Зона 3: Process area
zone3 = mpatches.FancyBboxPatch(
    (15.8, 1.5), 5.5, 13.5, boxstyle="round,pad=0.3",
    linewidth=1.5, edgecolor=C_ZONE, facecolor='#FAFAFA',
    linestyle=(0, (8, 4)))
ax.add_patch(zone3)
ax.text(18.55, 15.2, 'Process Area',
        fontdict={**font_label, 'style': 'italic'},
        ha='center', va='center', color=C_ZONE,
        bbox=dict(boxstyle='square,pad=0.15', facecolor='#FAFAFA',
                  edgecolor='none'))


# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def draw_block(x, y, w, h, line1, line2='', bold=False):
    lw = 2.5 if bold else 1.5
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        linewidth=lw, edgecolor=C_LINE, facecolor=C_BLOCK, zorder=3)
    ax.add_patch(rect)
    if line2:
        ax.text(x + w/2, y + h/2 + 0.3, line1,
                fontdict=font_block, ha='center', va='center', zorder=4)
        ax.text(x + w/2, y + h/2 - 0.3, line2,
                fontdict=font_small, ha='center', va='center', zorder=4)
    else:
        ax.text(x + w/2, y + h/2, line1,
                fontdict=font_block, ha='center', va='center', zorder=4)


def draw_voltage(x, y, voltage, warn=False):
    color = C_WARN if warn else C_OK
    bg = '#FFEBEE' if warn else '#E8F5E9'
    rect = mpatches.FancyBboxPatch(
        (x - 1.15, y - 0.3), 2.3, 0.6, boxstyle="round,pad=0.08",
        linewidth=1.5, edgecolor=color, facecolor=bg, zorder=5)
    ax.add_patch(rect)
    ax.text(x, y, f'{voltage:.2f} V', fontdict=font_value,
            ha='center', va='center', color=color, zorder=6)


def draw_cable_box(x, y, num, params):
    rect = mpatches.FancyBboxPatch(
        (x - 0.5, y - 0.25), 1.0, 0.5, boxstyle="square,pad=0",
        linewidth=1.5, edgecolor=C_LINE, facecolor='#FFFFFF', zorder=5)
    ax.add_patch(rect)
    ax.text(x, y, str(num), fontdict=font_cable,
            ha='center', va='center', zorder=6)
    ax.text(x, y - 0.55, params,
            fontdict=font_small, ha='center', va='top', color=C_CABLE,
            zorder=6)


# ═══════════════════════════════════════════════════════════════════
# БЛОКИ ОБОРУДОВАНИЯ
# ═══════════════════════════════════════════════════════════════════

# ── AC Mains input ──
ax.text(2.9, 14.3, 'AC Mains', fontdict=font_label, ha='center', va='bottom')
ax.text(2.9, 13.85, '100\u2013240 VAC, 50/60 Hz', fontdict=font_small,
        ha='center', va='bottom')
ax.annotate('', xy=(2.9, 13.0), xytext=(2.9, 13.75),
            arrowprops=dict(arrowstyle='->', color=C_LINE, lw=1.5))

# ── SCADA Ekor Box ──
draw_block(0.8, 10.0, 4.2, 3.0,
           'SCADA Ekor Box', 'Power Supply 24 VDC', bold=True)
draw_voltage(2.9, 9.4, V_source, warn=False)

# ── Connection Box ──
draw_block(9.2, 9.5, 4.2, 3.0,
           'Connection Box', '(Junction)')
draw_voltage(11.3, 9.0, V_connbox, warn=(V_connbox < 20))

# ── Transmitter №1 (upper branch) ──
draw_block(16.5, 11.5, 4.0, 2.5,
           'Transmitter \u21161', 'Ekor (8 W)', bold=True)
draw_voltage(18.5, 11.0, V_T1, warn=(V_T1 < 20))

# ── Transmitter №2 (lower branch) ──
draw_block(16.5, 4.5, 4.0, 2.5,
           'Transmitter \u21162', 'Ekor (8 W)', bold=True)
draw_voltage(18.5, 4.0, V_T2, warn=(V_T2 < 20))

# ── Sensor №1 ──
draw_block(17.1, 14.2, 2.8, 0.9, 'Sensor DK-3S')
ax.plot([18.5, 18.5], [14.0, 14.2], color=C_LINE, lw=1, ls='--', zorder=3)

# ── Sensor №2 ──
draw_block(17.1, 2.2, 2.8, 0.9, 'Sensor DK-3S')
ax.plot([18.5, 18.5], [3.1, 4.5], color=C_LINE, lw=1, ls='--', zorder=3)


# ═══════════════════════════════════════════════════════════════════
# CABLE 9: SCADA → Connection Box (250 m, 1.5 mm²)
# ═══════════════════════════════════════════════════════════════════

# Две параллельные линии (+ и -)
y_p = 12.2   # + провод
y_n = 10.8   # - провод
ax.plot([5.0, 9.2], [y_p, y_p], color=C_LINE, lw=2, zorder=3)
ax.plot([5.0, 9.2], [y_n, y_n], color=C_LINE, lw=2, zorder=3)

# + / - обозначения
ax.text(5.15, y_p + 0.15, '+', fontdict=font_cable, va='bottom', zorder=4)
ax.text(5.15, y_n - 0.15, '\u2013', fontdict=font_cable, va='top', zorder=4)

# Стрелка тока
ax.annotate('', xy=(8.8, 12.55), xytext=(5.8, 12.55),
            arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.8),
            zorder=4)
ax.text(7.3, 12.85, f'I = {I_cab9*1000:.0f} mA',
        fontdict={**font_value, 'size': 11},
        ha='center', va='bottom', color=C_ACCENT, zorder=4)

# Маркировка кабеля в рамке
draw_cable_box(7.1, 11.5, 9, '250 m, 1.5 mm\u00b2')

# Падение напряжения (выделяется)
ax.text(7.1, 10.35, f'\u0394U = {dU_cab9:.2f} V',
        fontdict={**font_value, 'size': 11},
        ha='center', va='top', color=C_WARN, zorder=4,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3E0',
                  edgecolor=C_WARN, linewidth=1.2))
ax.text(7.1, 9.7, f'P = {P_cab9:.2f} W',
        fontdict={**font_small, 'weight': 'bold'},
        ha='center', va='top', color=C_WARN, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# CABLE 3: Connection Box → Transmitter №1 (15 m)
# ═══════════════════════════════════════════════════════════════════

# Вертикальный отвод вверх из Connection Box + горизонтально к TX1
y3_p = 12.4
y3_n = 11.7
# Вверх из ConnBox
ax.plot([13.4, 13.4], [12.5, y3_p], color=C_LINE, lw=1.5, zorder=3)
ax.plot([12.6, 12.6], [12.5, y3_n], color=C_LINE, lw=1.5, zorder=3)
# Горизонтально
ax.plot([13.4, 16.5], [y3_p, y3_p], color=C_LINE, lw=1.5, zorder=3)
ax.plot([12.6, 16.5], [y3_n, y3_n], color=C_LINE, lw=1.5, zorder=3)

draw_cable_box(14.9, 12.8, 3, '15 m, 1.5 mm\u00b2')

# Стрелка тока
ax.annotate('', xy=(16.2, 12.65), xytext=(14.0, 12.65),
            arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.2),
            zorder=4)
ax.text(15.6, 13.35, f'I = {I_tx*1000:.0f} mA',
        fontdict={**font_small, 'weight': 'bold'},
        ha='center', va='bottom', color=C_ACCENT, zorder=4)

# Падение
ax.text(14.9, 11.4, f'\u0394U = {dU_cab3:.2f} V',
        fontdict={**font_small, 'weight': 'bold'},
        ha='center', va='top', color='#BB6600', zorder=4)


# ═══════════════════════════════════════════════════════════════════
# CABLE 4: Connection Box → Transmitter №2 (15 m)
# ═══════════════════════════════════════════════════════════════════

y4_p = 6.0
y4_n = 5.3
# Вниз из ConnBox
ax.plot([13.4, 13.4], [9.5, y4_p], color=C_LINE, lw=1.5, zorder=3)
ax.plot([12.6, 12.6], [9.5, y4_n], color=C_LINE, lw=1.5, zorder=3)
# Горизонтально
ax.plot([13.4, 16.5], [y4_p, y4_p], color=C_LINE, lw=1.5, zorder=3)
ax.plot([12.6, 16.5], [y4_n, y4_n], color=C_LINE, lw=1.5, zorder=3)

draw_cable_box(14.9, 5.65, 4, '15 m, 1.5 mm\u00b2')

ax.annotate('', xy=(16.2, 6.25), xytext=(14.0, 6.25),
            arrowprops=dict(arrowstyle='->', color=C_ACCENT, lw=1.2),
            zorder=4)
ax.text(15.6, 6.55, f'I = {I_tx*1000:.0f} mA',
        fontdict={**font_small, 'weight': 'bold'},
        ha='center', va='bottom', color=C_ACCENT, zorder=4)

ax.text(14.9, 4.55, f'\u0394U = {dU_cab3:.2f} V',
        fontdict={**font_small, 'weight': 'bold'},
        ha='center', va='top', color='#BB6600', zorder=4)


# ═══════════════════════════════════════════════════════════════════
# СИГНАЛЬНЫЕ ЛИНИИ 4-20 mA (пунктиром, как на Fig.5)
# ═══════════════════════════════════════════════════════════════════

# TX1 → SCADA
ax.annotate('', xy=(5.0, 13.6), xytext=(16.5, 13.6),
            arrowprops=dict(arrowstyle='<-', color=C_LINE, lw=0.8,
                           linestyle=(0, (6, 3))), zorder=3)
ax.text(10.5, 13.8, '4\u201320 mA  (QS1, QS2)', fontdict=font_small,
        ha='center', va='bottom', color=C_CABLE, zorder=4)

# TX2 → SCADA
ax.annotate('', xy=(5.0, 7.5), xytext=(16.5, 7.5),
            arrowprops=dict(arrowstyle='<-', color=C_LINE, lw=0.8,
                           linestyle=(0, (6, 3))), zorder=3)
ax.text(10.5, 7.7, '4\u201320 mA  (QS1, QS2)', fontdict=font_small,
        ha='center', va='bottom', color=C_CABLE, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# RS-485 bus (дополнительно — штрихпунктир)
# ═══════════════════════════════════════════════════════════════════

ax.plot([5.0, 16.5], [8.2, 8.2], color=C_LINE, lw=0.8,
        ls=(0, (4, 2, 1, 2)), zorder=3)
ax.text(10.5, 8.35, 'RS-485  (A, B)', fontdict=font_small,
        ha='center', va='bottom', color=C_CABLE, zorder=4)


# ═══════════════════════════════════════════════════════════════════
# ТАБЛИЦА ИТОГОВ (штамп внизу)
# ═══════════════════════════════════════════════════════════════════

stamp_x = -0.5
stamp_y = -2.3
stamp_w = 22.0
stamp_h = 3.2

rect_stamp = mpatches.Rectangle(
    (stamp_x, stamp_y), stamp_w, stamp_h,
    linewidth=2, edgecolor=C_LINE, facecolor='#FAFAFA', zorder=3)
ax.add_patch(rect_stamp)

# Горизонтальные линии
for dy in [2.4, 1.6, 0.8]:
    ax.plot([stamp_x, stamp_x + stamp_w],
            [stamp_y + dy, stamp_y + dy],
            color=C_LINE, lw=0.8, zorder=4)

# Вертикальные разделители
col_xs = [5.5, 9.5, 13.5, 17.0]
for cx in col_xs:
    ax.plot([cx, cx], [stamp_y, stamp_y + stamp_h - 0.8],
            color=C_LINE, lw=0.8, zorder=4)

# Заголовок штампа
ax.text(stamp_x + stamp_w/2, stamp_y + 2.75,
        f'VOLTAGE DROP SUMMARY  \u2014  Worst case: {temp}\u00b0C,  '
        f'I = {I_tx*1000:.0f} mA / transmitter  (8 W per passport)',
        fontdict={**font_block, 'size': 10}, ha='center', va='center',
        zorder=5)

# Заголовки столбцов
headers = ['Parameter', '\u0394U, V', 'V at point, V', 'P loss, W', 'Status']
hx = [2.5, 7.5, 11.5, 15.25, 19.0]
for h, x in zip(headers, hx):
    ax.text(x, stamp_y + 1.95, h,
            fontdict={**font_small, 'weight': 'bold'},
            ha='center', va='center', zorder=5)

# Cable 9
row1 = [f'Cable 9  (250 m, 1.5 mm\u00b2)',
        f'{dU_cab9:.2f}',
        f'{V_connbox:.2f}',
        f'{P_cab9:.2f}',
        '\u26a0 High drop' if dU_cab9 > 3 else 'OK']
for val, x in zip(row1, hx):
    c = C_WARN if '\u26a0' in str(val) else C_LINE
    ax.text(x, stamp_y + 1.15, val, fontdict=font_value,
            ha='center', va='center', color=c, zorder=5)

# Cable 3/4
row2 = [f'Cable 3/4  (15 m, 1.5 mm\u00b2)',
        f'{dU_cab3:.2f}',
        f'{V_T1:.2f}',
        f'{P_cab3:.3f}',
        '\u26a0 < 20 V' if V_T1 < 20 else 'OK']
for val, x in zip(row2, hx):
    c = C_WARN if '\u26a0' in str(val) else C_LINE
    ax.text(x, stamp_y + 0.35, val, fontdict=font_value,
            ha='center', va='center', color=c, zorder=5)


# ═══════════════════════════════════════════════════════════════════
# ПРИМЕЧАНИЕ (справа от штампа или под)
# ═══════════════════════════════════════════════════════════════════

note = (f'Note: Transmitter supply range 18\u201330 V (abs), '
        f'recommended \u2265 20 V.\n'
        f'Cable 9 at 1.5 mm\u00b2 × 250 m causes {dU_cab9:.1f} V drop '
        f'({dU_cab9/24*100:.0f}%) \u2014 consider 2.5 mm\u00b2.')
ax.text(stamp_x + stamp_w/2, stamp_y - 0.2, note,
        fontdict={'family': 'serif', 'size': 9, 'style': 'italic'},
        ha='center', va='top', color='#444444', zorder=5)


# ── Save ──────────────────────────────────────────────────────────
out_path = '/home/user/46clod/K1_power_supply_diagram.png'
plt.savefig(out_path, dpi=180, bbox_inches='tight',
            facecolor=C_BG, edgecolor='none', pad_inches=0.4)
plt.close()
print(f'Saved: {out_path}')
