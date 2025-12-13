from antioch.session.session import Session, SessionContainer
from common.message import PirStatus, Pose
from common.session.config import PirSensorConfig


class PirSensor(SessionContainer):
    """
    PIR (Passive Infrared) sensor object for motion detection.

    PIR sensors detect infrared radiation changes caused by moving warm objects.
    The sensor uses a 3-sensor design (center, left, right) with dual elements per sensor.

    Example:
        scene = Scene()
        pir = scene.add_pir_sensor(path="/World/pir_sensor")
        scene.play()
        scene.step(dt_us=100_000)
        status = pir.get_detection_status()
        print(f"Detected: {status.is_detected}")
    """

    def __init__(self, path: str, config: PirSensorConfig | None = None):
        """
        Initialize PIR sensor object.

        :param path: USD path for the PIR sensor.
        :param config: Optional PIR sensor config.
        """

        super().__init__()
        self._config = config
        self._session.query_sim_rpc(endpoint="pir_sensor/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: PirSensorConfig, world_pose: Pose | None, local_pose: Pose | None) -> "PirSensor":
        """
        Add PIR sensor to the scene.

        :param path: USD path for the PIR sensor.
        :param config: PIR sensor configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The PIR sensor instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="pir_sensor/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path, config)

    def get_detection_status(self) -> PirStatus:
        """
        Get current detection status.

        :return: Detection status with is_detected, signal_strength, and per-sensor details.
        """

        return PirStatus(**self._session.query_sim_rpc(endpoint="pir_sensor/get_status", payload={"path": self._path}))

    def set_debug_mode(self, enabled: bool) -> None:
        """
        Enable or disable debug ray visualization.

        When enabled, rays are drawn each update:
        - Green: Center sensor
        - Blue: Left sensor
        - Red: Right sensor
        - Cyan points at hit locations

        :param enabled: Whether to enable debug visualization.
        """

        self._session.query_sim_rpc(endpoint="pir_sensor/set_debug_mode", payload={"path": self._path, "enabled": enabled})


def set_pir_material(path: str, emissivity: float = 0.9, temperature_c: float | None = None) -> None:
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
        endpoint="pir_material/set",
        payload={"path": path, "emissivity": emissivity, "temperature_c": temperature_c},
    )
