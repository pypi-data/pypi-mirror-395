from dataclasses import dataclass, field
from typing import Optional
from enum import Enum, auto
from aidkit.units.length import Length, LengthUnit
from Optics.radius import Radius
from Optics import Material
from Optics import get_default_material


class BaseSurface(Enum):
    OBJ = auto()
    STOP = auto()
    IMG = auto()


class SurfaceType(Enum):
    STANDARD = auto()
    PARAXIAL = auto()

    def __str__(self):
        return self.name.capitalize()

@dataclass
class OpticalSurface:
    type: SurfaceType
    base: Optional[BaseSurface] = None
    comment: str = ""
    radius: Radius = Radius.flat()
    thickness: Length = Length(0.0, LengthUnit.MM)
    material: Material = field(default_factory=get_default_material)
    semi_diameter: Length = Length.from_value(0.0, LengthUnit.MM)
    is_global_reference: bool = False

    @property
    def is_basic(self) -> bool:
        return self.base is not None




