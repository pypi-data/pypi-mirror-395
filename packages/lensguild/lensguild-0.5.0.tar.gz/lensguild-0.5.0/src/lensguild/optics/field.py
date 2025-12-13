from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any

# noinspection PyPep8Naming
@dataclass(slots=True)
class Field:
    X: float = 0.0
    Y: float = 0.0
    Weight: float = 1.0

    def set_X(self, v: float) -> None:
        self.X = float(v)

    def set_Y(self, v: float) -> None:
        self.Y = float(v)

    @property
    def x(self) -> float:
        return self.X

    @x.setter
    def x(self, v: float) -> None:
        self.set_X(v)

    @property
    def y(self) -> float:
        return self.Y

    @y.setter
    def y(self, v: float) -> None:
        self.set_Y(v)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Field":
        return cls(X=float(d.get("X", 0.0)),
                   Y=float(d.get("Y", 0.0)),
                   Weight=float(d.get("Weight", 1.0)))

    def __str__(self) -> str:
        return f"X={self.X:.6f}, Y={self.Y:.6f}, Weight={self.Weight:.3f}\n"