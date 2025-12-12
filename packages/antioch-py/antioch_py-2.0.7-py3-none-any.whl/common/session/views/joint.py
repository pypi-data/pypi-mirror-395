from enum import Enum

from pydantic import Field

from common.message import Message, Pose


class JointType(str, Enum):
    """
    Types of joints supported by the simulator.
    """

    REVOLUTE = "revolute"
    PRISMATIC = "prismatic"
    FIXED = "fixed"
    SPHERICAL = "spherical"
    DISTANCE = "distance"
    GENERIC = "generic"


class JointAxis(str, Enum):
    """
    Axis of motion for joints.
    """

    X = "x"
    Y = "y"
    Z = "z"


class JointConfig(Message):
    """
    Configuration for a joint object that connects two bodies.
    """

    # Joint relationships
    parent_path: str = Field(description="USD path to parent body")
    child_path: str = Field(description="USD path to child body")

    # Transform
    pose: Pose = Field(default_factory=Pose.identity, description="Joint pose relative to parent")

    # Joint properties
    joint_type: JointType = Field(default=JointType.FIXED, description="Type of joint motion allowed")
    axis: JointAxis = Field(default=JointAxis.X, description="Axis of motion for non-fixed joints")

    # Motion limits (for revolute: degrees, for prismatic: meters)
    lower_limit: float | None = Field(default=None, description="Lower motion limit")
    upper_limit: float | None = Field(default=None, description="Upper motion limit")

    # Physics properties
    friction: float = Field(default=0.01, description="Joint friction (unitless)")
    armature: float = Field(default=0.1, description="Joint armature (kg for prismatic, kg-m^2 for revolute)")

    # Special properties
    exclude_from_articulation: bool = Field(default=False, description="Whether to exclude this joint from articulation")


class GetJoint(Message):
    """
    Get an existing joint.
    """

    path: str | None = Field(default=None, description="USD path of the joint prim")


class GetJointResponse(Message):
    """
    Response from getting a joint.
    """

    path: str


class AddJoint(Message):
    """
    Add a joint connecting two bodies.
    """

    path: str = Field(description="USD path for the joint")
    config: JointConfig
