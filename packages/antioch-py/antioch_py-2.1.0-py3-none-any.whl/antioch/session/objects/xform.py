from antioch.session.session import Session, SessionContainer
from common.message import Pose, Vector3


class XForm(SessionContainer):
    """
    Ergonomic wrapper for xform operations.

    XForms should be added using scene.add_xform() or retrieved using scene.get_xform().

    Example:
        scene = Scene()

        # Add xform
        xform = scene.add_xform(
            path="/World/container",
            world_pose={"position": [1.0, 2.0, 3.0], "orientation": [1.0, 0.0, 0.0, 0.0]},
            scale=[2.0, 2.0, 2.0]
        )

        pose = xform.get_world_pose()
    """

    def __init__(self, path: str):
        """
        Initialize xform by resolving path and validating existence.

        :param path: USD path for the xform.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="xform/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(
        cls,
        path: str,
        world_pose: Pose | None,
        local_pose: Pose | None,
        scale: Vector3 | None,
    ) -> "XForm":
        """
        Add an xform to the scene.

        :param path: USD path for the xform.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :param scale: Optional scale.
        :return: The xform instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="xform/add",
            payload={"path": path, "world_pose": world_pose, "local_pose": local_pose, "scale": scale},
        )
        return cls(path)

    def get_world_pose(self) -> Pose:
        """
        Get the world pose of the xform.

        :return: World pose.
        """

        return self._session.query_sim_rpc(
            endpoint="xform/get_world_pose",
            payload={"path": self._path},
            response_type=Pose,
        )

    def get_local_pose(self) -> Pose:
        """
        Get the local pose of the xform.

        :return: Local pose.
        """

        return self._session.query_sim_rpc(
            endpoint="xform/get_local_pose",
            payload={"path": self._path},
            response_type=Pose,
        )

    def set_world_pose(self, pose: Pose | dict) -> None:
        """
        Set the world pose of the xform.

        :param pose: World pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(
            endpoint="xform/set_world_pose",
            payload={"path": self._path, "pose": pose},
        )

    def set_local_pose(self, pose: Pose | dict) -> None:
        """
        Set the local pose of the xform.

        :param pose: Local pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(
            endpoint="xform/set_local_pose",
            payload={"path": self._path, "pose": pose},
        )

    def set_visibility(self, visible: bool) -> None:
        """
        Set the visibility of the xform.

        :param visible: True to make visible, False to hide.
        """

        self._session.query_sim_rpc(
            endpoint="xform/set_visibility",
            payload={"path": self._path, "visible": visible},
        )
