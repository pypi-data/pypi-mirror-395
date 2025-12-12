from enum import Enum

from pydantic import Field

from common.message import CameraInfo, Message, Pose


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


class GetCamera(Message):
    """
    Get an existing camera sensor.
    """

    path: str | None = Field(default=None, description="USD path of the camera prim")
    resolution: tuple[int, int] | None = Field(default=None, description="Image resolution in pixels (width, height)")


class GetCameraResponse(Message):
    """
    Response from getting a camera.
    """

    path: str


class AddCamera(Message):
    """
    Add a camera sensor.
    """

    path: str = Field(description="USD path for the camera")
    config: CameraConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")


class GetCameraFrame(Message):
    """
    Get camera frame with image data.
    """

    path: str


class BufferCameraRgbRead(Message):
    """
    Request to buffer current camera RGB frame at simulation time.
    """

    path: str


class GetBufferedCameraRgbRead(Message):
    """
    Request to get buffered camera RGB frame at or before simulation time.
    """

    path: str
    read_sim_time: float


class BufferCameraDepthRead(Message):
    """
    Request to buffer current camera depth frame at simulation time.
    """

    path: str


class GetBufferedCameraDepthRead(Message):
    """
    Request to get buffered camera depth frame at or before simulation time.
    """

    path: str
    read_sim_time: float
