from antioch.session.session import Session, SessionContainer
from common.message import Pose, Vector3
from common.session.sim import GetLocalPose, GetWorldPose, SetLocalPose, SetWorldPose
from common.session.views.rigid_body import (
    AddRigidBody,
    ApplyForce,
    BodyCenterOfMass,
    BodyInertia,
    BodyMass,
    BodyVelocity,
    DisableGravity,
    DisablePhysics,
    EnableGravity,
    EnablePhysics,
    GetBodyCenterOfMass,
    GetBodyInertia,
    GetBodyMass,
    GetBodyVelocity,
    GetRigidBody,
    GetRigidBodyResponse,
    RigidBodyConfig,
    SetBodyVelocity,
)


class RigidBody(SessionContainer):
    """
    Ergonomic wrapper for rigid body operations.

    Rigid bodies should be added using scene.add_rigid_body() or retrieved using scene.get_rigid_body().

    Example:
        scene = Scene()

        # Add rigid body
        body = scene.add_rigid_body(
            path="/World/cube",
            mass=1.0,
            linear_velocity=[1.0, 0.0, 0.0]
        )

        # Set velocity with tuples/lists
        body.set_velocity(
            linear=(1.0, 0.0, 0.0),
            angular=[0.0, 0.0, 1.0]
        )
        pose = body.get_world_pose()
    """

    def __init__(self, path: str):
        """
        Initialize rigid body by resolving path and validating existence.

        :param path: USD path for the rigid body.
        """

        super().__init__()

        # Validate path
        self._path = self._session.query_sim_rpc(
            endpoint="get_rigid_body",
            payload=GetRigidBody(path=path),
            response_type=GetRigidBodyResponse,
        ).path

    @classmethod
    def add(
        cls,
        path: str,
        config: RigidBodyConfig,
        world_pose: Pose | None,
        local_pose: Pose | None,
        scale: Vector3 | None,
    ) -> "RigidBody":
        """
        Add a rigid body to the scene.

        :param path: USD path for the rigid body.
        :param config: Rigid body configuration.
        :param world_pose: Optional world pose.
        :param local_pose: Optional local pose.
        :param scale: Optional scale.
        :return: The rigid body instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="add_rigid_body",
            payload=AddRigidBody(
                path=path,
                config=config,
                world_pose=world_pose,
                local_pose=local_pose,
                scale=scale,
            ),
        )
        return cls(path)

    def get_velocity(self) -> BodyVelocity:
        """
        Get the velocity of the rigid body.

        :return: Linear and angular velocities.
        """

        return self._session.query_sim_rpc(
            endpoint="get_body_velocity",
            payload=GetBodyVelocity(path=self._path),
            response_type=BodyVelocity,
        )

    def set_velocity(
        self,
        linear: Vector3 | list[float] | tuple[float, float, float],
        angular: Vector3 | list[float] | tuple[float, float, float],
    ) -> None:
        """
        Set the velocity of the rigid body.

        :param linear: Linear velocity as Vector3 (or list/tuple of 3 floats).
        :param angular: Angular velocity as Vector3 (or list/tuple of 3 floats).
        """

        self._session.query_sim_rpc(
            endpoint="set_body_velocity",
            payload=SetBodyVelocity(
                path=self._path,
                velocity=BodyVelocity(
                    linear=Vector3.from_any(linear),
                    angular=Vector3.from_any(angular),
                ),
            ),
        )

    def apply_force(
        self,
        force: Vector3 | list[float] | tuple[float, float, float],
        is_global: bool = True,
    ) -> None:
        """
        Apply force to the rigid body.

        :param force: Force vector as Vector3 (or list/tuple of 3 floats).
        :param is_global: Whether force is in global frame.
        """

        self._session.query_sim_rpc(
            endpoint="apply_force",
            payload=ApplyForce(
                path=self._path,
                force=Vector3.from_any(force),
                is_global=is_global,
            ),
        )

    def get_mass(self) -> float:
        """
        Get the mass of the rigid body.

        :return: Mass in kg.
        """

        return self._session.query_sim_rpc(
            endpoint="get_body_mass",
            payload=GetBodyMass(path=self._path),
            response_type=BodyMass,
        ).mass

    def get_inertia(self) -> list[float]:
        """
        Get the inertia tensor of the rigid body.

        :return: Inertia tensor as 9 values (3x3 matrix flattened).
        """

        return self._session.query_sim_rpc(
            endpoint="get_body_inertia",
            payload=GetBodyInertia(path=self._path),
            response_type=BodyInertia,
        ).inertia

    def get_center_of_mass(self) -> BodyCenterOfMass:
        """
        Get the center of mass position and orientation.

        :return: Center of mass position and orientation.
        """

        return self._session.query_sim_rpc(
            endpoint="get_body_center_of_mass",
            payload=GetBodyCenterOfMass(path=self._path),
            response_type=BodyCenterOfMass,
        )

    def enable_gravity(self) -> None:
        """
        Enable gravity on the rigid body.
        """

        self._session.query_sim_rpc(
            endpoint="enable_gravity",
            payload=EnableGravity(path=self._path),
        )

    def disable_gravity(self) -> None:
        """
        Disable gravity on the rigid body.
        """

        self._session.query_sim_rpc(
            endpoint="disable_gravity",
            payload=DisableGravity(path=self._path),
        )

    def enable_physics(self) -> None:
        """
        Enable rigid body physics (make body dynamic).
        """

        self._session.query_sim_rpc(
            endpoint="enable_physics",
            payload=EnablePhysics(path=self._path),
        )

    def disable_physics(self) -> None:
        """
        Disable rigid body physics (make body kinematic).
        """

        self._session.query_sim_rpc(
            endpoint="disable_physics",
            payload=DisablePhysics(path=self._path),
        )

    def get_world_pose(self) -> Pose:
        """
        Get the world pose of the rigid body.

        :return: World pose.
        """

        return self._session.query_sim_rpc(
            endpoint="get_rigid_body_world_pose",
            payload=GetWorldPose(path=self._path),
            response_type=Pose,
        )

    def get_local_pose(self) -> Pose:
        """
        Get the local pose of the rigid body.

        :return: Local pose.
        """

        return self._session.query_sim_rpc(
            endpoint="get_rigid_body_local_pose",
            payload=GetLocalPose(path=self._path),
            response_type=Pose,
        )

    def set_world_pose(self, pose: Pose | dict) -> None:
        """
        Set the world pose of the rigid body.

        :param pose: World pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(
            endpoint="set_rigid_body_world_pose",
            payload=SetWorldPose(path=self._path, pose=Pose.from_any(pose)),
        )

    def set_local_pose(self, pose: Pose | dict) -> None:
        """
        Set the local pose of the rigid body.

        :param pose: Local pose as Pose (or dict with position/orientation lists).
        """

        self._session.query_sim_rpc(
            endpoint="set_rigid_body_local_pose",
            payload=SetLocalPose(path=self._path, pose=Pose.from_any(pose)),
        )
