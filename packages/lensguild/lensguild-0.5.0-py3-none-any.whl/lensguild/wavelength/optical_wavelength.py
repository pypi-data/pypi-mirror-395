from dataclasses import dataclass, field
from Wavelength.wavelength import Wavelength, WavelengthUnit

@dataclass(frozen=True)
class OpticalWavelength(Wavelength):
    is_primary: bool = False
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
    ) -> 'OpticalWavelength':
        base = Wavelength.from_value(value, unit)
        return OpticalWavelength(length=base.length, is_primary=is_primary, weight=weight)

    def __str__(self) -> str:
        base = super().__str__()
        flag = " (primary)" if self.is_primary else ""
        return f"{base}{flag}, weight={self.weight:.2f}"