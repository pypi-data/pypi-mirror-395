from dataclasses import dataclass
from aidkit.units.length import Length, LengthUnit

@dataclass(frozen=True)
class Radius:
    length: Length  # Radius is stored as a Length in mm internally

    @staticmethod
    def from_value(value: float, unit: LengthUnit) -> 'Radius':
        return Radius(Length.from_value(value, unit))

    @staticmethod
    def flat() -> 'Radius':
        return Radius(Length.infinity())

    def is_flat(self) -> bool:
        return self.length.is_infinite()

    def to(self, unit: LengthUnit) -> float:
        return self.length.to(unit)

    @property
    def value_mm(self) -> float:
        return self.length.value_mm

    def sign(self) -> int:
        if self.is_flat():
            return 0
        return 1 if self.value_mm > 0 else -1

    def __str__(self) -> str:
        if self.is_flat():
            return "∞ mm (Flat)"
        direction = "Convex" if self.value_mm > 0 else "Concave"
        return f"{self.value_mm:.2f} mm ({direction})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Radius):
            return NotImplemented
        return self.length == other.length

    def __neg__(self) -> 'Radius':
        return Radius(Length(-self.value_mm))
