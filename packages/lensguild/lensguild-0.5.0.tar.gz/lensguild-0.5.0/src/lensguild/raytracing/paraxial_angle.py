from dataclasses import dataclass
from aidkit.units.angle_unit import AngleUnit
from aidkit.units.angle import Angle

@dataclass(frozen=True)
class ParaxialAngle(Angle):
    def __new__(cls, value_radians: float) -> "ParaxialAngle":
        return super().__new__(cls, value_rad=value_radians, _original_unit=AngleUnit.RAD)

    @staticmethod
    def from_radians(value_radians: float) -> "ParaxialAngle":
        return ParaxialAngle(value_radians)

    @staticmethod
    def from_degrees(value_deg: float) -> "ParaxialAngle":
        value_rad = AngleUnit.DEG.to_radians(value_deg)
        return ParaxialAngle(value_rad)

    def to_radians(self) -> float:
        return self.to(AngleUnit.RAD)

    def to_degrees(self) -> float:
        return self.to(AngleUnit.DEG)

    def is_parallel(self, tol: float = 1e-9) -> bool:
        return abs(self.value_rad) < tol

    @staticmethod
    def zero() -> "ParaxialAngle":
        return ParaxialAngle(0.0)

    def __str__(self) -> str:
        if self.is_parallel():
            return "0 rad (parallel to axis)"
        return super().__str__()
