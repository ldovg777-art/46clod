"""
Fig.5 — Structural scheme of the system (exact copy from K1 documentation)
DEEPAK K1 — GP Plant, India  |  421457.103E1
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(22, 30))
ax.set_xlim(-1, 23)
ax.set_ylim(-4, 30)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

BK = '#000000'
FB = {'family': 'sans-serif', 'weight': 'bold', 'size': 11}
FL = {'family': 'sans-serif', 'size': 9}
FS = {'family': 'sans-serif', 'size': 8}
FT = {'family': 'sans-serif', 'size': 7}
FTB = {'family': 'sans-serif', 'weight': 'bold', 'size': 7}


def box(x, y, w, h):
    r = mpatches.Rectangle((x, y), w, h, linewidth=1.5,
                            edgecolor=BK, facecolor='#FFF', zorder=3)
    ax.add_patch(r)


def txt(x, y, s, f=FL, **kw):
    ax.text(x, y, s, fontdict=f, ha=kw.get('ha', 'center'),
            va=kw.get('va', 'center'), zorder=kw.get('z', 4),
            rotation=kw.get('rot', 0))


def line(pts, lw=1.2):
    ax.plot([p[0] for p in pts], [p[1] for p in pts],
            color=BK, lw=lw, zorder=2)


def wn(x, y, num, length=''):
    """Wire number in a small box."""
    r = mpatches.Rectangle((x-0.3, y-0.22), 0.6, 0.44,
                            linewidth=1, edgecolor=BK, facecolor='#FFF',
                            zorder=5)
    ax.add_patch(r)
    txt(x, y, str(num), f=FTB, z=6)
    if length:
        txt(x, y+0.5, length, f=FT)


# ═══════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════
txt(11, 29.5, 'Fig.5  Structural scheme of the system',
    f={'family': 'sans-serif', 'weight': 'bold', 'size': 14})

# ═══════════════════════════════════════════════════════════════
# ZONE 1: Technological area
# ═══════════════════════════════════════════════════════════════
z = mpatches.Rectangle((0.5, 15), 21, 13.5, linewidth=1.5,
                        edgecolor=BK, facecolor='none',
                        linestyle=(0, (8, 4)), zorder=1)
ax.add_patch(z)
txt(1.5, 28.2, 'Technological area', f=FL, ha='left')

# ═══════════════════════════════════════════════════════════════
# SENSORS
# ═══════════════════════════════════════════════════════════════
box(3.5, 26.0, 4.0, 1.5)
txt(5.5, 26.75, 'S1  Sensor1', f=FB)

box(14.0, 26.0, 4.0, 1.5)
txt(16.0, 26.75, 'S2  Sensor2', f=FB)

# ═══════════════════════════════════════════════════════════════
# TRANSMITTERS
# ═══════════════════════════════════════════════════════════════
box(3.5, 22.5, 4.0, 1.8)
txt(5.5, 23.7, 'Transmitter', f=FB)
txt(5.5, 23.15, 'T1', f=FB)

box(14.0, 22.5, 4.0, 1.8)
txt(16.0, 23.7, 'Transmitter', f=FB)
txt(16.0, 23.15, 'T2', f=FB)

# Wire 1: S1 → T1
line([(5.5, 26.0), (5.5, 24.3)])
wn(5.5, 25.2, 1, '15m')

# Wire 2: S2 → T2
line([(16.0, 26.0), (16.0, 24.3)])
wn(16.0, 25.2, 2, '15m')

# Wire 7: T1 → ground (right) with ground symbol
line([(7.5, 23.4), (9.0, 23.4)])
wn(8.3, 23.4, 7)
txt(8.3, 22.8, '50m', f=FT)
# Ground symbol ⏚
gx, gy = 9.0, 23.4
line([(gx, gy-0.3), (gx, gy+0.3)], lw=1.5)
line([(gx+0.15, gy-0.2), (gx+0.15, gy+0.2)], lw=1.2)
line([(gx+0.3, gy-0.1), (gx+0.3, gy+0.1)], lw=0.8)

# Wire 8: T2 → ground (right) with ground symbol
line([(18.0, 23.4), (19.5, 23.4)])
wn(18.8, 23.4, 8)
txt(18.8, 22.8, '50m', f=FT)
gx2, gy2 = 19.5, 23.4
line([(gx2, gy2-0.3), (gx2, gy2+0.3)], lw=1.5)
line([(gx2+0.15, gy2-0.2), (gx2+0.15, gy2+0.2)], lw=1.2)
line([(gx2+0.3, gy2-0.1), (gx2+0.3, gy2+0.1)], lw=0.8)


# ═══════════════════════════════════════════════════════════════
# CONNECTION BOX
# ═══════════════════════════════════════════════════════════════
box(4.0, 16.5, 8.5, 4.5)
txt(8.25, 20.5, 'Connection box', f=FB)

# Terminal labels POWER
txt(5.5, 19.8, 'POWER', f=FTB)
txt(5.5, 19.35, '1  24VDC+', f=FT)
txt(5.5, 18.95, '2  24VDC\u2013', f=FT)
txt(5.5, 18.55, '3  24VDC+', f=FT)
txt(5.5, 18.15, '4  24VDC\u2013', f=FT)

# Terminal labels RS-485
txt(8.5, 19.8, 'RS-485', f=FTB)
txt(8.5, 19.35, '5  Data+', f=FT)
txt(8.5, 18.95, '6  Data\u2013', f=FT)
txt(8.5, 18.55, '7  Data+', f=FT)
txt(8.5, 18.15, '8  Data\u2013', f=FT)

# Vertical line inside connection box separating POWER from RS-485
line([(7.0, 17.8), (7.0, 20.0)], lw=0.8)


# ═══════════════════════════════════════════════════════════════
# WIRES: T1/T2 ↔ Connection box
# ═══════════════════════════════════════════════════════════════

# Wire 3: Connection box → T1 (24VDC + RS485)
line([(5.0, 21.0), (5.0, 22.5)])
wn(5.0, 21.75, 3)
txt(4.0, 21.75, '15m', f=FT)
txt(3.5, 22.2, '24VDC/', f=FT, ha='center')
txt(3.5, 21.85, 'RS485', f=FT, ha='center')

# Wire 4: Connection box → T2 (24VDC + RS485)
line([(12.5, 18.5), (13.5, 18.5), (15.0, 18.5), (15.0, 22.5)])
wn(14.0, 18.5, 4)
txt(14.0, 17.9, '15m', f=FT)
txt(15.6, 20.5, '24VDC/', f=FT, ha='center')
txt(15.6, 20.15, 'RS485', f=FT, ha='center')

# Wire 5: T1 → DCS (4-20mA, 200m) — goes straight down
line([(6.5, 22.5), (6.5, 15.0)])
txt(7.2, 21.5, '4-20mA', f=FT, ha='left')
line([(6.5, 14.0), (6.5, 11.0)])
wn(6.5, 13.0, 5, '200m')

# Wire 6: T2 → DCS (4-20mA, 200m) — goes down, routes left to DCS
line([(17.0, 22.5), (17.0, 21.0), (7.5, 21.0), (7.5, 15.0)])
txt(12.0, 21.3, '4-20mA', f=FT)
line([(7.5, 14.0), (7.5, 11.0)])
wn(7.5, 13.0, 6, '200m')


# ═══════════════════════════════════════════════════════════════
# ZONE 2: Central control room
# ═══════════════════════════════════════════════════════════════
z2 = mpatches.Rectangle((0.5, -1.5), 21, 15.5, linewidth=1.5,
                         edgecolor=BK, facecolor='none',
                         linestyle=(0, (8, 4)), zorder=1)
ax.add_patch(z2)
txt(1.5, -1.2, 'Central control room', f=FL, ha='left')

# Wire 9: Connection box → SCADA Ekor Box (250m, 24VDC + RS485)
line([(8.0, 16.5), (8.0, 15.0)])
line([(8.0, 14.0), (8.0, 10.0), (12.5, 10.0)])
wn(8.0, 12.5, 9, '250m')
txt(7.0, 11.5, '24VDC/', f=FT)
txt(7.0, 11.15, 'RS485', f=FT)


# ═══════════════════════════════════════════════════════════════
# DCS TERMINAL BLOCK
# ═══════════════════════════════════════════════════════════════
box(3.0, 9.5, 9.0, 1.5)
terms = ['4-20mA', 'T1 Pot+', 'T1 Pot\u2013', 'T1 pH+', 'T1 pH\u2013',
         'T2 Pot+', 'T2 Pot\u2013', 'T2 pH+', 'T2 pH\u2013']
for i, t in enumerate(terms):
    tx = 3.5 + i * 0.95
    txt(tx, 10.25, t, f={**FT, 'size': 5.5}, rot=90)

# DCS box
box(3.0, 6.0, 6.0, 2.5)
txt(6.0, 7.65, 'DCS', f=FB)
txt(6.0, 7.0, 'K-1 GP Plant', f=FB)

# Terminal → DCS
line([(7.0, 9.5), (7.0, 8.5)])

# 230VAC in
txt(9.5, 7.5, '230VAC', f=FT)
txt(9.5, 7.1, '1.5A', f=FT)
line([(9.0, 7.3), (9.5, 7.3)], lw=0.8)


# ═══════════════════════════════════════════════════════════════
# SCADA EKOR BOX
# ═══════════════════════════════════════════════════════════════
box(12.5, 7.5, 4.5, 2.5)
txt(14.75, 9.1, 'SCADA Ekor Box', f=FB)
txt(14.75, 8.4, '24VDC output', f=FS)

# Socket → SCADA
box(12.5, 5.0, 2.5, 1.2)
txt(13.75, 5.6, 'Socket', f=FS)
line([(13.75, 6.2), (13.75, 7.5)])
wn(13.0, 6.85, 10)
txt(12.0, 6.85, '100m', f=FT)
txt(12.0, 6.45, '230VAC', f=FT)

# Wire 11: SCADA → 24VDC (3m)
line([(17.0, 8.5), (18.5, 8.5)])
wn(17.75, 8.5, 11)
txt(17.75, 9.1, '3m', f=FT)
txt(18.8, 8.5, '24VDC', f=FT, ha='left')


# ═══════════════════════════════════════════════════════════════
# OPERATOR PANEL
# ═══════════════════════════════════════════════════════════════
box(12.5, 2.5, 4.5, 2.0)
txt(14.75, 3.85, 'Oper. panel', f=FB)
txt(14.75, 3.2, '(display)', f=FS)

# RS-485 from SCADA → Oper
line([(14.75, 7.5), (14.75, 4.5)])
txt(15.3, 6.0, 'RS485', f=FT, ha='left')

# Mouse
box(13.0, 0.5, 2.5, 1.0)
txt(14.25, 1.0, 'Mouse', f=FS)
line([(14.25, 2.5), (14.25, 1.5)])


# ═══════════════════════════════════════════════════════════════
# LCD MONITOR
# ═══════════════════════════════════════════════════════════════
box(18.0, 5.5, 3.0, 2.0)
txt(19.5, 6.85, 'LCD', f=FB)
txt(19.5, 6.25, 'Monitor', f=FB)

# Wire 12: Oper panel → LCD Monitor (3m, HDMI)
line([(17.0, 3.5), (19.5, 3.5), (19.5, 5.5)])
wn(19.5, 4.5, 12, '3m')
txt(18.0, 3.8, 'HDMI', f=FT)


# ═══════════════════════════════════════════════════════════════
# WIRE LEGEND
# ═══════════════════════════════════════════════════════════════
ly = -2.0
leg = [
    'Wires 1,2 \u2013 type 4\u00d71.0 mm\u00b2 with shield (Ekor)',
    'Wires 5,6 \u2013 type 2pair\u00d71.5 mm\u00b2 with shield (K-1 GP Plant)',
    'Wires 3,4,9 \u2013 type 2pair\u00d71.5 mm\u00b2 twisted pair (K-1 GP Plant)',
    'Wires 7,8 \u2013 type 1C\u00d72.5 mm\u00b2 grounding wire YG (K-1 GP Plant)',
    'Wire 10 \u2013 type 3Core\u00d72.5 mm\u00b2 (K-1 GP Plant)',
    'Wire 11 \u2013 type 3\u00d70.75 mm\u00b2 (Ekor)',
    'Wire 12 \u2013 type HDMI (Ekor)',
]
for i, t in enumerate(leg):
    txt(1.0, ly - i*0.45, t, f=FT, ha='left')


# ── Save ─────────────────────────────────────────────────────
out = '/home/user/46clod/K1_fig5_structural_scheme.png'
plt.savefig(out, dpi=180, bbox_inches='tight',
            facecolor='#FFF', edgecolor='none', pad_inches=0.3)
plt.close()
print(f'Saved: {out}')
