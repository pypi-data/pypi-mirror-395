from enum import Enum

from pydantic import Field
from pydantic.alias_generators import to_camel

from common.message import CameraInfo, Message, Pose, Vector3


class GeometryType(str, Enum):
    """
    Supported geometry types.
    """

    SPHERE = "sphere"
    CUBE = "cube"
    CYLINDER = "cylinder"
    CONE = "cone"
    CAPSULE = "capsule"
    MESH = "mesh"


class MeshApproximation(str, Enum):
    """
    Collision mesh approximation type.

    Values are stored in snake_case for consistency with Rust. Use to_usd()
    to get the camelCase format required by USD/Isaac Sim.
    """

    NONE = "none"
    CONVEX_HULL = "convex_hull"
    CONVEX_DECOMPOSITION = "convex_decomposition"
    BOUNDING_SPHERE = "bounding_sphere"
    BOUNDING_CUBE = "bounding_cube"
    MESH_SIMPLIFICATION = "mesh_simplification"
    SDF = "sdf"
    SPHERE_FILL = "sphere_fill"

    def to_usd(self) -> str:
        """
        Convert to USD camelCase format.

        :return: The USD camelCase format.
        """

        return to_camel(self.value)


class GeometryConfig(Message):
    """
    Configuration for creating geometry.
    """

    geometry_type: GeometryType = Field(description="Geometry type")
    radius: float | None = Field(default=None, description="Radius for sphere/cylinder/cone/capsule")
    height: float | None = Field(default=None, description="Height for cylinder/cone/capsule")
    size: float | None = Field(default=None, description="Size for cube (uniform)")
    color: Vector3 | None = Field(default=None, description="RGB color (0-1)")
    opacity: float = Field(default=1.0, description="Opacity (0=transparent, 1=opaque)")
    enable_collision: bool = Field(default=True, description="Whether to enable collision on this geometry")
    static_friction: float = Field(default=0.5, description="Static friction coefficient")
    dynamic_friction: float = Field(default=0.5, description="Dynamic friction coefficient")
    restitution: float = Field(default=0.2, description="Restitution (bounciness)")
    mesh_file_path: str | None = Field(default=None, description="Path to mesh file (FBX, OBJ, glTF, STL, etc.) - required for MESH type")
    mesh_approximation: MeshApproximation = Field(default=MeshApproximation.CONVEX_DECOMPOSITION, description="Mesh approximation method")
    contact_offset: float | None = Field(default=None, description="Distance at which collision detection begins")
    rest_offset: float | None = Field(default=None, description="Minimum separation distance between objects")
    torsional_patch_radius: float | None = Field(default=None, description="Radius for torsional friction calculations")
    min_torsional_patch_radius: float | None = Field(default=None, description="Minimum radius for torsional friction")


class CameraMode(str, Enum):
    """
    Camera capture modes.
    """

    RGB = "rgb"
    DEPTH = "depth"


class DistortionModel(str, Enum):
    """
    Camera lens distortion model types.
    """

    PINHOLE = "pinhole"
    OPENCV_PINHOLE = "opencv_pinhole"
    OPENCV_FISHEYE = "opencv_fisheye"
    FTHETA = "ftheta"
    KANNALA_BRANDT_K3 = "kannala_brandt_k3"
    RAD_TAN_THIN_PRISM = "rad_tan_thin_prism"


