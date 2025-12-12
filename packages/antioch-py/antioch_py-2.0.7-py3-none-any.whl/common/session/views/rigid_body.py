from enum import Enum

from pydantic import Field

from common.message import Message, Pose, Vector3


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


class GetRigidBody(Message):
    """
    Get an existing rigid body view from a prim with RigidBodyAPI already applied.
    """

    path: str | None = Field(default=None, description="USD path of the rigid body prim")


class GetRigidBodyResponse(Message):
    """
    Response from getting a rigid body.
    """

    path: str


class AddRigidBody(Message):
    """
    Add or apply rigid body physics to a prim.

    Note: The prim should already exist (e.g., added as geometry first).
    Collision properties are configured on the geometry, not here.
    """

    path: str = Field(description="USD path of prim to apply physics to")
    config: RigidBodyConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")
    scale: Vector3 | None = Field(default=None, description="Scale (x, y, z)")


class BodyVelocity(Message):
    """
    Body velocity.
    """

    linear: Vector3
    angular: Vector3


class GetBodyVelocity(Message):
    """
    Get body velocity.
    """

    path: str


class SetBodyVelocity(Message):
    """
    Set body velocity.
    """

    path: str
    velocity: BodyVelocity


class BoundingBox(Message):
    """
    Axis-aligned bounding box.
    """

    min: Vector3
    max: Vector3


class GetBodyBoundingBox(Message):
    """
    Get body bounding box.
    """

    path: str


class ApplyForce(Message):
    """
    Apply force to body.
    """

    path: str
    force: Vector3
    is_global: bool = True


class ApplyTorque(Message):
    """
    Apply torque to body.
    """

    path: str
    torque: Vector3
    is_global: bool = True


class ApplyForceAtPosition(Message):
    """
    Apply force at a specific position on the body.
    """

    path: str
    force: Vector3
    position: Vector3
    is_global: bool = True


class BodyDistance(Message):
    """
    Distance between two bodies.
    """

    distance: float


class GetDistanceBetweenBodies(Message):
    """
    Get distance between bodies.
    """

    path1: str
    path2: str


class GetBodyMass(Message):
    """
    Get body mass.
    """

    path: str


class BodyMass(Message):
    """
    Body mass.
    """

    mass: float


class GetBodyInertia(Message):
    """
    Get body inertia tensor.
    """

    path: str


class BodyInertia(Message):
    """
    Body inertia tensor (3x3 matrix as 9 values).
    """

    inertia: list[float]


class GetBodyCenterOfMass(Message):
    """
    Get body center of mass.
    """

    path: str


class BodyCenterOfMass(Message):
    """
    Body center of mass position and orientation.
    """

    position: Vector3
    orientation: Vector3


class EnableGravity(Message):
    """
    Enable gravity on rigid body.
    """

    path: str


class DisableGravity(Message):
    """
    Disable gravity on rigid body.
    """

    path: str


class EnablePhysics(Message):
    """
    Enable rigid body physics.
    """

    path: str


class DisablePhysics(Message):
    """
    Disable rigid body physics.
    """

    path: str
