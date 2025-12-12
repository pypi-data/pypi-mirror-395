from pydantic import Field

from common.message import Message
from common.session.views.geometry import MeshApproximation


class SetCollision(Message):
    """
    Apply collision API to a prim, optionally with mesh approximation.
    """

    path: str = Field(description="USD path to the prim")
    mesh_approximation: MeshApproximation | None = Field(
        default=None,
        description="Optional mesh approximation method for collision geometry",
    )


class RemoveCollision(Message):
    """
    Remove collision API from a prim.
    """

    path: str = Field(description="USD path to the prim")


class HasCollision(Message):
    """
    Check if a prim has collision API applied.
    """

    path: str = Field(description="USD path to the prim")


class HasCollisionResponse(Message):
    """
    Response for collision check.
    """

    has_collision: bool = Field(description="Whether the prim has collision API")


class GetMeshApproximation(Message):
    """
    Get mesh collision approximation from a prim.
    """

    path: str = Field(description="USD path to the prim")


class GetMeshApproximationResponse(Message):
    """
    Response for mesh approximation query.
    """

    approximation: MeshApproximation | None = Field(
        default=None,
        description="Mesh approximation method, or None if not set",
    )
