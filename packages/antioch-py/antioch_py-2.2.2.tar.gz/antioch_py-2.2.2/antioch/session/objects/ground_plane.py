from antioch.session.session import Session, SessionContainer
from common.session.config import GroundPlaneConfig


class GroundPlane(SessionContainer):
    """
    Ergonomic wrapper for ground plane operations.

    Ground planes should be added using scene.add_ground_plane() or retrieved using scene.get_ground_plane().

    Note: Ground planes do not support pose modification after creation.
    Set the z_position during creation.

    Example:
        scene = Scene()

        # Add ground plane
        ground = scene.add_ground_plane(
            path="/World/Ground",
            size=5000.0,
            z_position=0.0,
            color=[0.5, 0.5, 0.5]
        )
    """

    def __init__(self, path: str):
        """
        Initialize ground plane by resolving path and validating existence.

        :param path: USD path for the ground plane.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="ground_plane/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: GroundPlaneConfig) -> "GroundPlane":
        """
        Add a ground plane to the scene.

        :param path: USD path for the ground plane.
        :param config: Ground plane configuration.
        :return: The ground plane instance.
        """

        Session.get_current().query_sim_rpc(endpoint="ground_plane/add", payload={"path": path, "config": config})
        return cls(path)
