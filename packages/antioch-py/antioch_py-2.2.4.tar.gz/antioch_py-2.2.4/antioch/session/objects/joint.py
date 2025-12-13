from antioch.session.session import Session, SessionContainer
from common.session.config import JointConfig


class Joint(SessionContainer):
    """
    Ergonomic wrapper for joint operations.

    Joints connect two bodies and define kinematic constraints between them.
    Joints should be added using scene.add_joint() or retrieved using scene.get_joint().

    Example:
        scene = Scene()

        # Add a revolute joint between two bodies
        joint = scene.add_joint(
            path="/World/robot/joint1",
            parent_path="/World/robot/link1",
            child_path="/World/robot/link2",
            joint_type=JointType.REVOLUTE,
            axis=JointAxis.Z,
            lower_limit=-180.0,
            upper_limit=180.0,
        )
    """

    def __init__(self, path: str):
        """
        Initialize joint by resolving path and validating existence.

        :param path: USD path for the joint.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="joint/get", payload={"path": path})
        self._path = path

    @classmethod
    def add(cls, path: str, config: JointConfig) -> "Joint":
        """
        Add a joint to the scene.

        :param path: USD path for the joint.
        :param config: Joint configuration.
        :return: The joint instance.
        """

        Session.get_current().query_sim_rpc(endpoint="joint/add", payload={"path": path, "config": config})
        return cls(path)
