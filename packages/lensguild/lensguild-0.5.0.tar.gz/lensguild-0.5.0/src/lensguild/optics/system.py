from lensguild.optics.lens_data import LensData
from lensguild.optics.surface import OpticalSurface, BaseSurface, SurfaceType
from lensguild.optics.radius import Radius
from lensguild.optics.material import Material
from lensguild.optics.materials_catalog import MaterialCatalogs, CatalogName
from lensguild.optics.wavelengths import Wavelengths
from allytools.units import LengthUnit, Length
from lensguild.optics.field import Field, F
from lensguild.raytracing.point import Point

class System:
    def __init__(self):
        self.lens = LensData()
        self.fields = Field()
        self.materials = MaterialCatalogs()
        self.wavelengths = Wavelengths()
        self._initialize_default_materials()
        self._initialize_default_wavelengths()
        self._initialize_single_lens()
        self._initialize_default_fields()

    def _initialize_default_wavelengths(self):
        self.wavelengths.add_wavelength(value_nm=550,
                                        is_primary=True,
                                        weight=1.0)

    def _initialize_default_fields(self):
        self.fields.add_field(Length.from_value(0.0, LengthUnit.MM))

    def _initialize_default_materials(self):
        self.materials.add_from_registry(CatalogName.GENERAL)
        self.materials.add_from_registry(CatalogName.SCHOTT)

    def _initialize_default_lens(self):
        self.lens.add_surface(OpticalSurface(type = SurfaceType.STANDARD,
                                             base=BaseSurface.OBJ,
                                             radius=Radius.flat(),
                                             comment="Object plane"))
        self.lens.add_surface(OpticalSurface(type= SurfaceType.STANDARD,
                                             base=BaseSurface.STOP,
                                             radius=Radius.flat(),
                                             comment="Aperture stop"))
        self.lens.add_surface(OpticalSurface(type=SurfaceType.STANDARD,
                                             base=BaseSurface.IMG,
                                             radius=Radius.flat(),
                                             comment="Image plane"))
        center = Point(0, 0, 0),
    def _initialize_single_lens(self):
        self.lens.add_surface(OpticalSurface(type=SurfaceType.STANDARD,
                                             base=BaseSurface.OBJ,
                                             radius=Radius.flat(),
                                             thickness=Length(100.0, LengthUnit.MM),
                                             comment="Object plane"))
        self.lens.add_surface(OpticalSurface(type=SurfaceType.STANDARD,
                                             radius=Radius.from_value(50,LengthUnit.MM),
                                             thickness=Length(10.0, LengthUnit.MM),
                                             semi_diameter = Length(20.0, LengthUnit.MM),
                                             material= self._get_existing_material("N-BK7")))
        self.lens.add_surface(OpticalSurface(type=SurfaceType.STANDARD,
                                             base=BaseSurface.STOP,
                                             radius=Radius.from_value(-50,LengthUnit.MM),
                                             thickness=Length(93.0, LengthUnit.MM),
                                             semi_diameter=Length.from_value(20.0, LengthUnit.MM),
                                             comment="Aperture stop"))
        self.lens.add_surface(OpticalSurface(type=SurfaceType.STANDARD,
                                             base=BaseSurface.IMG,
                                             radius=Radius.flat(),
                                             thickness=Length.from_value(0.0, LengthUnit.MM),
                                             comment="Image plane"))

    def _get_existing_material(self, name: str) -> Material:
        material = self.materials.get_material(name)
        if material:
            return material
        raise ValueError(f"[MaterialCatalogs] Required material '{name}' not found in any loaded catalogs.")
