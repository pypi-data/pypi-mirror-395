import matplotlib.pyplot as plt
import numpy as np

from aidkit.units.length import Length
from aidkit.units.length_unit import LengthUnit
from aidkit.units.angle import Angle
from aidkit.units.angle_unit import AngleUnit
def draw_layout(system, traced_rays=None, show_materials=True):
    surfaces = system.lens.surfaces
    z = 0.0
    z_positions = []

    # Compute surface positions
    for surface in surfaces:
        z_positions.append(z)
        z += surface.thickness.to(LengthUnit.MM)

    fig, ax = plt.subplots(figsize=(12, 3))

    # Draw material regions between surfaces
    for i in range(len(surfaces) - 1):
        z_start = z_positions[i]
        z_end = z_positions[i + 1]
        y_max = max(surfaces[i].semi_diameter.to(LengthUnit.MM), 1.0)
        ax.axvspan(z_start, z_end, color='lightgrey', alpha=0.2)

        if show_materials:
            mat = surfaces[i].material.name
            z_mid = (z_start + z_end) / 2
            ax.text(z_mid, y_max + 2, mat, fontsize=8, ha='center', va='bottom')

    # Draw surfaces
    for surface, z_pos in zip(surfaces, z_positions):
        r = surface.radius.value_mm
        aperture = surface.semi_diameter.to(LengthUnit.MM)

        if surface.radius.is_flat():
            ax.plot([z_pos, z_pos], [-aperture, aperture], color="black")
        else:
            direction = -1 if r < 0 else 1
            curvature = abs(r)
            theta = np.linspace(-0.5, 0.5, 100)
            x = z_pos + direction * (curvature - curvature * np.cos(theta))
            y = aperture * np.sin(theta)
            ax.plot(x, y, color="blue")

    # Draw traced paraxial ray if given
    if traced_rays is not None and len(traced_rays) == len(z_positions):
        ray_z = []
        ray_y = []
        for z, ray in zip(z_positions, traced_rays):
            ray_z.append(z)
            ray_y.append(ray.y.to(LengthUnit.MM))
        ax.plot(ray_z, ray_y, color="red", linewidth=1.5, label="Paraxial Ray")

    ax.set_aspect('equal')
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel("Height (mm)")
    ax.set_title("Lens Layout with Material Zones")
    ax.grid(True)
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()