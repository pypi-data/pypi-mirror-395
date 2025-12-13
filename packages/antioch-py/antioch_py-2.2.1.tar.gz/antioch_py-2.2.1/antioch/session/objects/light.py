from antioch.session.session import Session, SessionContainer
from common.message import Pose, Vector3
from common.session.config import LightConfig


class Light(SessionContainer):
    """
    Ergonomic wrapper for light operations.

    Lights should be added using scene.add_light() or retrieved using scene.get_light().

    Example:
        scene = Scene()

        # Add light
        light = scene.add_light(
            path="/World/Sun",
            light_type=LightType.DISTANT,
            intensity=30000.0,
            color=[1.0, 0.9, 0.8]
        )

        # Set color with a tuple
        light.set_color((0.5, 0.7, 1.0))
        pose = light.get_world_pose()
    """

    def __init__(self, path: str):
        """
        Initialize light by resolving path and validating existence.

        :param path: USD path for the light.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="light/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: LightConfig, world_pose: Pose | None, local_pose: Pose | None) -> "Light":
        """
        Add a light to the scene.

        :param path: USD path for the light.
        :param config: Light configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The light instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="light/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path)

    def get_world_pose(self) -> Pose:
        """
        Get the world pose of the light.

        :return: World pose.
        """

        return self._session.query_sim_rpc(endpoint="light/get_world_pose", payload={"path": self._path}, response_type=Pose)

    def get_local_pose(self) -> Pose:
        """
        Get the local pose of the light.

        :return: Local pose.
        """

        return self._session.query_sim_rpc(endpoint="light/get_local_pose", payload={"path": self._path}, response_type=Pose)

    def set_world_pose(self, pose: Pose | dict) -> None:
        """
        Set the world pose of the light.

        :param pose: World pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(endpoint="light/set_world_pose", payload={"path": self._path, "pose": pose})

    def set_local_pose(self, pose: Pose | dict) -> None:
        """
        Set the local pose of the light.

        :param pose: Local pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(endpoint="light/set_local_pose", payload={"path": self._path, "pose": pose})

    def set_intensity(self, intensity: float) -> None:
        """
        Set the intensity of the light.

        :param intensity: Light intensity value.
        """

        self._session.query_sim_rpc(endpoint="light/set_intensity", payload={"path": self._path, "intensity": intensity})

    def set_color(self, color: Vector3 | list[float] | tuple[float, float, float]) -> None:
        """
        Set the color of the light.

        :param color: RGB color as Vector3 (or list/tuple of 3 floats) with values 0-1.
        """

        self._session.query_sim_rpc(endpoint="light/set_color", payload={"path": self._path, "color": color})

    def enable(self) -> None:
        """
        Enable the light (make it illuminate the scene).
        """

        self._session.query_sim_rpc(endpoint="light/enable", payload={"path": self._path})

    def disable(self) -> None:
        """
        Disable the light (turn it off).
        """

        self._session.query_sim_rpc(endpoint="light/disable", payload={"path": self._path})
