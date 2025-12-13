from typing import Final
from pathlib import  Path
from allytools.units.length import Length
from allytools.units.angle import Angle
from isensor.sensor import SensorFormats
from .objective import Objective, ObjectiveID, ObjectiveBrand

DSL935_F3_0_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Sunex, "DSL935 F3.0 NIR"),
    EFL=Length(9.6),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=3.0,
    max_fov=Angle.from_value(51.0),
    max_image_circle=Length(8.8),
    max_CRA=Angle.from_value(13.0),
    exit_pupil_diameter=Length(6.55),
    exit_pupil_position_to_image=Length(20.0),
    _zmx_file=Path(r"Catalog\Sunex\DSL935_F3.0.zmx"),
    filter=None)

DSL935_F4_8_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Sunex, "DSL935 F4.8 NIR"),
    EFL=Length(9.59),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=4.8,
    max_fov=Angle.from_value(51.0),
    max_image_circle=Length(8.8),
    max_CRA=Angle.from_value(13.0),
    exit_pupil_diameter=Length(4.1),
    exit_pupil_position_to_image=Length(20.5),
    _zmx_file=Path(r"Catalog\Sunex\DSL935_F4.8.zmx"),
    filter=None)

DSL934_F3_0_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Sunex, "DSL934 F3.0 NIR"),
    EFL=Length(9.0),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=3.0,
    max_fov=Angle.from_value(52.0),
    max_image_circle=Length(8.8),
    max_CRA=Angle.from_value(14.0),
    exit_pupil_diameter=Length(5.7),
    exit_pupil_position_to_image=Length(17.2),
    _zmx_file=Path(r"Catalog\Sunex\DSL934_F3.0.zmx"),
    filter=None,
)

DSL934_F4_0_NIR: Final[Objective] = Objective(
    objectiveID=ObjectiveID(ObjectiveBrand.Sunex, "DSL934 F4.0 NIR"),
    EFL=Length(9.0),
    sensor_format=SensorFormats.S_1_1_8,
    f_number=4.0,
    max_fov=Angle.from_value(52.0),
    max_image_circle=Length(8.8),
    max_CRA=Angle.from_value(14.0),
    exit_pupil_diameter=Length(4.3),
    exit_pupil_position_to_image=Length(17.2),
    _zmx_file=Path(r"Catalog\Sunex\DSL934_F4.0.zmx"),
    filter=None,
)

__all__ =["DSL934_F4_0_NIR", "DSL934_F3_0_NIR", "DSL935_F3_0_NIR", "DSL935_F4_8_NIR"]