from __future__ import annotations
from typing import Mapping, Final
from types import MappingProxyType
from allytools.db import FrozenDB
from lensguild.objective.objective import Objective
from lensguild.objective.Sunex import *
from lensguild.objective.Commonlands import *
from lensguild.objective.Navitar import *
from lensguild.objective.EdmundOptics import *

_REGISTRY: dict[str, Objective] = {
    "DSL934_F3_0_NIR": DSL934_F3_0_NIR,
    "DSL934_F4_0_NIR": DSL934_F3_0_NIR,
    "DSL935_F4_8_NIR": DSL935_F4_8_NIR,
    "DSL935_F3_0_NIR": DSL935_F3_0_NIR,
    "CIL052_F3_4_M12B_NIR": CIL052_F3_4_M12B_NIR,
    "CIL085_F4_4_M12B_NIR":CIL085_F4_4_M12B_NIR,
    "Navitar_E3399_16_F5_6": NAVITAR_E3399_16_F5_6,
    "EO_86579_12_5_6":EO_86579_12_F5_6
}
class ObjectivesDB(metaclass=FrozenDB):
    __slots__ = ()
    DSL934_F3_0_NIR: Final[Objective] = DSL934_F3_0_NIR
    DSL934_F4_0_NIR: Final[Objective] = DSL934_F4_0_NIR
    DSL935_F4_8_NIR:    Final[Objective] = DSL935_F4_8_NIR
    DSL935_F3_0_NIR:    Final[Objective] = DSL935_F3_0_NIR
    CIL052_F3_4_M12B_NIR:    Final[Objective] = CIL052_F3_4_M12B_NIR
    CIL085_F4_4_M12B_NIR: Final[Objective] = CIL085_F4_4_M12B_NIR
    NAVITAR_E3399_16_F5_6: Final[Objective] = NAVITAR_E3399_16_F5_6
    EO_86579_12_F5_6: Final[Objective] = EO_86579_12_F5_6



    REGISTRY: Final[Mapping[str, Objective]] = MappingProxyType(_REGISTRY)

    @classmethod
    def get_objective(cls, name: str) -> Objective:
        try:
            return cls.REGISTRY[name]
        except KeyError as e:
            available = ", ".join(cls.REGISTRY.keys())
            raise KeyError(f"Unknown objective '{name}'. Available: {available}") from e

    @classmethod
    def names(cls) -> tuple[str, ...]:
        return tuple(cls.REGISTRY.keys())


