from dataclasses import dataclass
from typing import Optional
from Optics.refractive_index import RefractiveIndex


@dataclass(frozen=True)
class Material:
    name: str                      # e.g. "N-BK7"
    refractive_index: RefractiveIndex        # e.g. 1.5168 (nd at 589.3 nm)
    abbe_number: float             # e.g. 64.17 (Vd)
    density: Optional[float] = None  # [g/cm^3], optional
    manufacturer: Optional[str] = None  # e.g. "Schott", optional

    def __str__(self):
        return f"{self.name} (n={self.refractive_index}, Vd={self.abbe_number})"


