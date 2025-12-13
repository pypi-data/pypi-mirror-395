from typing import Final
from pathlib import  Path
from allytools.units.length import  Length
from allytools.units.angle import Angle
from isensor import SensorFormats
from lensguild.objective.objective import Objective, ObjectiveID, ObjectiveBrand

NAVITAR_E3399_16_F5_6: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Navitar, "NAVITAR E3399 f=16mm F/#5.6"),
    EFL=Length(16.0),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=5.6,
    max_fov=Angle.from_value(32.0),
    max_image_circle=Length(20.0),
    max_CRA=Angle.from_value(10.0),
    exit_pupil_diameter=Length(94.2),
    exit_pupil_position_to_image=Length(528),
    _zmx_file=Path(r"Catalog\Navitar\E3399 (1-26497)_16_5.6.zmx"),
    filter=None,
)

__all__ =["NAVITAR_E3399_16_F5_6"]