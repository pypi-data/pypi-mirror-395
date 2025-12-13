from antioch.session.session import Session, SessionContainer
from common.message import Pose, RadarScan
from common.session.config import RadarConfig


class Radar(SessionContainer):
    """
    Radar object for time-synchronized scan data.

    Example:
        scene = Scene()
        radar = scene.get_radar(name="my_ark/my_module/my_radar")
        scan = radar.get_scan()
    """

    def __init__(self, path: str):
        """
        Initialize Radar object.

        :param path: USD path for the radar.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="radar/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: RadarConfig, world_pose: Pose | None, local_pose: Pose | None) -> "Radar":
        """
        Add radar to the scene.

        :param path: USD path for the radar.
        :param config: Radar configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The radar instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="radar/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path)

    def get_scan(self) -> RadarScan | None:
        """
        Get radar scan data.

        :return: Radar scan with detections, or None if scan data is not ready.
        """

        scan = self._session.query_sim_rpc(endpoint="radar/get_scan", payload={"path": self._path})
        return RadarScan(**scan) if scan else None

    def set_debug_mode(self, enabled: bool) -> None:
        """
        Enable or disable debug visualization.

        :param enabled: Whether to enable debug visualization.
        """

        self._session.query_sim_rpc(endpoint="radar/set_debug_mode", payload={"path": self._path, "enabled": enabled})
