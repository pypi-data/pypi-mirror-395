from dataclasses import dataclass, field
from typing import List
from Optics.wavelength import  Wavelength, WavelengthUnit

@dataclass
class Wavelengths:
    wavelengths: List[Wavelength] = field(default_factory=list)

    def add_wavelength(self, value_nm: float, is_primary: bool = False, weight: float = 1.0):
        new_wavelength = Wavelength.from_value(
            value=value_nm,
            unit=WavelengthUnit.NM,
            is_primary=is_primary,
            weight=weight
        )
        if any(w.length == new_wavelength.length for w in self.wavelengths):
            return  # Optionally: log, warn, or replace

        self.wavelengths.append(new_wavelength)