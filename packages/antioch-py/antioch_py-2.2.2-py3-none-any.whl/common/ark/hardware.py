from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import Field

from common.message import Message, Pose
from common.session.config import ArticulationConfig, CameraConfig, ImuConfig, PirSensorConfig, RadarConfig


class HardwareType(str, Enum):
    """
    Types of hardware that can be attached to an instance.
    """

    CAMERA = "camera"
    IMU = "imu"
    PIR = "pir"
    RADAR = "radar"
    ACTUATOR_GROUP = "actuator_group"


class ActuatorGroupHardware(Message):
    """
    Actuator group hardware that controls multiple joints.
    """

    type: Literal[HardwareType.ACTUATOR_GROUP] = HardwareType.ACTUATOR_GROUP
    module: str
    name: str
    config: ArticulationConfig


class ImuHardware(Message):
    """
    IMU sensor hardware attached to a link.
    """

    type: Literal[HardwareType.IMU] = HardwareType.IMU
    module: str
    name: str
    path: str
    pose: Pose = Field(default_factory=Pose)
    parent_link: str | None = None
    config: ImuConfig


class PirHardware(Message):
    """
    PIR (Passive Infrared) sensor hardware attached to a link.
    """

    type: Literal[HardwareType.PIR] = HardwareType.PIR
    module: str
    name: str
    path: str
    pose: Pose = Field(default_factory=Pose)
    parent_link: str | None = None
    config: PirSensorConfig


class RadarHardware(Message):
    """
    Radar sensor hardware attached to a link.
    """

    type: Literal[HardwareType.RADAR] = HardwareType.RADAR
    module: str
    name: str
    path: str
    pose: Pose = Field(default_factory=Pose)
    parent_link: str | None = None
    config: RadarConfig


class CameraHardware(Message):
    """
    Camera sensor hardware attached to a link.

    Used for both RGB and depth cameras - the mode is specified in the config.
    """

    type: Literal[HardwareType.CAMERA] = HardwareType.CAMERA
    module: str
    name: str
    path: str
    pose: Pose = Field(default_factory=Pose)
    parent_link: str | None = None
    config: CameraConfig


# Discriminated union based on the 'type' field
Hardware = Annotated[
    Union[ActuatorGroupHardware, ImuHardware, PirHardware, RadarHardware, CameraHardware],
    Field(discriminator="type"),
]
