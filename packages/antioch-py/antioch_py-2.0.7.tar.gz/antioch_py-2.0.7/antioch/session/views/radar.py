from antioch.session.session import Session, SessionContainer
from common.message import Pose, RadarScan
from common.session.views.radar import (
    AddRadar,
    GetRadar,
    GetRadarResponse,
    GetRadarScan,
    RadarConfig,
    SetRadarDebugMode,
    SetRadarMaterial,
)


class Radar(SessionContainer):
    """
    Radar view for time-synchronized scan data.

    Example:
        scene = Scene()
        radar = scene.get_radar(name="my_ark/my_module/my_radar")
        scan = radar.get_scan()
    """

    def __init__(self, path: str):
        """
        Initialize Radar view.

        :param path: USD path for the radar.
        """

        super().__init__()

        self._path = self._session.query_sim_rpc(
            endpoint="get_radar",
            payload=GetRadar(path=path),
            response_type=GetRadarResponse,
        ).path

    @classmethod
    def add(
        cls,
        path: str,
        config: RadarConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
    ) -> "Radar":
        """
        Add radar to the scene.

        :param path: USD path for the radar.
        :param config: Radar configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The radar instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="add_radar",
            payload=AddRadar(
                path=path,
                config=config,
                world_pose=world_pose,
                local_pose=local_pose,
            ),
        )
        return cls(path)

    def get_scan(self) -> RadarScan | None:
        """
        Get radar scan data.

        :return: Radar scan with detections, or None if scan data is not ready.
        """

        scan = self._session.query_sim_rpc(
            endpoint="get_radar_scan",
            payload=GetRadarScan(path=self._path),
            response_type=RadarScan,
        )

        return scan

    def set_debug_mode(self, enabled: bool) -> None:
        """
        Enable or disable debug visualization.

        :param enabled: Whether to enable debug visualization.
        """

        self._session.query_sim_rpc(
            endpoint="set_radar_debug_mode",
            payload=SetRadarDebugMode(path=self._path, enabled=enabled),
        )


def set_radar_material(
    path: str,
    reflectivity: float | None = None,
    metallic: float | None = None,
    roughness: float | None = None,
    backscattering: float | None = None,
    cross_section: float | None = None,
) -> None:
    """
    Set radar-specific material properties on a prim and all prims in its subtree.

    These properties define how the prim appears to radar sensors.

    Example:
        # Make a target highly reflective to radar
        set_radar_material("/World/car", reflectivity=0.9, metallic=1.0)

    :param path: USD path of the prim to configure.
    :param reflectivity: Radar reflectivity (0-1).
    :param metallic: Metallic property (0-1).
    :param roughness: Surface roughness (0-1).
    :param backscattering: Backscattering coefficient.
    :param cross_section: Radar cross section in dBsm.
    """

    Session.get_current().query_sim_rpc(
        endpoint="set_radar_material",
        payload=SetRadarMaterial(
            path=path,
            reflectivity=reflectivity,
            metallic=metallic,
            roughness=roughness,
            backscattering=backscattering,
            cross_section=cross_section,
        ),
    )
