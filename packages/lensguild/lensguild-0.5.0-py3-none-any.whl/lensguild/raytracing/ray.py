from lensguild.raytracing.point import Point
from lensguild.raytracing.direction import Direction,DirectionMode
from typing import Tuple
from allytools.units.length import LengthUnit

class Ray:
    def __init__(self, point: Point, direction: Direction, is_paraxial: bool = False):
        self.start_point = point
        self.direction = direction
        self.is_paraxial = is_paraxial

        if is_paraxial:
            if direction.mode != DirectionMode.PARAXIAL:
                raise ValueError("Direction must be initialized in PARAXIAL mode when is_paraxial=True")

            self.u = direction.l
            self.y = point.y

    @property
    def position_mm(self) -> Tuple[float, float, float]:
        p = self.start_point
        return p.x.to(LengthUnit.MM), p.y.to(LengthUnit.MM), p.z.to(LengthUnit.MM)

    @property
    def direction_cosines(self) -> Tuple[float, float, float]:
        return self.direction.l, self.direction.m, self.direction.n

    def __repr__(self) -> str:
        x0, y0, z0 = self.position_mm
        l, m, n = self.direction_cosines
        base = f"Ray(P=({x0:.6f},{y0:.6f},{z0:.6f}) mm, D=({l:.6f},{m:.6f},{n:.6f})"
        if self.is_paraxial:
            base += f", paraxial: y={(self.y.to(LengthUnit.MM)):.6f} mm, u={self.u:.6e}"
        return base + ")"