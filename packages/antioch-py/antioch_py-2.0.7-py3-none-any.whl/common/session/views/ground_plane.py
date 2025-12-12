from pydantic import Field

from common.message import Message, Vector3


class GroundPlaneConfig(Message):
    """
    Configuration for creating a ground plane.
    """

    size: float = Field(default=5000.0, description="Size of the ground plane in meters")
    z_position: float = Field(default=0.0, description="Z position of the ground plane")
    color: Vector3 = Field(default=Vector3.new(0.5, 0.5, 0.5), description="RGB color (0-1)")
    static_friction: float = Field(default=0.5, description="Static friction coefficient")
    dynamic_friction: float = Field(default=0.5, description="Dynamic friction coefficient")
    restitution: float = Field(default=0.0, description="Restitution (bounciness)")


class GetGroundPlane(Message):
    """
    Get an existing ground plane.
    """

    path: str | None = Field(default=None, description="USD path of the ground plane prim")


class GetGroundPlaneResponse(Message):
    """
    Response from getting a ground plane.
    """

    path: str


class AddGroundPlane(Message):
    """
    Add a ground plane.
    """

    path: str = Field(description="USD path for the ground plane")
    config: GroundPlaneConfig
