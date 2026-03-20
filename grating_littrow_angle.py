import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def littrow_angle(lines_per_mm, wavelength_nm, order=1):
    d = 1 / (lines_per_mm * 1e3)
    wavelength = wavelength_nm * 1e-9
    sin_theta = order * wavelength / (2 * d)

    if abs(sin_theta) > 1:
        raise ValueError("No physical solution (sin(theta) > 1)")

    return np.arcsin(sin_theta)

def plot_grating_orders(lines_per_mm, wavelength_nm):
    theta = littrow_angle(lines_per_mm, wavelength_nm, order=1)

    fig, ax = plt.subplots(figsize=(6, 6))

    # ✅ Grating region: y <= 0
    grating = Rectangle((-5, -5), 10, 5,
                        facecolor='lightblue', alpha=0.4,
                        edgecolor='blue')
    ax.add_patch(grating)

    # Grating grooves (only on surface region)
    for i in range(-10, 10):
        ax.plot([i * 0.4, i * 0.4], [-5, 0], color='black', linewidth=1)

    origin = np.array([0, 0])  # surface

    # Beam directions
    incident_dir = np.array([-np.sin(theta), -np.cos(theta)])
    zero_order_dir = np.array([-np.sin(theta), np.cos(theta)])
    first_order_dir = -incident_dir

    # Incident (coming from above → toward surface)
    ax.arrow(*(origin - incident_dir * 4), *(incident_dir * 4),
             head_width=0.2, color='blue', length_includes_head=True,
             label='Incident')

    # 0th order (reflection)
    ax.arrow(origin[0], origin[1],
             zero_order_dir[0]*4, zero_order_dir[1]*4,
             head_width=0.2, color='green', length_includes_head=True,
             label='0th Order')

    # 1st order (Littrow)
    ax.arrow(origin[0], origin[1],
             first_order_dir[0]*4, first_order_dir[1]*4,
             head_width=0.2, color='red', length_includes_head=True,
             label='1st Order (Littrow)')

    # Surface line (important visual cue)
    ax.axhline(0, color='blue', linewidth=2)

    # Normal
    ax.plot([0, 0], [-5, 5], '--', color='gray')

    # Angle label
    ax.text(0.5, 2.5, f"θ ≈ {np.degrees(theta):.2f}°", fontsize=12)

    # Formatting
    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title("Diffraction Grating (Surface at y = 0)")
    ax.grid(True)
    ax.legend()

    plt.show()

# Example

lambda0 = 493  # wavelength in nm
lines_per_mm = 3600

print("Wavelength (nm):", lambda0)
print("Lines per mm:", lines_per_mm)

plot_grating_orders(lines_per_mm,lambda0)
print(f"Littrow angle ≈ {np.degrees(littrow_angle(3600, 493)):.2f}°")