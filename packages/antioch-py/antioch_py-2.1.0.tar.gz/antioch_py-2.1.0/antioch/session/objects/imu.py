from antioch.session.session import Session, SessionContainer
from common.message import ImuSample, Pose
from common.session.config import ImuConfig


class Imu(SessionContainer):
    """
    IMU object for time-synchronized sensor data.

    Example:
        scene = Scene()
        imu = scene.get_imu(name="my_ark/my_module/my_imu")
        sample = imu.get_sample()
    """

    def __init__(self, path: str):
        """
        Initialize IMU object.

        :param path: USD path for the IMU.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="imu/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: ImuConfig, world_pose: Pose | None, local_pose: Pose | None) -> "Imu":
        """
        Add IMU to the scene.

        :param path: USD path for the IMU.
        :param config: IMU configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The IMU instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="imu/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path)

    def get_sample(self) -> ImuSample | None:
        """
        Get IMU sensor sample.

        :return: IMU sensor measurements, or None if sensor data is not ready.
        """

        sample = self._session.query_sim_rpc(endpoint="imu/get_sample", payload={"path": self._path})
        return ImuSample(**sample) if sample else None
