from antioch.session.session import Session, SessionContainer
from common.message import CameraInfo, Image, Pose
from common.session.config import CameraConfig


class Camera(SessionContainer):
    """
    Camera object for time-synchronized image capture.

    Example:
        scene = Scene()
        camera = scene.get_camera(name="my_ark/my_module/my_camera")
        frame = camera.get_frame()
    """

    def __init__(self, path: str, config: CameraConfig | None = None):
        """
        Initialize camera object.

        :param path: USD path for the camera.
        :param config: Optional camera config for intrinsics.
        """

        super().__init__()
        self._config = config
        self._session.query_sim_rpc(endpoint="camera/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: CameraConfig, world_pose: Pose | None, local_pose: Pose | None) -> "Camera":
        """
        Add camera to the scene.

        :param path: USD path for the camera.
        :param config: Camera configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The camera instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="camera/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path, config)

    def get_frame(self) -> Image | None:
        """
        Get camera frame with image data.

        :return: Image (RGB or depth based on camera mode), or None if image data is not ready.
        """

        image_dict = self._session.query_sim_rpc(endpoint="camera/get_frame", payload={"path": self._path})
        return Image(**image_dict) if image_dict else None

    def get_camera_info(self, frame_id: str = "camera_optical_frame") -> CameraInfo | None:
        """
        Get camera info with calculated intrinsics.

        :param frame_id: The coordinate frame ID for the camera.
        :return: CameraInfo with full intrinsics and distortion parameters, or None if no config.
        """

        return self._config.to_camera_info(frame_id=frame_id) if self._config else None
