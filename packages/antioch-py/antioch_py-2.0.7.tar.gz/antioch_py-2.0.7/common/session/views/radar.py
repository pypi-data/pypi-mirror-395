from pydantic import Field

from common.message import Message, Pose


class RadarConfig(Message):
    """
    Configuration for RTX radar sensor.

    All parameters can be customized with sensible defaults provided.
    """

    # Core sensor parameters
    frequency: int = Field(default=10, description="Sensor update frequency in Hz")

    # Field of view (degrees from center, so total FOV is 2x these values)
    max_azimuth: float = Field(default=66.0, description="Maximum azimuth angle in degrees (±FOV from center)")
    max_elevation: float = Field(default=20.0, description="Maximum elevation angle in degrees (±FOV from center)")

    # Range parameters
    max_range: float = Field(default=200.0, description="Maximum detection range in meters")
    range_resolution: float = Field(default=0.4, description="Range resolution in meters")

    # Angular resolution at boresight (center of FOV)
    azimuth_resolution: float = Field(default=1.3, description="Azimuth resolution at boresight in degrees")
    elevation_resolution: float = Field(default=5.0, description="Elevation resolution at boresight in degrees")

    # Noise parameters (standard deviation for Gaussian noise)
    azimuth_noise: float = Field(default=0.0, description="Azimuth measurement noise standard deviation in radians")
    range_noise: float = Field(default=0.0, description="Range measurement noise standard deviation in meters")


class GetRadar(Message):
    """
    Get an existing radar sensor.
    """

    path: str | None = Field(default=None, description="USD path of the radar prim")


class GetRadarResponse(Message):
    """
    Response from getting a radar.
    """

    path: str


class AddRadar(Message):
    """
    Add a radar sensor.
    """

    path: str = Field(description="USD path for the radar")
    config: RadarConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")


class GetRadarScan(Message):
    """
    Get radar scan data.
    """

    path: str


class SetRadarDebugMode(Message):
    """
    Enable or disable debug visualization for a radar sensor.
    """

    path: str
    enabled: bool = Field(description="Whether to enable debug visualization")


class BufferRadarRead(Message):
    """
    Request to buffer current radar scan at simulation time.
    """

    path: str


class GetBufferedRadarRead(Message):
    """
    Request to get buffered radar scan at or before simulation time.
    """

    path: str
    read_sim_time: float


class SetRadarMaterial(Message):
    """
    Set radar-specific material properties on a prim and all materials in its subtree.

    These properties define how the prim appears to radar sensors.
    Based on RTX Sensor Non-Visual Materials system.
    """

    path: str = Field(description="USD path of the prim to configure")
    reflectivity: float | None = Field(default=None, description="Radar reflectivity (0-1)")
    metallic: float | None = Field(default=None, description="Metallic property (0-1)")
    roughness: float | None = Field(default=None, description="Surface roughness (0-1)")
    backscattering: float | None = Field(default=None, description="Backscattering coefficient")
    cross_section: float | None = Field(default=None, description="Radar cross section in dBsm")
