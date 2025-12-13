from common.message.base import Message
from common.message.vector import Vector3


class Twist(Message):
    """
    Linear and angular velocity (twist).
    """

    linear: Vector3
    angular: Vector3