class CameraConfig(Message):
    """
    Configuration for camera sensor.
    """

    mode: CameraMode = Field(default=CameraMode.RGB, description="Camera capture mode (RGB or depth)")
    frequency: int = Field(default=30, description="Camera update frequency in Hz")
    width: int = Field(default=640, description="Image width in pixels")
    height: int = Field(default=480, description="Image height in pixels")
    focal_length: float = Field(default=50.0, description="Focal length in mm")
    sensor_width: float = Field(default=20.4, description="Physical sensor width in mm")
    sensor_height: float = Field(default=15.3, description="Physical sensor height in mm")
    near_clip: float = Field(default=0.1, description="Near clipping plane in meters")
    far_clip: float = Field(default=1000.0, description="Far clipping plane in meters")
    f_stop: float = Field(default=0.0, description="F-stop for depth of field")
    focus_distance: float = Field(default=10.0, description="Focus distance in meters")
    principal_point_x: float = Field(default=0.0, description="Principal point X offset in pixels")
    principal_point_y: float = Field(default=0.0, description="Principal point Y offset in pixels")
    distortion_model: DistortionModel = Field(default=DistortionModel.PINHOLE, description="Lens distortion model")
    distortion_coefficients: list[float] | None = Field(default=None, description="Distortion coefficients")

    def to_camera_info(self, frame_id: str = "camera_optical_frame") -> CameraInfo:
        """
        Convert camera configuration to CameraInfo with calculated intrinsics.

        :param frame_id: The coordinate frame ID for the camera.
        :return: CameraInfo with full intrinsics and distortion parameters.
        """

        # Convert mm to pixels for focal length
        fx = self.width * self.focal_length / self.sensor_width
        fy = self.height * self.focal_length / self.sensor_height

        # Principal point (image center + offset)
        cx = self.width / 2.0 + self.principal_point_x
        cy = self.height / 2.0 + self.principal_point_y

        return CameraInfo(
            width=self.width,
            height=self.height,
            fx=fx,
            fy=fy,
            cx=cx,
            cy=cy,
            distortion_model=self.distortion_model.value,
            distortion_coefficients=self.distortion_coefficients or [],
            frame_id=frame_id,
        )


class ArticulationJointConfig(Message):
    """
    Complete configuration for a single joint in an articulation.
    """

    path: str = Field(description="Name of the joint/DOF")
    stiffness: float | None = Field(default=None, description="PD controller stiffness (Kp)")
    damping: float | None = Field(default=None, description="PD controller damping (Kd)")
    lower_limit: float | None = Field(default=None, description="Lower joint limit")
    upper_limit: float | None = Field(default=None, description="Upper joint limit")
    armature: float | None = Field(default=None, description="Joint armature")
    friction_coefficient: float | None = Field(default=None, description="Joint friction coefficient")
    max_velocity: float | None = Field(default=None, description="Maximum joint velocity")
    max_effort: float | None = Field(default=None, description="Maximum joint effort")


class ArticulationConfig(Message):
    """
    Configuration for applying articulation root to a prim.
    """

    solver_position_iterations: int = Field(default=32, description="Number of position iterations for the solver")
    solver_velocity_iterations: int = Field(default=1, description="Number of velocity iterations for the solver")
    sleep_threshold: float = Field(default=0.005, description="Sleep threshold for the articulation")
    stabilization_threshold: float = Field(default=0.001, description="Stabilization threshold for the articulation")
    enable_self_collisions: bool = Field(default=False, description="Whether to enable self-collisions")
    joint_configs: list[ArticulationJointConfig] = Field(default_factory=list, description="Per-joint configurations")


class JointType(str, Enum):
    """
    Types of joints supported by the simulator.
    """

    REVOLUTE = "revolute"
    PRISMATIC = "prismatic"
    FIXED = "fixed"
    SPHERICAL = "spherical"
    DISTANCE = "distance"
    GENERIC = "generic"


class JointAxis(str, Enum):
    """
    Axis of motion for joints.
    """

    X = "x"
    Y = "y"
    Z = "z"


class JointConfig(Message):
    """
    Configuration for a joint object that connects two bodies.
    """

    # Joint relationships
    parent_path: str = Field(description="USD path to parent body")
    child_path: str = Field(description="USD path to child body")

    # Transform
    pose: Pose = Field(default_factory=Pose.identity, description="Joint pose relative to parent")

    # Joint properties
    joint_type: JointType = Field(default=JointType.FIXED, description="Type of joint motion allowed")
    axis: JointAxis = Field(default=JointAxis.X, description="Axis of motion for non-fixed joints")

    # Motion limits (for revolute: degrees, for prismatic: meters)
    lower_limit: float | None = Field(default=None, description="Lower motion limit")
    upper_limit: float | None = Field(default=None, description="Upper motion limit")

    # Physics properties
    friction: float = Field(default=0.01, description="Joint friction (unitless)")
    armature: float = Field(default=0.1, description="Joint armature (kg for prismatic, kg-m^2 for revolute)")

    # Special properties
    exclude_from_articulation: bool = Field(default=False, description="Whether to exclude this joint from articulation")


