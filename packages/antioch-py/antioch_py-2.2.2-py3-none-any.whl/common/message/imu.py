from common.message.base import Message
from common.message.quaternion import Quaternion
from common.message.vector import Vector3


class ImuSample(Message):
    """
    IMU sensor sample data.
    """

    _type = "antioch/imu_sample"
    linear_acceleration: Vector3
    angular_velocity: Vector3
    orientation: Quaternion
