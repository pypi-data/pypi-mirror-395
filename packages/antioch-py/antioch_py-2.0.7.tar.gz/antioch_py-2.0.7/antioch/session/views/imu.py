from antioch.session.session import Session, SessionContainer
from common.message import ImuSample, Pose
from common.session.views.imu import AddImu, GetImu, GetImuResponse, GetImuSample, ImuConfig


class Imu(SessionContainer):
    """
    IMU view for time-synchronized sensor data.

    Example:
        scene = Scene()
        imu = scene.get_imu(name="my_ark/my_module/my_imu")
        sample = imu.get_sample()
    """

    def __init__(self, path: str):
        """
        Initialize IMU view.

        :param path: USD path for the IMU.
        """

        super().__init__()

        self._path = self._session.query_sim_rpc(
            endpoint="get_imu",
            payload=GetImu(path=path),
            response_type=GetImuResponse,
        ).path

    @classmethod
    def add(
        cls,
        path: str,
        config: ImuConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
    ) -> "Imu":
        """
        Add IMU to the scene.

        :param path: USD path for the IMU.
        :param config: IMU configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The IMU instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="add_imu",
            payload=AddImu(
                path=path,
                config=config,
                world_pose=world_pose,
                local_pose=local_pose,
            ),
        )
        return cls(path)

    def get_sample(self) -> ImuSample | None:
        """
        Get IMU sensor sample.

        :return: IMU sensor measurements, or None if sensor data is not ready.
        """

        sample = self._session.query_sim_rpc(
            endpoint="get_imu_sample",
            payload=GetImuSample(path=self._path),
            response_type=ImuSample,
        )

        return sample
