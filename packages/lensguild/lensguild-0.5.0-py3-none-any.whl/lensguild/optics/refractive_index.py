from dataclasses import dataclass
from typing import Optional

@dataclass
class RefractiveIndex:
    n: float                    # Real part of refractive index
    k: Optional[float] = None   # Optional imaginary part

    def is_complex(self) -> bool:
        return self.k is not None

    def as_complex(self) -> complex:
        return complex(self.n, self.k or 0.0)