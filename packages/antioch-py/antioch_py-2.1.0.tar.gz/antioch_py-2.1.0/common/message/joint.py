from common.message.base import Message


class JointState(Message):
    """
    State of a single joint.

    Represents the complete physical state of a joint including its position,
    velocity, and measured effort (force/torque).
    """

    _type = "antioch/joint_state"
    position: float
    velocity: float
    effort: float


class JointTarget(Message):
    """
    Control target for a single joint.

    Specifies desired position, velocity, and/or effort targets for a joint's
    PD controller. All fields are optional - omitted values are not controlled.
    """

    _type = "antioch/joint_target"
    position: float | None = None
    velocity: float | None = None
    effort: float | None = None


class JointStates(Message):
    """
    Collection of joint states for an actuator group.
    """

    _type = "antioch/joint_states"
    states: list[JointState]


class JointTargets(Message):
    """
    Collection of joint targets for an actuator group.
    """

    _type = "antioch/joint_targets"
    targets: list[JointTarget]
