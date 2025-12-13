from Optics.surface import OpticalSurface, BaseSurface
from typing import List

class LensData:
    def __init__(self):
        self.surfaces: List[OpticalSurface] = []

    def add_surface(self, surface: OpticalSurface):

        if not self.surfaces:
            if surface.base != BaseSurface.OBJ:
                raise ValueError("The first surface must be the object (OBJ) surface.")
            surface.is_global_reference = True
        else:
            if surface.base in {BaseSurface.OBJ, BaseSurface.STOP, BaseSurface.IMG}:
                if any(s.base == surface.base for s in self.surfaces):
                    raise ValueError(f"Only one '{surface.base.name}' surface is allowed in the lens.")

        self.surfaces.append(surface)
