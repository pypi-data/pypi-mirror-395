from dataclasses import dataclass, field
from typing import Tuple
from aidkit.units.length import Length, LengthUnit
from aidkit.units.angle import Angle, AngleUnit

@dataclass
class Pose:
    """Represents 3D translation and rotation of a surface."""
    translation: Tuple[Length, Length, Length] = field(default_factory=lambda: (
        Length.from_value(0.0, LengthUnit.MM),
        Length.from_value(0.0, LengthUnit.MM),
        Length.from_value(0.0, LengthUnit.MM)
    ))
    rotation: Tuple[Angle, Angle, Angle] = field(default_factory=lambda: (
        Angle.from_value(0.0, AngleUnit.DEG),
        Angle.from_value(0.0, AngleUnit.DEG),
        Angle.from_value(0.0, AngleUnit.DEG)
    ))  # roll, pitch, yaw

    def __str__(self) -> str:
        t = self.translation
        r = self.rotation
        return (f"Translation: x={t[0]}, y={t[1]}, z={t[2]}\n"
                f"Rotation: roll={r[0]}, pitch={r[1]}, yaw={r[2]}")
