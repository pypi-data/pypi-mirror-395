from pydantic import Field

from common.message import Message, Pose


class ImuConfig(Message):
    """
    Configuration for IMU sensor.
    """

    frequency: int | None = Field(default=None, description="Sensor update frequency in Hz (optional, defaults to physics rate)")
    linear_acceleration_filter_size: int = Field(default=10, description="Filter window size for linear acceleration")
    angular_velocity_filter_size: int = Field(default=10, description="Filter window size for angular velocity")
    orientation_filter_size: int = Field(default=10, description="Filter window size for orientation")


class GetImu(Message):
    """
    Get an existing IMU sensor.
    """

    path: str | None = Field(default=None, description="USD path of the IMU prim")


class GetImuResponse(Message):
    """
    Response from getting an IMU.
    """

    path: str


class AddImu(Message):
    """
    Add an IMU sensor.
    """

    path: str = Field(description="USD path for the IMU")
    config: ImuConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")


class GetImuSample(Message):
    """
    Get IMU sensor sample.
    """

    path: str


class BufferImuRead(Message):
    """
    Request to buffer current IMU data at simulation time.
    """

    path: str


class GetBufferedImuRead(Message):
    """
    Request to get buffered IMU data at or before simulation time.
    """

    path: str
    read_sim_time: float
