"""
3D Model of Concentration Sensor DK-3S
Based on drawings from К1 Technical Description (Figs. 1, 4, 6-9)
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

# ── Helper: generate cylinder surface ──────────────────────────────
def cylinder(r, z_start, z_end, n=60):
    """Return X, Y, Z mesh for a cylinder along the Z-axis."""
    theta = np.linspace(0, 2 * np.pi, n)
    z = np.linspace(z_start, z_end, 2)
    theta, z = np.meshgrid(theta, z)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, z

def cone(r_base, r_tip, z_start, z_end, n=60):
    """Return X, Y, Z mesh for a truncated cone along Z-axis."""
    theta = np.linspace(0, 2 * np.pi, n)
    z = np.linspace(z_start, z_end, 30)
    theta, z = np.meshgrid(theta, z)
    t = (z - z_start) / (z_end - z_start)
    r = r_base + (r_tip - r_base) * t
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, z

def disk(r_inner, r_outer, z_pos, n=60):
    """Return X, Y, Z mesh for an annular disk at z_pos."""
    theta = np.linspace(0, 2 * np.pi, n)
    r = np.linspace(r_inner, r_outer, 2)
    theta, r = np.meshgrid(theta, r)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.full_like(x, z_pos)
    return x, y, z

# ── Sensor dimensions (mm, based on drawings) ─────────────────────
# Total sensor length ~411 mm
# Shell outer diameter ~20 mm (fits inside DN50 pipe)
# Protective sleeve outer diameter ~24 mm
# Gland bush diameter ~30 mm
# Input unit (cable end) ~42 mm (M42x3 thread)

fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(111, projection='3d')

alpha_body = 0.7

# ── 1. Working electrode tip (leftmost) ───────────────────────────
# Small conical tip, φ1.4mm wire protruding 2mm
x, y, z = cone(0.7, 0.1, 0, 4, n=40)
ax.plot_surface(x, y, z, color='gold', alpha=0.95, shade=True)

# ── 2. Protective sleeve (covers working electrode area) ──────────
# Cylindrical sleeve, slightly larger diameter than shell
x, y, z = cylinder(12.5, 4, 80)
ax.plot_surface(x, y, z, color='#708090', alpha=alpha_body, shade=True)
# Sleeve end cap
x, y, z = disk(0, 12.5, 4)
ax.plot_surface(x, y, z, color='#607080', alpha=0.8, shade=True)
# Sleeve end cap (right)
x, y, z = disk(0, 12.5, 80)
ax.plot_surface(x, y, z, color='#607080', alpha=0.5, shade=True)

# ── 3. Shell (main body) ──────────────────────────────────────────
# Main cylindrical body of the sensor
x, y, z = cylinder(10, 80, 320)
ax.plot_surface(x, y, z, color='#A9A9A9', alpha=alpha_body, shade=True)

# ── 4. Electrolytic bridge (tube running along the body) ──────────
# Small tube on the outside of the shell
theta_offset = np.pi / 4  # position on the shell surface
eb_r = 2.5  # bridge tube radius
eb_cx = 10 * np.cos(theta_offset)
eb_cy = 10 * np.sin(theta_offset)
t = np.linspace(0, 2 * np.pi, 30)
zz = np.linspace(30, 310, 2)
t, zz = np.meshgrid(t, zz)
x_eb = eb_cx + eb_r * np.cos(t)
y_eb = eb_cy + eb_r * np.sin(t)
ax.plot_surface(x_eb, y_eb, zz, color='#B8860B', alpha=0.6, shade=True)

# ── 5. Gland bush (sealing area in the middle) ────────────────────
x, y, z = cylinder(15, 310, 340)
ax.plot_surface(x, y, z, color='#696969', alpha=alpha_body, shade=True)
# Gland bush flanges
x, y, z = disk(10, 15, 310)
ax.plot_surface(x, y, z, color='#505050', alpha=0.8, shade=True)
x, y, z = disk(10, 15, 340)
ax.plot_surface(x, y, z, color='#505050', alpha=0.8, shade=True)

# ── 6. Input unit / Cable entry (M42x3 threaded section) ──────────
# Wider section at the cable end
x, y, z = cone(15, 21, 340, 360)
ax.plot_surface(x, y, z, color='#808080', alpha=alpha_body, shade=True)
x, y, z = cylinder(21, 360, 411)
ax.plot_surface(x, y, z, color='#808080', alpha=alpha_body, shade=True)
# Thread grooves (decorative rings)
for zp in np.arange(365, 410, 4):
    x, y, z = cylinder(22, zp, zp + 1.5, n=40)
    ax.plot_surface(x, y, z, color='#606060', alpha=0.5, shade=True)
# End cap with cable holes
x, y, z = disk(0, 21, 411)
ax.plot_surface(x, y, z, color='#505050', alpha=0.7, shade=True)

# ── 7. Current taps (electrode wires coming out of cable end) ─────
# Working electrode wire (WE) - red
wire_len = 50
x, y, z = cylinder(1.2, 411, 411 + wire_len, n=20)
ax.plot_surface(x + 5, y, z, color='red', alpha=0.9, shade=True)

# Reference electrode wire (RE) - blue
x, y, z = cylinder(1.2, 411, 411 + wire_len, n=20)
ax.plot_surface(x - 5, y, z, color='blue', alpha=0.9, shade=True)

# Subsidiary electrode wire (SE) - black
x, y, z = cylinder(1.2, 411, 411 + wire_len, n=20)
ax.plot_surface(x, y + 5, z, color='black', alpha=0.9, shade=True)

# Shield wire - green
x, y, z = cylinder(1.2, 411, 411 + wire_len, n=20)
ax.plot_surface(x, y - 5, z, color='green', alpha=0.9, shade=True)

# ── 8. Tag with serial number ─────────────────────────────────────
# Small rectangular tag on the body
tag_z = np.array([[200, 230], [200, 230]])
tag_x = np.array([[-11, -11], [-11, -11]])
tag_y = np.array([[-6, -6], [6, 6]])
ax.plot_surface(tag_x, tag_y, tag_z, color='white', alpha=0.9, shade=True)
ax.text(-12, 0, 215, "S/N", fontsize=7, color='black', ha='center', va='center')

# ── Annotations ───────────────────────────────────────────────────
label_props = dict(fontsize=8, color='#333333',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow',
                             edgecolor='gray', alpha=0.8))

# Arrow-like annotations using text + lines
annotations = [
    (2, -18, 2, "Working electrode\nwith Tip (φ1.4mm)"),
    (16, -20, 50, "Protective sleeve"),
    (-14, -18, 200, "Shell (body)"),
    (16, 14, 170, "Electrolytic bridge"),
    (20, -18, 325, "Gland bush"),
    (28, -25, 385, "Input unit\n(M42×3)"),
    (10, -20, 445, "WE (red)"),
    (-10, -20, 445, "RE (blue)"),
    (5, 12, 445, "SE (black)"),
    (5, -15, 445, "Shield (green)"),
]
for (x, y, z, txt) in annotations:
    ax.text(x, y, z, txt, **label_props)

# ── Title and formatting ──────────────────────────────────────────
ax.set_title('3D Model — Concentration Sensor DK-3S\n'
             '(based on K1 Technical Description drawings)',
             fontsize=14, fontweight='bold', pad=20)

ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z — Length (mm)')

# Set viewing angle
ax.view_init(elev=15, azim=-60)

# Equal aspect ratio
max_range = 240
ax.set_xlim(-max_range/4, max_range/4)
ax.set_ylim(-max_range/4, max_range/4)
ax.set_zlim(-20, 480)

ax.set_box_aspect([1, 1, 3.5])

plt.tight_layout()
plt.savefig('/home/user/46clod/sensor_DK3S_3d.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: sensor_DK3S_3d.png")
plt.close()
