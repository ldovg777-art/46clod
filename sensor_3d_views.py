"""
3D Model of Concentration Sensor DK-3S — Multiple views
Based on drawings from К1 Technical Description (Figs. 1, 4, 6-9)
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cylinder(r, z_start, z_end, n=60):
    theta = np.linspace(0, 2 * np.pi, n)
    z = np.linspace(z_start, z_end, 2)
    theta, z = np.meshgrid(theta, z)
    return r * np.cos(theta), r * np.sin(theta), z

def cone(r_base, r_tip, z_start, z_end, n=60):
    theta = np.linspace(0, 2 * np.pi, n)
    z = np.linspace(z_start, z_end, 30)
    theta, z = np.meshgrid(theta, z)
    t = (z - z_start) / (z_end - z_start)
    r = r_base + (r_tip - r_base) * t
    return r * np.cos(theta), r * np.sin(theta), z

def disk(r_inner, r_outer, z_pos, n=60):
    theta = np.linspace(0, 2 * np.pi, n)
    r = np.linspace(r_inner, r_outer, 2)
    theta, r = np.meshgrid(theta, r)
    return r * np.cos(theta), r * np.sin(theta), np.full_like(r * np.cos(theta), z_pos)


def draw_sensor(ax, show_labels=True):
    """Draw the complete DK-3S sensor on given axes."""
    alpha_body = 0.75

    # 1. Working electrode tip
    x, y, z = cone(0.7, 0.1, 0, 4, n=40)
    ax.plot_surface(x, y, z, color='#FFD700', alpha=0.95, shade=True)

    # 2. Protective sleeve
    x, y, z = cylinder(12.5, 4, 80)
    ax.plot_surface(x, y, z, color='#5F788A', alpha=alpha_body, shade=True)
    x, y, z = disk(0, 12.5, 4)
    ax.plot_surface(x, y, z, color='#4F6878', alpha=0.9, shade=True)
    x, y, z = disk(10, 12.5, 80)
    ax.plot_surface(x, y, z, color='#4F6878', alpha=0.5, shade=True)

    # 3. Shell (main body)
    x, y, z = cylinder(10, 80, 310)
    ax.plot_surface(x, y, z, color='#B0B0B0', alpha=alpha_body, shade=True)

    # 4. Electrolytic bridge
    offset_angle = np.pi / 4
    eb_cx = 10 * np.cos(offset_angle)
    eb_cy = 10 * np.sin(offset_angle)
    t = np.linspace(0, 2 * np.pi, 30)
    zz = np.linspace(30, 305, 2)
    t, zz = np.meshgrid(t, zz)
    ax.plot_surface(eb_cx + 2.5 * np.cos(t), eb_cy + 2.5 * np.sin(t), zz,
                    color='#CD9B1D', alpha=0.65, shade=True)

    # 5. Gland bush
    x, y, z = cylinder(15, 310, 340)
    ax.plot_surface(x, y, z, color='#707070', alpha=alpha_body, shade=True)
    x, y, z = disk(10, 15, 310)
    ax.plot_surface(x, y, z, color='#555555', alpha=0.85, shade=True)
    x, y, z = disk(10, 15, 340)
    ax.plot_surface(x, y, z, color='#555555', alpha=0.85, shade=True)

    # 6. Input unit (M42x3)
    x, y, z = cone(15, 21, 340, 360)
    ax.plot_surface(x, y, z, color='#888888', alpha=alpha_body, shade=True)
    x, y, z = cylinder(21, 360, 411)
    ax.plot_surface(x, y, z, color='#888888', alpha=alpha_body, shade=True)
    for zp in np.arange(365, 410, 4):
        x, y, z = cylinder(22, zp, zp + 1.5, n=40)
        ax.plot_surface(x, y, z, color='#666666', alpha=0.5, shade=True)
    x, y, z = disk(0, 21, 411)
    ax.plot_surface(x, y, z, color='#555555', alpha=0.7, shade=True)

    # 7. Electrode wires
    wire_len = 55
    colors_offsets = [
        ('red',    5,  0, 'WE'),
        ('blue',  -5,  0, 'RE'),
        ('black',  0,  5, 'SE'),
        ('#228B22', 0, -5, 'Shield'),
    ]
    for col, dx, dy, name in colors_offsets:
        x, y, z = cylinder(1.2, 411, 411 + wire_len, n=20)
        ax.plot_surface(x + dx, y + dy, z, color=col, alpha=0.9, shade=True)

    # 8. Tag
    tag_z = np.array([[200, 230], [200, 230]])
    tag_x = np.array([[-11.5, -11.5], [-11.5, -11.5]])
    tag_y = np.array([[-6, -6], [6, 6]])
    ax.plot_surface(tag_x, tag_y, tag_z, color='white', alpha=0.95, shade=True,
                    edgecolor='gray', linewidth=0.5)

    if show_labels:
        lp = dict(fontsize=7, color='#222222',
                  bbox=dict(boxstyle='round,pad=0.15', fc='#FFFFF0',
                            ec='#999999', alpha=0.85))
        # Use leader lines + text
        leaders = [
            (-25, -25, 2,   "Working electrode\nTip (φ1.4mm)"),
            (-25, -20, 50,  "Protective\nsleeve"),
            (20,  -20, 195, "Shell (body)"),
            (22,   18, 165, "Electrolytic\nbridge"),
            (-25, -18, 325, "Gland bush"),
            (30,  -25, 385, "Input unit\n(M42×3)"),
            (-15,  20, 215, "S/N tag"),
        ]
        for (x, y, z, txt) in leaders:
            ax.text(x, y, z, txt, **lp)

        # Wire labels at the top
        ax.text(12, -5, 455, "WE", fontsize=7, color='red', fontweight='bold')
        ax.text(-16, -5, 455, "RE", fontsize=7, color='blue', fontweight='bold')
        ax.text(-3, 12, 455, "SE", fontsize=7, color='black', fontweight='bold')
        ax.text(-3, -16, 455, "Sh", fontsize=7, color='green', fontweight='bold')


# ── Create figure with 3 views ────────────────────────────────────
fig = plt.figure(figsize=(20, 10))
fig.suptitle('3D Model — Concentration Sensor DK-3S\n'
             '(K1 Technical Description, Figs. 1, 4)',
             fontsize=15, fontweight='bold', y=0.98)

views = [
    (111, 15, -60,  "Perspective view"),
    (132, 0,   0,   "Front view"),
    (133, 90,  0,   "Top view"),
]

# View 1: Perspective (large)
ax1 = fig.add_subplot(1, 3, (1, 2), projection='3d')
draw_sensor(ax1, show_labels=True)
ax1.view_init(elev=15, azim=-60)
ax1.set_xlabel('X (mm)', fontsize=8)
ax1.set_ylabel('Y (mm)', fontsize=8)
ax1.set_zlabel('Length (mm)', fontsize=8)
ax1.set_xlim(-60, 60)
ax1.set_ylim(-60, 60)
ax1.set_zlim(-20, 480)
ax1.set_box_aspect([1, 1, 3.5])
ax1.set_title("Perspective view", fontsize=11, pad=5)

# View 2: Front
ax2 = fig.add_subplot(2, 3, 3, projection='3d')
draw_sensor(ax2, show_labels=False)
ax2.view_init(elev=0, azim=0)
ax2.set_xlim(-40, 40)
ax2.set_ylim(-40, 40)
ax2.set_zlim(-20, 480)
ax2.set_box_aspect([1, 1, 4])
ax2.set_title("Front view", fontsize=10, pad=3)
ax2.tick_params(labelsize=6)

# View 3: Isometric from top
ax3 = fig.add_subplot(2, 3, 6, projection='3d')
draw_sensor(ax3, show_labels=False)
ax3.view_init(elev=25, azim=30)
ax3.set_xlim(-40, 40)
ax3.set_ylim(-40, 40)
ax3.set_zlim(-20, 480)
ax3.set_box_aspect([1, 1, 4])
ax3.set_title("Isometric view", fontsize=10, pad=3)
ax3.tick_params(labelsize=6)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/home/user/46clod/sensor_DK3S_3d_views.png', dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: sensor_DK3S_3d_views.png")
plt.close()
