"""
Block Diagram — Potentiostat System DK-3S
DEEPAK K1 — GP Plant, India  |  421457.103E1

Shows the complete signal flow:
  Sensor DK-3S (3 electrodes) → Spark protection QB →
  Potentiostat QT → Controller QI → RS-485 / 4-20mA → DCS

Style: matching K1 Technical Description Fig.5 (clean B&W technical drawing)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Matplotlib setup ─────────────────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(24, 18))
ax.set_xlim(-1, 25)
ax.set_ylim(-1.5, 18.5)
ax.set_aspect('equal')
ax.axis('off')

# ── Fonts ────────────────────────────────────────────────────────
FT = {'family': 'serif', 'weight': 'bold', 'size': 16}
FB = {'family': 'serif', 'weight': 'bold', 'size': 11}
FL = {'family': 'serif', 'size': 9}
FS = {'family': 'serif', 'size': 8}
FM = {'family': 'monospace', 'weight': 'bold', 'size': 10}
FC = {'family': 'monospace', 'weight': 'bold', 'size': 9}

# ── Colors ───────────────────────────────────────────────────────
BG = '#FFFFFF'
BLK = '#000000'
ZN = '#666666'
ACC = '#0055AA'
RED = '#CC0000'
GRN = '#006600'
fig.patch.set_facecolor(BG)


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

def box(x, y, w, h, line1, line2='', line3='', bold=False, fill='#FFFFFF',
        ec=BLK):
    lw = 2.5 if bold else 1.5
    r = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        linewidth=lw, edgecolor=ec, facecolor=fill, zorder=3)
    ax.add_patch(r)
    lines = [l for l in (line1, line2, line3) if l]
    n = len(lines)
    for i, l in enumerate(lines):
        yy = y + h/2 + (n-1)*0.22 - i*0.44
        f = FB if i == 0 else FS
        ax.text(x + w/2, yy, l, fontdict=f, ha='center', va='center',
                zorder=4)


def zone(x, y, w, h, label):
    z = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.3",
        linewidth=1.5, edgecolor=ZN, facecolor='#FAFAFA',
        linestyle=(0, (8, 4)))
    ax.add_patch(z)
    ax.text(x + w/2, y + h + 0.05, label,
            fontdict={**FL, 'style': 'italic'},
            ha='center', va='bottom', color=ZN,
            bbox=dict(boxstyle='square,pad=0.15', facecolor='#FAFAFA',
                      edgecolor='none'))


def arrow(x1, y1, x2, y2, style='->', color=BLK, lw=1.5, ls='-'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls), zorder=3)


def wire(pts, color=BLK, lw=1.5, ls='-'):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=3)


def label(x, y, txt, f=FS, color=BLK, ha='center', va='center',
          bg=None, bec=None):
    kw = dict(fontdict=f, ha=ha, va=va, color=color, zorder=5)
    if bg:
        kw['bbox'] = dict(boxstyle='round,pad=0.2', facecolor=bg,
                          edgecolor=bec or color, linewidth=1)
    ax.text(x, y, txt, **kw)


def signal_label(x, y, name, desc=''):
    ax.text(x, y, name, fontdict={**FC, 'size': 8},
            ha='center', va='bottom', color=ACC, zorder=5)
    if desc:
        ax.text(x, y - 0.18, desc, fontdict={**FS, 'size': 7},
                ha='center', va='top', color='#555', zorder=5)


# ═══════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════

ax.text(12, 18.0,
        'Block Diagram \u2014 Potentiostat Measurement System DK-3S',
        fontdict=FT, ha='center', va='bottom')
ax.text(12, 17.6,
        'DEEPAK K1 \u2014 GP Plant, India  |  421457.103E1  |  '
        'Three-electrode potentiostatic method',
        fontdict={**FL, 'size': 10, 'style': 'italic'},
        ha='center', va='top')


# ═══════════════════════════════════════════════════════════════════
# ZONES
# ═══════════════════════════════════════════════════════════════════

# Zone: Process apparatus
zone(0, 0, 6.5, 16.8, 'Process Apparatus')

# Zone: Sensor assembly
zone(7.5, 2.5, 4.5, 14.3, 'Sensor Assembly (Ex zone)')

# Zone: Transmitter cabinet
zone(13.0, 2.5, 5.5, 14.3, 'Transmitter Cabinet')

# Zone: DCS / Operator
zone(19.5, 4.0, 4.8, 12.8, 'DCS / Operator Room')


# ═══════════════════════════════════════════════════════════════════
# PROCESS APPARATUS — Three electrodes
# ═══════════════════════════════════════════════════════════════════

# Working electrode
box(1.0, 13.5, 4.5, 2.2,
    'Working Electrode (WE)',
    'Wire \u00d81.4 mm, gold tip',
    'Reaction: H\u207a/OH\u207b \u2192 gas',
    bold=True)

# Reference electrode
box(1.0, 9.0, 4.5, 2.2,
    'Reference Electrode (RE)',
    'Ag/AgCl + electrolytic bridge',
    'Stable potential reference')

# Subsidiary electrode (wall)
box(1.0, 4.5, 4.5, 2.2,
    'Subsidiary Electrode (SE)',
    'Apparatus wall (steel)',
    'Current-carrying electrode')

# Solution
box(1.5, 1.0, 3.5, 2.3,
    'NH\u2084NO\u2083 Solution',
    'H\u207a, OH\u207b, NH\u2084\u207a, NO\u2083\u207b',
    fill='#F5F5F0')

# Ionic current arrows (solution → WE)
arrow(3.25, 3.3, 3.25, 4.5, color='#888', lw=1, ls='--')
label(4.3, 3.9, 'ionic\ncurrent', f={**FS, 'size': 7}, color='#888')

# Connect solution to electrodes
wire([(3.25, 3.3), (3.25, 4.5)], color='#999', lw=1, ls='--')
wire([(2.0, 3.3), (2.0, 4.5)], color='#999', lw=1, ls='--')
wire([(4.5, 3.3), (4.5, 9.0)], color='#999', lw=1, ls='--')


# ═══════════════════════════════════════════════════════════════════
# SENSOR ASSEMBLY — Spark protection
# ═══════════════════════════════════════════════════════════════════

# Spark protection QB1 (for WE signal)
box(8.0, 13.5, 3.5, 2.2,
    'Spark Protection',
    'QB (WE circuit)',
    'Ex barrier')

# Spark protection QB2 (for RE signal)
box(8.0, 9.0, 3.5, 2.2,
    'Spark Protection',
    'QB (RE circuit)',
    'Ex barrier')

# Spark protection QB3 (for SE circuit)
box(8.0, 4.5, 3.5, 2.2,
    'Spark Protection',
    'QB (SE circuit)',
    'Ex barrier')

# Wires: Electrodes → Spark protection
wire([(5.5, 14.6), (8.0, 14.6)], lw=2)
label(6.75, 14.9, 'WE wire', f={**FS, 'size': 7}, color=ACC)

wire([(5.5, 10.1), (8.0, 10.1)], lw=2)
label(6.75, 10.4, 'RE wire', f={**FS, 'size': 7}, color=ACC)

wire([(5.5, 5.6), (8.0, 5.6)], lw=2)
label(6.75, 5.9, 'SE wire', f={**FS, 'size': 7}, color=ACC)


# ═══════════════════════════════════════════════════════════════════
# TRANSMITTER CABINET
# ═══════════════════════════════════════════════════════════════════

# Potentiostat QT
box(13.5, 13.0, 4.5, 3.3,
    'Potentiostat QT',
    'Maintains E = const (WE\u2013RE)',
    'Measures I through WE',
    bold=True, fill='#F0F5FF')

# Controller QI
box(13.5, 8.5, 4.5, 3.0,
    'Controller QI',
    'I \u2192 Concentration \u2192 pH',
    'RS-485 + "Mission" signal')

# Signal converter QS1 (potential → 4-20mA)
box(13.5, 5.5, 4.5, 2.0,
    'Converter QS1',
    'E (0\u20132V) \u2192 4\u201320 mA')

# Signal converter QS2 (concentration → 4-20mA)
box(13.5, 3.0, 4.5, 2.0,
    'Converter QS2',
    'Conc (0\u20132V) \u2192 4\u201320 mA')


# ═══════════════════════════════════════════════════════════════════
# WIRES: Spark protection → Transmitter cabinet
# ═══════════════════════════════════════════════════════════════════

# WE → Potentiostat (top wire)
wire([(11.5, 14.6), (13.5, 14.6)], lw=2)
signal_label(12.5, 14.85, 'I(WE)')

# RE signal 1 → Potentiostat (goes up from QB to QT)
wire([(11.5, 10.5), (12.5, 10.5), (12.5, 14.0), (13.5, 14.0)], lw=2)
label(13.1, 12.7, 'RE1', f={**FC, 'size': 8}, color=ACC, ha='right')

# RE signal 2 → QS1 (dashed, separate path for DCS)
wire([(11.5, 9.5), (12.9, 9.5), (12.9, 6.5), (13.5, 6.5)], lw=1.5,
     ls=(0, (6, 3)))
label(13.1, 8.2, 'RE2', f={**FC, 'size': 8}, color=ACC, ha='right')

# SE → Potentiostat (current path, goes up)
wire([(11.5, 5.6), (12.1, 5.6), (12.1, 13.4), (13.5, 13.4)], lw=2)
label(11.7, 9.5, 'SE', f={**FC, 'size': 8}, color=ACC, ha='right')


# ═══════════════════════════════════════════════════════════════════
# INTERNAL CONNECTIONS IN TRANSMITTER CABINET
# ═══════════════════════════════════════════════════════════════════

# QT → QI: measured current (converted to voltage)
arrow(15.3, 13.0, 15.3, 11.5, color=ACC, lw=1.5)
label(14.7, 12.2, 'I\u2192U', f={**FC, 'size': 8}, color=ACC, ha='center')

# QI → QT: "Mission" (target potential)
arrow(16.8, 11.5, 16.8, 13.0, color=RED, lw=1.5)
label(17.5, 12.2, '"Mission"', f={**FC, 'size': 8}, color=RED, ha='center')

# QI → QS2: concentration analog
arrow(15.75, 8.5, 15.75, 5.0, color=ACC, lw=1.2)
label(14.7, 7.0, 'Conc', f={**FC, 'size': 8}, color=ACC, ha='center')


# ═══════════════════════════════════════════════════════════════════
# DCS / OPERATOR ROOM
# ═══════════════════════════════════════════════════════════════════

# Operator panel
box(20.0, 13.0, 3.8, 3.0,
    'Operator Panel',
    'RS-485 display',
    'E, I, pH, Conc, alarms',
    fill='#F5FFF5')

# DCS input QS1
box(20.0, 9.5, 3.8, 2.0,
    'DCS Input',
    'QS1: 4\u201320mA \u2192 E(mV)')

# DCS input QS2
box(20.0, 5.0, 3.8, 2.0,
    'DCS Input',
    'QS2: 4\u201320mA \u2192 Conc(%)')

# RS-485 bus: QI → Operator
wire([(18.0, 10.0), (19.2, 10.0), (19.2, 14.5), (20.0, 14.5)], lw=1.5,
     ls=(0, (4, 2, 1, 2)))
label(19.5, 13.0, 'RS-485', f={**FC, 'size': 7}, color='#555', ha='left')

# QS1 → DCS (4-20mA)
wire([(18.0, 6.5), (20.0, 10.5)], lw=1.5, ls=(0, (6, 3)))
label(19.3, 8.8, '4\u201320mA', f={**FC, 'size': 7}, color='#555', ha='left')

# QS2 → DCS (4-20mA)
wire([(18.0, 4.0), (20.0, 6.0)], lw=1.5, ls=(0, (6, 3)))
label(19.3, 5.2, '4\u201320mA', f={**FC, 'size': 7}, color='#555', ha='left')


# ═══════════════════════════════════════════════════════════════════
# FEEDBACK LOOP ANNOTATION
# ═══════════════════════════════════════════════════════════════════

# Annotation above potentiostat
fb_x, fb_y = 15.75, 16.6
label(fb_x, fb_y,
      'POTENTIOSTAT FEEDBACK LOOP',
      f={**FB, 'size': 10}, color=RED)
label(fb_x, fb_y - 0.42,
      'QT compares E(WE\u2013RE) with "Mission" setpoint from QI',
      f={**FS, 'size': 8}, color='#555')
label(fb_x, fb_y - 0.78,
      'Adjusts current through SE \u2192 solution \u2192 WE to maintain E = const',
      f={**FS, 'size': 8}, color='#555')

# Feedback arrow loop (visual arc)
from matplotlib.patches import FancyArrowPatch
loop = FancyArrowPatch(
    (18.3, 13.2), (18.3, 11.3),
    connectionstyle="arc3,rad=-0.5",
    arrowstyle='->', mutation_scale=15,
    color=RED, lw=2, linestyle='--', zorder=4)
ax.add_patch(loop)


# ═══════════════════════════════════════════════════════════════════
# LEGEND / NOTES at bottom
# ═══════════════════════════════════════════════════════════════════

note_y = -0.3
ax.plot([0, 24], [note_y + 0.7, note_y + 0.7], color=BLK, lw=1.5)

# Line types legend
lx = 0.5
label(lx, note_y, 'Signal types:', f={**FB, 'size': 9}, ha='left')
ax.plot([lx + 3.0, lx + 4.5], [note_y, note_y], color=BLK, lw=2)
label(lx + 5.0, note_y, '\u2014 Power / current circuit', f=FS, ha='left')

ax.plot([lx + 10.0, lx + 11.5], [note_y, note_y], color=BLK, lw=1.5,
        ls=(0, (6, 3)))
label(lx + 12.0, note_y, '\u2014 Analog signal (4\u201320 mA, 0\u20132 V)',
      f=FS, ha='left')

ax.plot([lx + 19.5, lx + 21.0], [note_y, note_y], color=BLK, lw=1.5,
        ls=(0, (4, 2, 1, 2)))
label(lx + 21.5, note_y, '\u2014 Digital (RS-485)', f=FS, ha='left')

# Measurement principle
note2_y = note_y - 0.6
label(0.5, note2_y,
      'Measurement principle:  Potentiostat maintains constant potential '
      'E between WE and RE.  Current I(WE) \u221d concentration of '
      'H\u207a (acid excess) or OH\u207b (ammonia excess).',
      f={**FS, 'size': 8, 'style': 'italic'}, ha='left', color='#444')

note3_y = note2_y - 0.4
label(0.5, note3_y,
      'Acid mode: 2H\u207a + 2e\u207b \u2192 H\u2082\u2191 (cathode)   |   '
      'Ammonia mode: 2OH\u207b \u2212 2e\u207b \u2192 O\u2082\u2191 + '
      'H\u2082O (anode)   |   '
      'Neutral: E \u2248 +600 mV   |   '
      'Range: +400 mV (NH\u2083 max) \u2026 +900 mV (HNO\u2083 max)',
      f={**FS, 'size': 8, 'style': 'italic'}, ha='left', color='#444')


# ── Save ──────────────────────────────────────────────────────────
out = '/home/user/46clod/K1_potentiostat_diagram.png'
plt.savefig(out, dpi=180, bbox_inches='tight',
            facecolor=BG, edgecolor='none', pad_inches=0.4)
plt.close()
print(f'Saved: {out}')
