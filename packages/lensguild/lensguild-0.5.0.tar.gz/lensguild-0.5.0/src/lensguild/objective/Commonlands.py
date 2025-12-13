from typing import Final
from pathlib import  Path
from allytools.units.length import Length
from allytools.units.angle import Angle
from isensor.sensor import SensorFormats
from .objective import Objective, ObjectiveID, ObjectiveBrand

CIL085_F4_4_M12B_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Commonlands, "CIL085-F4.4-M12B_NIR"),
    EFL=Length(8.2),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=4.4,
    max_fov=Angle.from_value(57.0),
    max_image_circle=Length(8.8),
    max_CRA=Angle.from_value(10.0),
    exit_pupil_diameter=Length(5.3),
    exit_pupil_position_to_image=Length(23.3),
    _zmx_file=Path(r"Catalog\Commanlands\CIL085_F4.4.zmx"),
    filter=None,
)

CIL052_F3_4_M12B_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Commonlands, "CIL052-F3.4-M12A_NIR"),
    EFL=Length(5.2),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=3.4,
    max_fov=Angle.from_value(82.0),
    max_image_circle=Length(8.9),
    max_CRA=Angle.from_value(12.0),
    exit_pupil_diameter=Length(5.2),
    exit_pupil_position_to_image=Length(17.7),
    _zmx_file=Path(r"Catalog\Commanlands\CIL052_F3.4.zmx"),
    filter=None,
)

__all__ =["CIL085_F4_4_M12B_NIR", "CIL052_F3_4_M12B_NIR"]