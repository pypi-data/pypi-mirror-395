from antioch.session.session import Session, SessionContainer
from common.message import JointState, JointTarget, Pose, Vector3
from common.session.config import ArticulationConfig, ArticulationJointConfig


class Articulation(SessionContainer):
    """
    Ergonomic wrapper for articulation operations.

    Articulations should be added using scene.add_articulation() or retrieved using scene.get_articulation().

    Example:
        scene = Scene()

        # Get an existing articulation
        robot = scene.get_articulation(path="/World/robot")

        # Use articulation
        joint_states = robot.get_joint_states()
        robot.set_joint_targets(
            joint_targets=[
                JointTarget(position=0.1, velocity=0.0, effort=0.0),
                JointTarget(position=0.2, velocity=0.0, effort=0.0),
            ]
        )
        pose = robot.get_world_pose()
    """

    def __init__(self, path: str):
        """
        Initialize articulation by resolving path and validating existence.

        :param path: USD path for the articulation.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="articulation/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(
        cls,
        path: str,
        config: ArticulationConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
        scale: Vector3 | None,
    ) -> "Articulation":
        """
        Add an articulation to the scene.

        :param path: USD path for the articulation.
        :param config: Articulation configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :param scale: Optional scale.
        :return: The articulation instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="articulation/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose, "scale": scale},
        )
        return cls(path)

    def get_joint_states(self, joint_names: list[str] | None = None) -> list[JointState]:
        """
        Get current joint states.

        :param joint_names: Optional list of joint names. If None, returns all joints.
        :return: List of joint states.
        """

        response = self._session.query_sim_rpc(
            endpoint="articulation/get_joint_states",
            payload={"path": self._path, "joint_names": joint_names},
        )
        return [JointState.model_validate(js) for js in response] if response else []

    def get_joint_targets(self, joint_names: list[str] | None = None) -> list[JointTarget]:
        """
        Get current applied control targets.

        :param joint_names: Optional list of joint names. If None, returns all joints.
        :return: List of joint control targets.
        """

        response = self._session.query_sim_rpc(
            endpoint="articulation/get_joint_targets",
            payload={"path": self._path, "joint_names": joint_names},
        )
        return [JointTarget.model_validate(jt) for jt in response] if response else []

    def get_joint_configs(self, joint_names: list[str] | None = None) -> list[ArticulationJointConfig]:
        """
        Get complete joint configurations.

        Only returns DOF joints. Non-DOF joints are automatically filtered out.
        Use the joint_name field in each config to get joint names.

        :param joint_names: Optional list of joint names. If None, returns all DOF joints.
        :return: List of joint configurations (DOF joints only).
        """

        response = self._session.query_sim_rpc(
            endpoint="articulation/get_joint_configs",
            payload={"path": self._path, "joint_names": joint_names},
        )
        return [ArticulationJointConfig.model_validate(jc) for jc in response] if response else []

    def set_joint_configs(self, joint_configs: list[ArticulationJointConfig]) -> None:
        """
        Set complete joint configurations.

        :param joint_configs: List of joint configurations to apply.
        """

        self._session.query_sim_rpc(endpoint="articulation/set_joint_configs", payload={"path": self._path, "joint_configs": joint_configs})

    def set_joint_states(self, joint_names: list[str] | None = None, joint_states: list[JointState] | None = None) -> None:
        """
        Set the joint states of the articulation (immediate teleport).

        :param joint_names: Optional list of joint names. If None, sets all joints.
        :param joint_states: List of joint states to set.
        """

        self._session.query_sim_rpc(
            endpoint="articulation/set_joint_states",
            payload={"path": self._path, "joint_names": joint_names, "joint_states": joint_states},
        )

    def set_joint_targets(self, joint_names: list[str] | None = None, joint_targets: list[JointTarget] | None = None) -> None:
        """
        Set control targets for the articulation's PD controllers.

        :param joint_names: Optional list of joint names. If None, targets all joints.
        :param joint_targets: List of joint control targets.
        """

        self._session.query_sim_rpc(
            endpoint="articulation/set_joint_targets",
            payload={"path": self._path, "joint_names": joint_names, "joint_targets": joint_targets},
        )

    def get_world_pose(self) -> Pose:
        """
        Get the world pose of the articulation.

        :return: World pose.
        """

        return self._session.query_sim_rpc(endpoint="articulation/get_world_pose", payload={"path": self._path}, response_type=Pose)

    def get_local_pose(self) -> Pose:
        """
        Get the local pose of the articulation.

        :return: Local pose.
        """

        return self._session.query_sim_rpc(endpoint="articulation/get_local_pose", payload={"path": self._path}, response_type=Pose)

    def set_world_pose(self, pose: Pose | dict) -> None:
        """
        Set the world pose of the articulation.

        :param pose: World pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(endpoint="articulation/set_world_pose", payload={"path": self._path, "pose": pose})

    def set_local_pose(self, pose: Pose | dict) -> None:
        """
        Set the local pose of the articulation.

        :param pose: Local pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(endpoint="articulation/set_local_pose", payload={"path": self._path, "pose": pose})
