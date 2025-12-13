from dataclasses import dataclass
from aidkit.units.angle_unit import AngleUnit
from aidkit.units.angle import Angle
from Optics.refractive_index import RefractiveIndex
from RayTracing.paraxial_angle import ParaxialAngle


@dataclass(frozen=True)
class SnellAngle(Angle):
    def __new__(cls, n: float, u_rad: float) -> "SnellAngle":
        value_rad = n * u_rad
        instance = object.__new__(cls)
        object.__setattr__(instance, "value_rad", value_rad)
        object.__setattr__(instance, "_original_unit", AngleUnit.RAD)
        return instance

    @staticmethod
    def from_n_u(ri: RefractiveIndex, u: ParaxialAngle) -> "SnellAngle":
        return SnellAngle(ri.n, u.to_radians())

    def to_n_u(self, n: float) -> float:
        """Returns paraxial angle u (in radians) by dividing by refractive index."""
        return self.value_rad / n

    def __str__(self) -> str:
        return f"{self.value_rad:.4f} rad (n·u)"
