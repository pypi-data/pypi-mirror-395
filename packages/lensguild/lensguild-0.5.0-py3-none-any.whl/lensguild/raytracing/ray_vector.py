import numpy as np
from dataclasses import dataclass
from allytools.units.length import Length
from RayTracing.snell_angle import SnellAngle
from RayTracing.ray import Ray
from Optics.surface import OpticalSurface

@dataclass
class RayVector:
    nu: SnellAngle
    y: Length

    @staticmethod
    def from_ray(ray:Ray, surface:OpticalSurface) -> "RayVector":
        if not ray.is_paraxial:
            raise ValueError("Ray must be paraxial to build a RayVector")

        n = surface.material.refractive_index.n
        u = ray.u
        y = ray.y
        sn = SnellAngle(n, u)

        return RayVector(nu=sn, y=y)

    def as_array(self) -> np.ndarray:
        return np.array([[self.nu.value_rad], [self.y.value_mm]], dtype=float)

    def __repr__(self) -> str:
        return f"RayVector(nu={self.nu.value_rad:.6f} rad, y={self.y.value_mm:.6f} mm)"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.nu.value_rad  # optical direction in radians
        elif index == 1:
            return self.y.value_mm  # transverse height in mm
        else:
            raise IndexError("RayVector only supports indices 0 (nu) and 1 (y)")

    def __len__(self) -> int:
        return 2


