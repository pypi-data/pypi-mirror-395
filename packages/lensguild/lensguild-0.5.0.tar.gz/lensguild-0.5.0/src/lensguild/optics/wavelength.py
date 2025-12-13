from dataclasses import dataclass, field
from allytools.units.length import Length, LengthUnit
from enum import Enum
from math import isinf

class WavelengthUnit(Enum):
    NM = 1e-6  # nanometers to mm
    UM = 1e-3  # micrometers to mm

@dataclass(frozen=True)
class Wavelength:
    length: Length
    is_primary: bool
    weight: float = field(default=1.0)

    def __post_init__(self):
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Weight must be between 0 and 1 (got {self.weight})")

    @staticmethod
    def from_value(
        value: float,
        unit: WavelengthUnit = WavelengthUnit.NM,
        is_primary: bool = False,
        weight: float = 1.0
    ) -> 'Wavelength':
        value_mm = value * unit.value
        if isinf(value_mm) or value_mm <= 0:
            raise ValueError(f"Wavelength must be a finite, positive value (got {value} {unit.name})")
        return Wavelength(length=Length(value_mm), is_primary=is_primary, weight=weight)

    def to(self, unit: WavelengthUnit = WavelengthUnit.NM) -> float:
        return self.length.to(LengthUnit.MM) / unit.value

    def __str__(self) -> str:
        return f"{self.to(WavelengthUnit.NM):.1f} nm"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Wavelength):
            return NotImplemented
        return (
            self.length == other.length and
            self.weight == other.weight and
            self.is_primary == other.is_primary
        )

    def __lt__(self, other: 'Wavelength') -> bool:
        return self.length < other.length

    def __add__(self, other: 'Wavelength') -> 'Wavelength':
        return Wavelength(
            self.length + other.length,
            is_primary=self.is_primary,
            weight=self.weight  # You could choose to define behavior here
        )

    def __sub__(self, other: 'Wavelength') -> 'Wavelength':
        return Wavelength(
            self.length - other.length,
            is_primary=self.is_primary,
            weight=self.weight
        )