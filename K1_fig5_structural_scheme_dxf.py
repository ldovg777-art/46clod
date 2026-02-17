"""
Fig.5 — Structural scheme of the system — DXF (AutoCAD) format
DEEPAK K1 — GP Plant, India  |  421457.103E1

Generates K1_fig5_structural_scheme.dxf
Opens in: AutoCAD, nanoCAD, BricsCAD, LibreCAD, QCAD, etc.
"""
import ezdxf
from ezdxf.enums import TextEntityAlignment

doc = ezdxf.new('R2010')
doc.header['$INSUNITS'] = 4  # mm

# ── Layers ────────────────────────────────────────────────────
doc.layers.new('ZONES', dxfattribs={'color': 8})
doc.layers.new('BLOCKS', dxfattribs={'color': 7})
doc.layers.new('WIRES', dxfattribs={'color': 7})
doc.layers.new('TEXT', dxfattribs={'color': 7})
doc.layers.new('WIRE_NUM', dxfattribs={'color': 7})
doc.layers.new('GND', dxfattribs={'color': 7})
doc.layers.new('TITLE', dxfattribs={'color': 7})

msp = doc.modelspace()

# Scale: 1 unit = 1 mm, drawing ~900 x 1300 mm
# Coordinates: origin at bottom-left, Y up


def box(x, y, w, h, layer='BLOCKS'):
    """Rectangle from bottom-left corner."""
    msp.add_lwpolyline(
        [(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)],
        close=True, dxfattribs={'layer': layer})


def txt(x, y, text, height=12, layer='TEXT', halign='center'):
    align = TextEntityAlignment.CENTER
    if halign == 'left':
        align = TextEntityAlignment.LEFT
    elif halign == 'right':
        align = TextEntityAlignment.RIGHT
    msp.add_text(text, height=height,
                 dxfattribs={'layer': layer}).set_placement(
                     (x, y), align=align)


def txt_bold(x, y, text, height=14, layer='TEXT'):
    # DXF doesn't have bold, use larger font
    txt(x, y, text, height=height, layer=layer)


def line(x1, y1, x2, y2, layer='WIRES'):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': layer})


def polyline(pts, layer='WIRES'):
    msp.add_lwpolyline(pts, dxfattribs={'layer': layer})


def wire_num(x, y, num, length=''):
    """Wire number in a small box."""
    bw, bh = 14, 10
    box(x - bw/2, y - bh/2, bw, bh, layer='WIRE_NUM')
    txt(x, y, str(num), height=8, layer='WIRE_NUM')
    if length:
        txt(x, y + bh/2 + 4, length, height=7, layer='WIRE_NUM')


def ground(x, y):
    """Ground symbol ⏚."""
    line(x, y-5, x, y+5, layer='GND')
    line(x+3, y-3.5, x+3, y+3.5, layer='GND')
    line(x+6, y-2, x+6, y+2, layer='GND')


# ═══════════════════════════════════════════════════════════════
# Coordinate system: Y goes UP, origin at bottom-left
# Total drawing area: 900 wide x 1300 tall
# ═══════════════════════════════════════════════════════════════

# ── TITLE ─────────────────────────────────────────────────────
txt(450, 1280, 'Fig.5  Structural scheme of the system', height=18,
    layer='TITLE')
txt(450, 1260, 'DEEPAK K1 - GP Plant, India  |  421457.103E1',
    height=10, layer='TITLE')

# ── ZONE 1: Technological area (dashed) ──────────────────────
# y: 620..1240
pts_z1 = [(20, 620), (880, 620), (880, 1240), (20, 1240), (20, 620)]
p = msp.add_lwpolyline(pts_z1, close=True,
                        dxfattribs={'layer': 'ZONES', 'linetype': 'DASHED'})
txt(60, 1225, 'Technological area', height=11, halign='left', layer='ZONES')

# ── ZONE 2: Central control room (dashed) ────────────────────
# y: 20..600
pts_z2 = [(20, 20), (880, 20), (880, 600), (20, 600), (20, 20)]
msp.add_lwpolyline(pts_z2, close=True,
                    dxfattribs={'layer': 'ZONES', 'linetype': 'DASHED'})
