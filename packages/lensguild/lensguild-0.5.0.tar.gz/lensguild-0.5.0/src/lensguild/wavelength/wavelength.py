from dataclasses import dataclass, field
from allytools.units.length import Length, LengthUnit
from enum import Enum
from math import isinf


class WavelengthUnit(Enum):
    NM = 1e-6  # nanometers → mm
    UM = 1e-3  # micrometers → mm


@dataclass(frozen=True)
class Wavelength:
    length: Length

    @staticmethod
    def from_value(value: float, unit: WavelengthUnit = WavelengthUnit.NM) -> 'Wavelength':
        value_mm = value * unit.value
        if isinf(value_mm) or value_mm <= 0:
            raise ValueError(f"Wavelength must be a finite, positive value (got {value} {unit.name})")
        return Wavelength(length=Length(value_mm))

    def to(self, unit: WavelengthUnit = WavelengthUnit.NM) -> float:
        return self.length.to(LengthUnit.MM) / unit.value

    def __str__(self) -> str:
        return f"{self.to(WavelengthUnit.NM):.1f} nm"

    def __lt__(self, other: 'Wavelength') -> bool:
        return self.length < other.length

    def __add__(self, other: 'Wavelength') -> 'Wavelength':
        return Wavelength(self.length + other.length)

    def __sub__(self, other: 'Wavelength') -> 'Wavelength':
        return Wavelength(self.length - other.length)