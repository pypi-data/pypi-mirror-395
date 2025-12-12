from antioch.session.session import Session, SessionContainer
from common.message import CameraInfo, Image, Pose
from common.session.views.camera import AddCamera, CameraConfig, GetCamera, GetCameraFrame, GetCameraResponse


class Camera(SessionContainer):
    """
    Camera view for time-synchronized image capture.

    Example:
        scene = Scene()
        camera = scene.get_camera(name="my_ark/my_module/my_camera")
        frame = camera.get_frame()
    """

    def __init__(
        self,
        path: str,
        config: CameraConfig | None = None,
    ):
        """
        Initialize camera view.

        :param path: USD path for the camera.
        :param config: Optional camera config for intrinsics.
        """

        super().__init__()

        self._config = config
        self._path = self._session.query_sim_rpc(
            endpoint="get_camera",
            payload=GetCamera(path=path),
            response_type=GetCameraResponse,
        ).path

    @classmethod
    def add(
        cls,
        path: str,
        config: CameraConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
    ) -> "Camera":
        """
        Add camera to the scene.

        :param path: USD path for the camera.
        :param config: Camera configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The camera instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="add_camera",
            payload=AddCamera(
                path=path,
                config=config,
                world_pose=world_pose,
                local_pose=local_pose,
            ),
        )
        return cls(path, config)

    def get_frame(self) -> Image | None:
        """
        Get camera frame with image data.

        :return: Image (RGB or depth based on camera mode), or None if image data is not ready.
        """

        image = self._session.query_sim_rpc(
            endpoint="get_camera_frame",
            payload=GetCameraFrame(path=self._path),
            response_type=Image,
        )

        return image

    def get_camera_info(self, frame_id: str = "camera_optical_frame") -> CameraInfo | None:
        """
        Get camera info with calculated intrinsics.

        :param frame_id: The coordinate frame ID for the camera.
        :return: CameraInfo with full intrinsics and distortion parameters, or None if no config.
        """

        if self._config is None:
            return None

        return self._config.to_camera_info(frame_id=frame_id)
