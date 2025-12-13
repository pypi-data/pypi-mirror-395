from __future__ import annotations
from typing import Tuple
import math
import numpy as np
from enum import Enum, auto
from dataclasses import dataclass

class DirectionMode(Enum):
    COSINE = auto()
    TANGENT = auto()
    PARAXIAL = auto()

@dataclass(frozen=True, slots=True)

class Direction:
    l: float
    m: float
    n: float
    mode: DirectionMode

    @classmethod
    def _from_components(cls, l: float, m: float, n: float,
                         mode: DirectionMode,
                         normalize: bool = True) -> Direction:
        if normalize:
            mag = math.sqrt(l*l + m*m + n*n)
            if mag == 0:
                raise ValueError("Direction cosines cannot all be zero.")
            l, m, n = l/mag, m/mag, n/mag
        return cls(l, m, n, mode)

    @classmethod
    def from_cosines(cls, l: float, m: float, n: float,
                     *, normalize: bool = True) -> Direction:
        return cls._from_components(l, m, n, DirectionMode.COSINE, normalize)

    @classmethod
    def from_tangents(cls, tan_x: float, tan_y: float,
                      *, normalize: bool = True) -> Direction:
        return cls._from_components(tan_x, tan_y, 1.0,
                                    DirectionMode.TANGENT, normalize)
    @classmethod
    def from_paraxial(cls, u: float,
                      *, normalize: bool = True) -> Direction:
        return cls._from_components(u, 0.0, 1.0,
                                    DirectionMode.PARAXIAL, normalize)


    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.l, self.m, self.n)

    def to_numpy(self) -> np.ndarray:
        """Return as NumPy array [l, m, n]."""
        return np.array([self.l, self.m, self.n], dtype=float)

    def as_tangents(self) -> Tuple[float, float]:
        """Return (tan_x, tan_y)."""
        if abs(self.n) < 1e-15:
            raise ZeroDivisionError("Cannot compute tangents: n ≈ 0.")
        return (self.l / self.n, self.m / self.n)

    def as_paraxial_u(self) -> float:
        """Return meridional slope u."""
        if abs(self.n) < 1e-15:
            raise ZeroDivisionError("Cannot convert to paraxial: n ≈ 0.")
        return self.l / self.n

    def normalized(self) -> Direction:
        """Return a normalized copy (mode resets to COSINE)."""
        mag = math.sqrt(self.l*self.l + self.m*self.m + self.n*self.n)
        if mag == 0:
            raise ValueError("Zero-length direction.")
        return Direction(self.l/mag, self.m/mag, self.n/mag, DirectionMode.COSINE)


    def dot(self, other: Direction) -> float:
        return self.l*other.l + self.m*other.m + self.n*other.n

    def cross(self, other: Direction) -> Direction:
        l = self.m*other.n - self.n*other.m
        m = self.n*other.l - self.l*other.n
        n = self.l*other.m - self.m*other.l
        return Direction.from_cosines(l, m, n)

    def __repr__(self):
        return (f"Direction(l={self.l:.6f}, m={self.m:.6f}, "
                f"n={self.n:.6f}, mode={self.mode.name})")

    def __str__(self):
        return f"({self.l:.3f}, {self.m:.3f}, {self.n:.3f})"