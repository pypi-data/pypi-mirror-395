from antioch.session.session import Session, SessionContainer
from common.message import Pose
from common.session.config import GeometryConfig


class Geometry(SessionContainer):
    """
    Ergonomic wrapper for geometry operations.

    Geometry provides basic shapes (sphere, cube, cylinder, cone, capsule) with
    collision, material, and visual properties. Geometries should be added using
    scene.add_geometry() or retrieved using scene.get_geometry().

    Example:
        scene = Scene()

        # Add geometry with flexible types (lists/tuples auto-convert)
        geom = scene.add_geometry(
            path="/World/cube",
            geometry_type=GeometryType.CUBE,
            size=[1.0, 1.0, 1.0],
            color=(1.0, 0.0, 0.0),
            world_pose={"position": [0, 0, 1], "orientation": [1, 0, 0, 0]}
        )

        # For dynamic pose control, use XForm
        xform = scene.get_xform(path="/World/cube")
        pose = xform.get_world_pose()
    """

    def __init__(self, path: str):
        """
        Initialize geometry by resolving path and validating existence.

        :param path: USD path for the geometry.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="geometry/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: GeometryConfig, world_pose: Pose | None, local_pose: Pose | None) -> "Geometry":
        """
        Add geometry to the scene.

        :param path: USD path for the geometry.
        :param config: Geometry configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :return: The geometry instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="geometry/add",
            payload={"path": path, "config": config, "world_pose": world_pose, "local_pose": local_pose},
        )
        return cls(path)
