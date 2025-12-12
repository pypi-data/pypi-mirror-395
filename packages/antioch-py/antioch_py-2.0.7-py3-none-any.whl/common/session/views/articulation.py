from pydantic import Field

from common.message import JointState, JointTarget, Message, Pose, Vector3


class ArticulationJointConfig(Message):
    """
    Complete configuration for a single joint in an articulation.
    """

    path: str = Field(description="Name of the joint/DOF")
    stiffness: float | None = Field(default=None, description="PD controller stiffness (Kp)")
    damping: float | None = Field(default=None, description="PD controller damping (Kd)")
    lower_limit: float | None = Field(default=None, description="Lower joint limit")
    upper_limit: float | None = Field(default=None, description="Upper joint limit")
    armature: float | None = Field(default=None, description="Joint armature")
    friction_coefficient: float | None = Field(default=None, description="Joint friction coefficient")
    max_velocity: float | None = Field(default=None, description="Maximum joint velocity")
    max_effort: float | None = Field(default=None, description="Maximum joint effort")


class ArticulationConfig(Message):
    """
    Configuration for applying articulation root to a prim.
    """

    solver_position_iterations: int = Field(default=32, description="Number of position iterations for the solver")
    solver_velocity_iterations: int = Field(default=1, description="Number of velocity iterations for the solver")
    sleep_threshold: float = Field(default=0.005, description="Sleep threshold for the articulation")
    stabilization_threshold: float = Field(default=0.001, description="Stabilization threshold for the articulation")
    enable_self_collisions: bool = Field(default=False, description="Whether to enable self-collisions")
    joint_configs: list[ArticulationJointConfig] = Field(default_factory=list, description="Per-joint configurations")


class GetArticulation(Message):
    """
    Get an existing articulation view from a prim with ArticulationRootAPI already applied.
    """

    path: str | None = Field(default=None, description="USD path of the articulation prim")


class GetArticulationResponse(Message):
    """
    Response from getting an articulation.
    """

    path: str


class AddArticulation(Message):
    """
    Add an articulation by applying ArticulationRootAPI to a prim.
    """

    path: str = Field(description="USD path of prim to apply articulation to")
    config: ArticulationConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")
    scale: Vector3 | None = Field(default=None, description="Scale (x, y, z)")


class ArticulationJointStates(Message):
    """
    Response containing joint states.
    """

    joint_states: list[JointState]


class ArticulationJointTargets(Message):
    """
    Response containing joint targets.
    """

    joint_targets: list[JointTarget]


class GetArticulationJointStates(Message):
    """
    Get articulation joint states.
    """

    path: str
    joint_names: list[str] | None = None


class GetArticulationJointTargets(Message):
    """
    Get articulation control targets.
    """

    path: str
    joint_names: list[str] | None = None


class SetArticulationJointStates(Message):
    """
    Set articulation joint states (immediate teleport).
    """

    path: str
    joint_names: list[str] | None = None
    joint_states: list[JointState] | None = None


class SetArticulationJointTargets(Message):
    """
    Set articulation control targets using PD controller.
    """

    path: str
    joint_names: list[str] | None = None
    joint_targets: list[JointTarget] | None = None


class GetArticulationJointConfigs(Message):
    """
    Get joint configurations for all joints.
    """

    path: str
    joint_names: list[str] | None = None


class ArticulationJointConfigs(Message):
    """
    Joint configurations response.
    """

    joint_configs: list[ArticulationJointConfig]


class SetArticulationJointConfigs(Message):
    """
    Set joint configurations.
    """

    path: str
    joint_configs: list[ArticulationJointConfig]


class BufferArticulationRead(Message):
    """
    Request to buffer current articulation state at simulation time.
    """

    path: str


class GetBufferedArticulationRead(Message):
    """
    Request to get buffered articulation state at or before simulation time.
    """

    path: str
    read_sim_time: float


class BufferedArticulationState(Message):
    """
    Buffered articulation state with joint names for filtering.
    """

    pose: Pose
    joint_states: list[JointState]
    joint_names: list[str]


class BufferArticulationWrite(Message):
    """
    Request to buffer articulation write at target simulation time.
    """

    path: str
    write_sim_time: float
    joint_names: list[str] | None = None
    joint_targets: list[JointTarget] | None = None


class BufferArticulationWriteResponse(Message):
    """
    Acknowledgment for buffered articulation write.
    """
