from pydantic import Field

from common.message import Message, Pose


class PirSensorConfig(Message):
    """
    Configuration for PIR (Passive Infrared) motion sensor.

    PIR sensors detect infrared radiation changes caused by moving warm objects.
    The sensor uses a dual-element design with interleaved zones for motion detection.
    """

    # Core sensor parameters
    update_rate_hz: float = Field(default=60.0, description="Sensor update frequency in Hz")
    max_range: float = Field(default=20.0, description="Maximum detection range in meters")

    # FOV configuration
    total_horiz_fov_deg: float = Field(default=150.0, description="Total horizontal coverage. Enables automatic fanning.")
    sensor_side_fov_deg: float = Field(default=45.0, description="Horizontal FOV for side sensors")
    sensor_center_fov_deg: float = Field(default=45.0, description="Horizontal FOV for center sensor")

    # Ray configuration
    sensor_rays_horiz: int = Field(default=128, description="Number of rays per sensor in horizontal direction")
    sensor_rays_vert: int = Field(default=16, description="Number of rays per sensor in vertical direction")

    # Sensor vertical angle range
    min_vertical_angle_center: float = Field(default=-30.0, description="Minimum vertical angle for center sensor in degrees")
    max_vertical_angle_center: float = Field(default=30.0, description="Maximum vertical angle for center sensor in degrees")
    min_vertical_angle_side: float = Field(default=-30.0, description="Minimum vertical angle for side sensors in degrees")
    max_vertical_angle_side: float = Field(default=30.0, description="Maximum vertical angle for side sensors in degrees")

    # DSP / electronics parameters
    gain_center: float = Field(default=0.015, description="Amplifier gain for center sensor")
    gain_sides: float = Field(default=0.01, description="Amplifier gain for side sensors")
    hp_corner_hz: float = Field(default=0.4, description="High-pass filter corner frequency in Hz")
    lp_corner_hz: float = Field(default=10.0, description="Low-pass filter corner frequency in Hz")
    blind_time_s: float = Field(default=0.5, description="Blind time after detection in seconds")
    pulse_counter: int = Field(default=2, description="Number of pulses required to trigger detection (1-4)")
    window_time_s: float = Field(default=2.0, description="Window time for pulse counting in seconds")
    count_mode: int = Field(default=0, description="Pulse counting mode (0: sign change required, 1: any crossing)")

    # Lens parameters
    lens_transmission: float = Field(default=0.9, description="Lens transmission coefficient (0-1)")
    lens_segments_h: int = Field(default=6, description="Number of horizontal lens segments (facets)")

    # Environment parameters
    ambient_temp_c: float = Field(default=20.0, description="Ambient temperature in Celsius")

    # Hard-coded theshold (if not none) overrides auto-calibration
    threshold: float | None = Field(default=None, description="Detection threshold (auto-calibrated if None)")
    threshold_scale: float = Field(default=1.0, description="Scale factor applied to auto-calibrated threshold")

    # Pyroelectric element parameters
    thermal_time_constant_s: float = Field(default=0.2, description="Element thermal time constant in seconds")
    pyro_responsivity: float = Field(default=4000.0, description="Pyroelectric responsivity scaling factor")
    noise_amplitude: float = Field(default=20e-6, description="Thermal/electronic noise amplitude")

    # Auto-threshold calibration parameters
    target_delta_t: float = Field(default=10.0, description="Target temperature difference for threshold calibration in Celsius")
    target_distance: float = Field(default=5.0, description="Target distance for threshold calibration in meters")
    target_emissivity: float = Field(default=0.98, description="Target emissivity for threshold calibration")
    target_velocity_mps: float = Field(default=1.0, description="Target velocity for threshold calibration in m/s")


class GetPirSensor(Message):
    """
    Get an existing PIR sensor.
    """

    path: str | None = Field(default=None, description="USD path of the PIR sensor prim")


class GetPirSensorResponse(Message):
    """
    Response from getting a PIR sensor.
    """

    path: str


class AddPirSensor(Message):
    """
    Add a PIR sensor.
    """

    path: str = Field(description="USD path for the PIR sensor")
    config: PirSensorConfig = Field(default_factory=PirSensorConfig)
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")


class GetPirDetectionStatus(Message):
    """
    Get PIR sensor detection status.
    """

    path: str


class SetPirDebugMode(Message):
    """
    Enable or disable debug visualization for a PIR sensor.
    """

    path: str
    enabled: bool = Field(description="Whether to enable debug ray visualization")


class SetPirMaterial(Message):
    """
    Set PIR-specific thermal properties on a prim.

    These properties define how the prim appears to PIR sensors.
    """

    path: str = Field(description="USD path of the prim to configure")
    emissivity: float = Field(default=0.9, description="Material emissivity (0-1)")
    temperature_c: float | None = Field(default=None, description="Surface temperature in Celsius")