txt(60, 30, 'Central control room', height=11, halign='left', layer='ZONES')


# ═══════════════════════════════════════════════════════════════
# SENSORS (top of zone 1)
# ═══════════════════════════════════════════════════════════════

# S1 Sensor1
box(150, 1140, 180, 60)
txt_bold(240, 1170, 'S1  Sensor1')

# S2 Sensor2
box(570, 1140, 180, 60)
txt_bold(660, 1170, 'S2  Sensor2')


# ═══════════════════════════════════════════════════════════════
# TRANSMITTERS
# ═══════════════════════════════════════════════════════════════

# T1
box(150, 1020, 180, 70)
txt_bold(240, 1065, 'Transmitter')
txt_bold(240, 1040, 'T1')

# T2
box(570, 1020, 180, 70)
txt_bold(660, 1065, 'Transmitter')
txt_bold(660, 1040, 'T2')


# ═══════════════════════════════════════════════════════════════
# WIRE 1: S1 → T1 (15m)
# ═══════════════════════════════════════════════════════════════
line(240, 1140, 240, 1090)
wire_num(240, 1115, 1, '15m')

# WIRE 2: S2 → T2 (15m)
line(660, 1140, 660, 1090)
wire_num(660, 1115, 2, '15m')


# ═══════════════════════════════════════════════════════════════
# WIRE 7: T1 → ground (50m)
# ═══════════════════════════════════════════════════════════════
line(330, 1055, 410, 1055)
wire_num(370, 1055, 7, '50m')
ground(410, 1055)

# WIRE 8: T2 → ground (50m)
line(750, 1055, 830, 1055)
wire_num(790, 1055, 8, '50m')
ground(830, 1055)


# ═══════════════════════════════════════════════════════════════
# CONNECTION BOX
# ═══════════════════════════════════════════════════════════════
box(120, 780, 380, 200)
txt_bold(310, 960, 'Connection box')

# Divider
line(310, 800, 310, 945)

# POWER terminals
txt(215, 930, 'POWER', height=9)
txt(215, 912, '1  24VDC+', height=7)
txt(215, 898, '2  24VDC-', height=7)
txt(215, 884, '3  24VDC+', height=7)
txt(215, 870, '4  24VDC-', height=7)

# RS-485 terminals
txt(405, 930, 'RS-485', height=9)
txt(405, 912, '5  Data+', height=7)
txt(405, 898, '6  Data-', height=7)
txt(405, 884, '7  Data+', height=7)
txt(405, 870, '8  Data-', height=7)


# ═══════════════════════════════════════════════════════════════
# WIRE 3: Connection box → T1 (15m, 24VDC/RS485)
# ═══════════════════════════════════════════════════════════════
line(200, 980, 200, 1020)
wire_num(200, 1000, 3)
txt(165, 1005, '15m', height=7)
txt(145, 1015, '24VDC/', height=7)
txt(145, 1003, 'RS485', height=7)

# WIRE 4: Connection box → T2 (15m, 24VDC/RS485)
polyline([(500, 860), (540, 860), (600, 860), (600, 1020)])
wire_num(540, 860, 4, '15m')
txt(620, 940, '24VDC/', height=7)
txt(620, 928, 'RS485', height=7)


# ═══════════════════════════════════════════════════════════════
# WIRE 5: T1 → DCS (4-20mA, 200m)
# ═══════════════════════════════════════════════════════════════
line(275, 1020, 275, 620)
line(275, 600, 275, 440)
wire_num(275, 530, 5, '200m')
txt(295, 1000, '4-20mA', height=7, halign='left')

# WIRE 6: T2 → DCS (4-20mA, 200m)
polyline([(700, 1020), (700, 1005), (320, 1005), (320, 620)])
line(320, 600, 320, 440)
wire_num(320, 530, 6, '200m')
txt(510, 1012, '4-20mA', height=7)


# ═══════════════════════════════════════════════════════════════
# WIRE 9: Connection box → SCADA Ekor Box (250m)
# ═══════════════════════════════════════════════════════════════
polyline([(380, 780), (380, 620)])
polyline([(380, 600), (380, 460), (520, 460), (520, 430)])
wire_num(380, 530, 9, '250m')
txt(360, 490, '24VDC/RS485', height=7, halign='right')


