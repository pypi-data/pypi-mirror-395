from typing import Final
from pathlib import  Path
from allytools.units.length import  Length
from allytools.units.angle import Angle
from isensor import SensorFormats
from .objective import Objective, ObjectiveID, ObjectiveBrand

EO_86579_12_F5_6: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.EdmundOptics, "EO 86579 f=16mm F/#5.6"),
    EFL=Length(16.0),
    sensor_format=SensorFormats.S_1_1,
    f_number=5.6,
    max_fov=Angle.from_value(32.0),
    max_image_circle=Length(17.6),
    max_CRA=Angle.from_value(10.0),
    exit_pupil_diameter=Length(18.4),
    exit_pupil_position_to_image=Length(51.5),
    _zmx_file=Path(r"Catalog\Edmund optics\Lenses\86570_5.6.zos"),
    filter=None)

__all__ =["EO_86579_12_F5_6"]