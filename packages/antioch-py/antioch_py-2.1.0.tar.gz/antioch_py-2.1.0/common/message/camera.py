import numpy as np
from pydantic import Field

from common.message.base import Message


class CameraInfo(Message):
    """
    Complete camera information including intrinsics, distortion, and projection.

    Follows standard camera calibration conventions with support for various
    distortion models and projection operations.
    """

    _type = "antioch/camera_info"

    # Image dimensions
    width: int = Field(description="Image width in pixels")
    height: int = Field(description="Image height in pixels")

    # Intrinsic parameters
    fx: float = Field(description="Focal length in x (pixels)")
    fy: float = Field(description="Focal length in y (pixels)")
    cx: float = Field(description="Principal point x (pixels)")
    cy: float = Field(description="Principal point y (pixels)")

    # Distortion model and coefficients
    distortion_model: str = Field(default="pinhole", description="Distortion model name")
    distortion_coefficients: list[float] = Field(default_factory=list, description="Distortion coefficients")

    # Frame information
    frame_id: str = Field(default="camera_optical_frame", description="Camera coordinate frame")

    @property
    def intrinsics_matrix(self) -> np.ndarray:
        """
        Get the 3x3 camera intrinsics matrix K.

        Returns:
            [[fx,  0, cx],
             [ 0, fy, cy],
             [ 0,  0,  1]]
        """

        return np.array([[self.fx, 0.0, self.cx], [0.0, self.fy, self.cy], [0.0, 0.0, 1.0]])

    def unproject_pixel(self, u: float, v: float, depth: float) -> np.ndarray:
        """
        Unproject a pixel coordinate to 3D point using the camera intrinsics.

        Note: This assumes no distortion. For distorted images, undistort first.

        :param u: Pixel x-coordinate.
        :param v: Pixel y-coordinate.
        :param depth: Depth value at the pixel in meters.
        :return: 3D point [x, y, z] in camera frame.
        """

        x = (u - self.cx) * depth / self.fx
        y = (v - self.cy) * depth / self.fy
        return np.array([x, y, depth])

    def project_point(self, point: np.ndarray) -> tuple[float, float]:
        """
        Project a 3D point to pixel coordinates.

        Note: This assumes no distortion. For accurate projection with distortion,
        additional processing is required.

        :param point: 3D point [x, y, z] in camera frame.
        :return: Pixel coordinates (u, v).
        :raises ValueError: If point is behind camera.
        """

        if point[2] <= 0:
            raise ValueError("Point must be in front of camera (z > 0)")

        u = self.fx * point[0] / point[2] + self.cx
        v = self.fy * point[1] / point[2] + self.cy
        return (u, v)

    def is_point_visible(self, u: float, v: float) -> bool:
        """
        Check if a pixel coordinate is within the image bounds.

        :param u: Pixel x-coordinate.
        :param v: Pixel y-coordinate.
        :return: True if point is visible in the image.
        """

        return 0 <= u < self.width and 0 <= v < self.height
