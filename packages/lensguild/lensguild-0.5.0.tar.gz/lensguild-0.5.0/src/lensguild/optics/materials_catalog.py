from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum, auto
from Optics import Material
from Optics.refractive_index import RefractiveIndex

def get_default_material() -> Material:
    air = CATALOG_REGISTRY[CatalogName.GENERAL].get_material("Air")
    if air:
        return air
    raise RuntimeError("Default material 'Air' not found in GENERAL catalog.")

class CatalogName(Enum):
    GENERAL = auto()
    SCHOTT = auto()
    OHARA = auto()

@dataclass
class MaterialCatalog:
    name: CatalogName
    materials: List[Material] = field(default_factory=list)

    def get_material(self, name: str) -> Optional[Material]:
        for g in self.materials:
            if g.name == name:
                return g
        return None

CATALOG_REGISTRY = {
    CatalogName.GENERAL: MaterialCatalog(name=CatalogName.GENERAL, materials=[
        Material(name="Air", refractive_index=RefractiveIndex(1.0), abbe_number=999.0, density=0.0012)
    ]),
    CatalogName.SCHOTT: MaterialCatalog(name=CatalogName.SCHOTT, materials=[
        Material(name="N-BK7", refractive_index=RefractiveIndex(1.5168), abbe_number=64.17, density=2.51),
        Material(name="N-SF10", refractive_index=RefractiveIndex(1.7282), abbe_number=28.41, density=3.65)
    ]),
    CatalogName.OHARA: MaterialCatalog(name=CatalogName.OHARA, materials=[
        Material(name="S-BSL7", refractive_index=RefractiveIndex(1.51633), abbe_number=64.15, density=2.51),
        Material(name="S-FPL53", refractive_index=RefractiveIndex(1.43999), abbe_number=94.99, density=2.39)
    ])
}

@dataclass
class MaterialCatalogs:
    catalogs: List[MaterialCatalog] = field(default_factory=list)

    def add_from_registry(self, name: CatalogName):
        if name in CATALOG_REGISTRY:
            catalog = CATALOG_REGISTRY[name]
            if all(c.name != catalog.name for c in self.catalogs):
                self.catalogs.append(MaterialCatalog(name=catalog.name, materials=list(catalog.materials)))

    def get_material(self, name: str) -> Optional[Material]:
        for catalog in self.catalogs:
            material = catalog.get_material(name)
            if material:
                return material
        print(f"[MaterialCatalogs] Material '{name}' not found in catalogs {[c.name.name for c in self.catalogs]}.")
        return None

    def list_all_materials(self) -> List[str]:
        return [m.name for c in self.catalogs for m in c.materials]

    def __str__(self):
        return f"MaterialCatalogs({[c.name.name for c in self.catalogs]})"


