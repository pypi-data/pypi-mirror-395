from __future__ import annotations
from typing import Iterable, Iterator, Optional, Sequence, Tuple, Union
from allytools.units.length import Length, LengthUnit

_Number = Union[float, int]
_Value = Union[Length, _Number]

def _to_length(value: Optional[_Value], default_unit: LengthUnit) -> Optional[Length]:
    if value is None:
        return None
    if isinstance(value, Length):
        return value
    return Length(float(value), default_unit)

class Point:

    __slots__ = ("_x", "_y", "_z", "_default_unit")

    def __init__(
        self,
        x: Optional[_Value] = None,
        y: Optional[_Value] = None,
        z: Optional[_Value] = None,
        *,
        default_unit: LengthUnit = LengthUnit.MM,
    ) -> None:
        self._default_unit: LengthUnit = default_unit
        self._x: Length = _to_length(x, default_unit) or Length(0.0, default_unit)
        self._y: Length = _to_length(y, default_unit) or Length(0.0, default_unit)
        self._z: Optional[Length] = _to_length(z, default_unit)  # None => 2D

    # ---------- convenience constructors ----------
    @classmethod
    def from_iterable(
        cls, vals: Iterable[_Value], *, default_unit: LengthUnit = LengthUnit.MM
    ) -> "Point":
        seq = list(vals)
        if len(seq) == 2:
            return cls(seq[0], seq[1], None, default_unit=default_unit)
        elif len(seq) == 3:
            return cls(seq[0], seq[1], seq[2], default_unit=default_unit)
        else:
            raise ValueError("Expected 2 or 3 values for Point.")

    @classmethod
    def xy(
        cls, x: _Value, y: _Value, *, default_unit: LengthUnit = LengthUnit.MM
    ) -> "Point":
        return cls(x, y, None, default_unit=default_unit)

    @classmethod
    def xyz(
        cls, x: _Value, y: _Value, z: _Value, *, default_unit: LengthUnit = LengthUnit.MM
    ) -> "Point":
        return cls(x, y, z, default_unit=default_unit)

    # ---------- properties ----------
    @property
    def default_unit(self) -> LengthUnit:
        return self._default_unit

    @property
    def dim(self) -> int:
        return 2 if self._z is None else 3

    @property
    def x(self) -> Length:
        return self._x

    @x.setter
    def x(self, value: _Value) -> None:
        self._x = _to_length(value, self._default_unit) or Length(0.0, self._default_unit)

    @property
    def y(self) -> Length:
        return self._y

    @y.setter
    def y(self, value: _Value) -> None:
        self._y = _to_length(value, self._default_unit) or Length(0.0, self._default_unit)

    @property
    def z(self) -> Optional[Length]:
        return self._z

    @z.setter
    def z(self, value: Optional[_Value]) -> None:
        self._z = _to_length(value, self._default_unit) if value is not None else None

    # ---------- conversions & exports ----------
    def to(self, unit: LengthUnit) -> "Point":
        z = self._z.to(unit) if self._z is not None else None
        return Point(self._x.to(unit), self._y.to(unit), z, default_unit=unit)

    def as_tuple(self, unit: Optional[LengthUnit] = None) -> Tuple[float, float, Optional[float]]:
        if unit is None:
            unit = self._default_unit
        x = self._x.to(unit).value
        y = self._y.to(unit).value
        z_val = self._z.to(unit).value if self._z is not None else None
        return (x, y, z_val)

    def as_sequence(self, unit: Optional[LengthUnit] = None) -> Sequence[float]:
        """Return [x, y] or [x, y, z] numeric list."""
        t = self.as_tuple(unit)
        return [t[0], t[1]] if t[2] is None else [t[0], t[1], t[2]]  # type: ignore[list-item]


    def __len__(self) -> int:
        return self.dim

    def __iter__(self) -> Iterator[Length]:
        yield self._x
        yield self._y
        if self._z is not None:
            yield self._z

    def __getitem__(self, index: int) -> Length:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        elif index == 2 and self._z is not None:
            return self._z
        raise IndexError(f"Index out of range for {self.dim}D Point.")

    def __setitem__(self, index: int, value: _Value) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            if self._z is None and value is not None:
                self._z = _to_length(value, self._default_unit)
            else:
                self.z = value
        else:
            raise IndexError(f"Index out of range for {self.dim}D Point.")

    def __repr__(self) -> str:
        if self._z is None:
            return f"Point2D(x={self._x}, y={self._y})"
        return f"Point3D(x={self._x}, y={self._y}, z={self._z})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        unit = self._default_unit
        if self.dim != other.dim:
            return False
        if self._x.to(unit).value != other._x.to(unit).value:
            return False
        if self._y.to(unit).value != other._y.to(unit).value:
            return False
        if self._z is None and other._z is None:
            return True
        if (self._z is None) != (other._z is None):
            return False
        return self._z.to(unit).value == other._z.to(unit).value  # type: ignore[union-attr]
