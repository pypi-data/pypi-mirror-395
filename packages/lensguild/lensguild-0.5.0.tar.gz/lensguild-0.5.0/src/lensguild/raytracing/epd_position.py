import numpy as np
from aidkit.units.length import Length, LengthUnit
from Optics.surface import OpticalSurface, BasicSurface

def compute_entrance_pupil_position(surfaces: list[OpticalSurface]) -> Length:
    stop_index = next((i for i, s in enumerate(surfaces) if s.basic == BasicSurface.STOP), None)
    if stop_index is None:
        raise ValueError("STOP surface is not defined.")
    if stop_index <= 1:
        raise ValueError("STOP must come after surface[1] to compute EPP relative to it.")

    curr = surfaces[stop_index]
    prev = surfaces[stop_index - 1]

    n_before = curr.material.refractive_index  # medium where light is coming from
    n_after = prev.material.refractive_index   # medium light is going into
    R = curr.radius.value_mm

    # ✅ Corrected refraction matrix for backward tracing
    if not curr.radius.is_flat():
        refraction = np.array([
            [1, 0],
            [(n_before - n_after) / (n_before * R), n_after / n_before]
        ])
    else:
        refraction = np.identity(2)

    d = prev.thickness.to(LengthUnit.MM)
    translation = np.array([
        [1, -d],
        [0, 1]
    ])

    M = translation @ refraction

    print(f"Refraction matrix @ surface {stop_index}:\n{refraction}")
    print(f"Translation matrix from surface {stop_index - 1} to {stop_index}:\n{translation}")

    y_in = 1.0
    u_in = 0.0
    y_out = M[0, 0] * y_in + M[0, 1] * u_in
    u_out = M[1, 0] * y_in + M[1, 1] * u_in

    if abs(u_out) < 1e-12:
        raise ZeroDivisionError("Paraxial ray is parallel after tracing; EPP is at infinity.")

    # ✅ Do not negate, because we’re tracing backward
    z_rel = -y_out / u_out
    return Length.from_value(z_rel, LengthUnit.MM)