# ═══════════════════════════════════════════════════════════════
# DCS TERMINAL BLOCK
# ═══════════════════════════════════════════════════════════════
box(80, 390, 380, 50)
terms = ['4-20mA', 'T1 Pot+', 'T1 Pot-', 'T1 pH+', 'T1 pH-',
         'T2 Pot+', 'T2 Pot-', 'T2 pH+', 'T2 pH-']
for i, t in enumerate(terms):
    tx = 110 + i * 38
    txt(tx, 415, t, height=5.5)


# ═══════════════════════════════════════════════════════════════
# DCS K-1 GP Plant
# ═══════════════════════════════════════════════════════════════
box(80, 250, 280, 100)
txt_bold(220, 315, 'DCS')
txt_bold(220, 290, 'K-1 GP Plant')

# Terminal → DCS
line(220, 390, 220, 350)

# 230VAC in
txt(385, 310, '230VAC', height=7)
txt(385, 295, '1.5A', height=7)


# ═══════════════════════════════════════════════════════════════
# SCADA EKOR BOX
# ═══════════════════════════════════════════════════════════════
box(500, 340, 200, 90)
txt_bold(600, 395, 'SCADA Ekor Box')
txt(600, 370, '24VDC output', height=9)


# ═══════════════════════════════════════════════════════════════
# Socket
# ═══════════════════════════════════════════════════════════════
box(510, 220, 110, 45)
txt(565, 242, 'Socket', height=9)

# WIRE 10: Socket → SCADA (100m, 230VAC)
line(565, 265, 565, 340)
wire_num(542, 300, 10)
txt(520, 310, '100m', height=7, halign='right')
txt(520, 295, '230VAC', height=7, halign='right')


# ═══════════════════════════════════════════════════════════════
# WIRE 11: SCADA → 24VDC (3m)
# ═══════════════════════════════════════════════════════════════
line(700, 385, 770, 385)
wire_num(735, 385, 11, '3m')
txt(780, 385, '24VDC', height=7, halign='left')


# ═══════════════════════════════════════════════════════════════
# OPERATOR PANEL
# ═══════════════════════════════════════════════════════════════
box(500, 140, 200, 70)
txt_bold(600, 185, 'Oper. panel')
txt(600, 160, '(display)', height=9)

# RS-485 from SCADA → Oper panel
line(600, 340, 600, 210)
txt(615, 275, 'RS485', height=7, halign='left')


# ═══════════════════════════════════════════════════════════════
# MOUSE
# ═══════════════════════════════════════════════════════════════
box(540, 55, 110, 40)
txt(595, 75, 'Mouse', height=9)
line(595, 140, 595, 95)


# ═══════════════════════════════════════════════════════════════
# LCD MONITOR
# ═══════════════════════════════════════════════════════════════
box(740, 250, 120, 70)
txt_bold(800, 298, 'LCD')
txt_bold(800, 275, 'Monitor')

# WIRE 12: Oper panel → LCD Monitor (3m, HDMI)
polyline([(700, 175), (800, 175), (800, 250)])
wire_num(800, 210, 12, '3m')
txt(760, 165, 'HDMI', height=7)


# ═══════════════════════════════════════════════════════════════
# WIRE LEGEND (bottom)
# ═══════════════════════════════════════════════════════════════
ly = 10
leg = [
    'Wires 1,2 - type 4x1.0 mm2 with shield (Ekor)',
    'Wires 5,6 - type 2pair x1.5 mm2 with shield (K-1 GP Plant)',
    'Wires 3,4,9 - type 2pair x1.5 mm2 twisted pair (K-1 GP Plant)',
    'Wires 7,8 - type 1Cx2.5 mm2 grounding wire YG (K-1 GP Plant)',
    'Wire 10 - 3Corex2.5 mm2 (K-1)   Wire 11 - 3x0.75 mm2 (Ekor)   Wire 12 - HDMI (Ekor)',
]
# Place legend below the drawing (negative Y)
for i, t in enumerate(leg):
    txt(30, -10 - i*12, t, height=7, halign='left')


# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
out = '/home/user/46clod/K1_fig5_structural_scheme.dxf'
doc.saveas(out)
print(f'Saved: {out}')
