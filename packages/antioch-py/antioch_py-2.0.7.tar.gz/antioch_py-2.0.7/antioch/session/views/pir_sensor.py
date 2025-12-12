from antioch.session.session import Session, SessionContainer
from common.message import PirStatus, Pose
from common.session.views.pir_sensor import (
    AddPirSensor,
    GetPirDetectionStatus,
    GetPirSensor,
    GetPirSensorResponse,
    PirSensorConfig,
    SetPirDebugMode,
    SetPirMaterial,
)


class PirSensor(SessionContainer):
    """
    PIR (Passive Infrared) sensor view for motion detection.

    PIR sensors detect infrared radiation changes caused by moving warm objects.
    The sensor uses a dual-element design with interleaved zones for motion detection.

    Example:
        scene = Scene()
        pir = scene.add_pir_sensor(path="/World/pir_sensor")
        scene.play()
        scene.step(dt_us=100_000)
        status = pir.get_detection_status()
        print(f"Detected: {status.is_detected}")
    """

    def __init__(
        self,
        path: str,
        config: PirSensorConfig | None = None,
    ):
        """
        Initialize PIR sensor view.

        :param path: USD path for the PIR sensor.
        :param config: Optional PIR sensor config.
        """

        super().__init__()

        self._config = config
        self._path = self._session.query_sim_rpc(
            endpoint="get_pir_sensor",
            payload=GetPirSensor(path=path),
            response_type=GetPirSensorResponse,
        ).path

    @classmethod
    def add(
        cls,
        path: str,
        config: PirSensorConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
    ) -> "PirSensor":
        """
        Add PIR sensor to the scene.

        :param path: USD path for the PIR sensor.
        :param config: PIR sensor configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The PIR sensor instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="add_pir_sensor",
            payload=AddPirSensor(
                path=path,
                config=config,
                world_pose=world_pose,
                local_pose=local_pose,
            ),
        )
        return cls(path, config)

    def get_detection_status(self) -> PirStatus:
        """
        Get current detection status.

        :return: Detection status with is_detected, signal_strength, threshold, element_flux, and element_signal.
        """

        status = self._session.query_sim_rpc(
            endpoint="get_pir_detection_status",
            payload=GetPirDetectionStatus(path=self._path),
            response_type=PirStatus,
        )
        return status

    def set_debug_mode(self, enabled: bool) -> None:
        """
        Enable or disable debug ray visualization.

        When enabled, rays are drawn each update:
        - Red rays for element 0
        - Blue rays for element 1
        - Green points at hit locations

        :param enabled: Whether to enable debug visualization.
        """

        self._session.query_sim_rpc(
            endpoint="set_pir_debug_mode",
            payload=SetPirDebugMode(path=self._path, enabled=enabled),
        )


def set_pir_material(
    path: str,
    emissivity: float = 0.9,
    temperature_c: float | None = None,
) -> None:
    """
    Set PIR-specific thermal properties on a prim.

    These properties define how the prim appears to PIR sensors:
    - emissivity: How well the surface emits infrared radiation (0-1)
    - temperature_c: Surface temperature in Celsius

    Example:
        # Make a target detectable by PIR sensors
        set_pir_material("/World/person", emissivity=0.98, temperature_c=37.0)

    :param path: USD path of the prim to configure.
    :param emissivity: Material emissivity (0-1, default 0.9).
    :param temperature_c: Surface temperature in Celsius (optional).
    """

    Session.get_current().query_sim_rpc(
        endpoint="set_pir_material",
        payload=SetPirMaterial(
            path=path,
            emissivity=emissivity,
            temperature_c=temperature_c,
        ),
    )