class BodyType(str, Enum):
    """
    Type of rigid body.
    """

    DYNAMIC = "dynamic"
    KINEMATIC = "kinematic"


class RigidBodyConfig(Message):
    """
    Configuration for rigid body physics properties.

    Note: Collision properties (friction, restitution, mesh approximation) are configured
    on the geometry, not the rigid body.
    """

    body_type: BodyType = Field(default=BodyType.DYNAMIC, description="Type of rigid body")
    mass: float = Field(default=1.0, description="Mass in kg")
    density: float | None = Field(default=None, description="Density in kg/m³ (alternative to mass)")
    center_of_mass: Vector3 | None = Field(default=None, description="Center of mass offset in body frame")
    diagonal_inertia: Vector3 | None = Field(default=None, description="Diagonal inertia values (Ixx, Iyy, Izz)")
    principal_axes: Vector3 | None = Field(default=None, description="Principal axes orientation as RPY")
    sleep_threshold: float | None = Field(default=None, description="Mass-normalized kinetic energy threshold for sleeping")
    linear_velocity: Vector3 | None = Field(default=None, description="Initial linear velocity")
    angular_velocity: Vector3 | None = Field(default=None, description="Initial angular velocity")


class LightType(str, Enum):
    """
    Supported light types.
    """

    SPHERE = "sphere"
    RECT = "rect"
    DISK = "disk"
    CYLINDER = "cylinder"
    DISTANT = "distant"
    DOME = "dome"


class LightConfig(Message):
    """
    Configuration for creating a light.
    """

    light_type: LightType = Field(default=LightType.SPHERE, description="Light type")
    intensity: float = Field(default=30000.0, description="Light intensity")
    exposure: float = Field(default=10.0, description="Light exposure")
    color: Vector3 = Field(default_factory=Vector3.ones, description="RGB color (0-1)")
    radius: float = Field(default=0.1, description="Radius for sphere lights (meters)")
    width: float | None = Field(default=None, description="Width for rect lights (meters)")
    height: float | None = Field(default=None, description="Height for rect/cylinder lights (meters)")
    length: float | None = Field(default=None, description="Length for cylinder lights (meters)")
    angle: float | None = Field(default=None, description="Angle for distant lights (degrees)")
    texture_file: str | None = Field(default=None, description="Texture file for dome lights")


class GroundPlaneConfig(Message):
    """
    Configuration for creating a ground plane.
    """

    size: float = Field(default=5000.0, description="Size of the ground plane in meters")
    z_position: float = Field(default=0.0, description="Z position of the ground plane")
    color: Vector3 = Field(default=Vector3.new(0.5, 0.5, 0.5), description="RGB color (0-1)")
    static_friction: float = Field(default=0.5, description="Static friction coefficient")
    dynamic_friction: float = Field(default=0.5, description="Dynamic friction coefficient")
    restitution: float = Field(default=0.0, description="Restitution (bounciness)")


class ImuConfig(Message):
    """
    Configuration for IMU sensor.
    """

    frequency: int | None = Field(default=None, description="Sensor update frequency in Hz (optional, defaults to physics rate)")
    linear_acceleration_filter_size: int = Field(default=10, description="Filter window size for linear acceleration")
    angular_velocity_filter_size: int = Field(default=10, description="Filter window size for angular velocity")
    orientation_filter_size: int = Field(default=10, description="Filter window size for orientation")


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


class PirSensorConfig(Message):
    """
    Configuration for PIR (Passive Infrared) motion sensor.

    PIR sensors detect infrared radiation changes caused by moving warm objects.
    The sensor uses a 3-sensor design (center, left, right) with dual elements per sensor.
    """

    # Core sensor parameters
    update_rate_hz: float = Field(default=60.0, description="Sensor update frequency in Hz")
    max_range: float = Field(default=20.0, description="Maximum detection range in meters")

    # FOV configuration
    total_horiz_fov_deg: float = Field(default=150.0, description="Total horizontal coverage")
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

    # Hard-coded threshold (if not none) overrides auto-calibration
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
