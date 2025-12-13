from common.message import Message, Pose
from common.session.config import JointAxis, JointType


class Joint(Message):
    """
    Complete specification for a joint connecting two links in an ark.

    A joint defines the kinematic relationship between a parent and child link,
    including the type of motion allowed, physical properties, and optional
    actuator_group assignment for coordinated control of multiple joints.
    """

    path: str
    parent: str
    child: str
    type: JointType
    pose: Pose
    axis: JointAxis | None
    lower_limit: float | None
    upper_limit: float | None


class Link(Message):
    """
    A link in the kinematic tree.

    Links are uniquely identified by their USD path.
    """

    path: str
