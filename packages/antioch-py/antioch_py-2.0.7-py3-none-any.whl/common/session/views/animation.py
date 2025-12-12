from typing import Literal

from pydantic import Field

from common.message import Message, Vector3


class AddAnimationFromWaypoints(Message):
    """
    Add an animation to the scene using waypoints.
    """

    path: str = Field(description="USD path for the animation")
    waypoints: list[Vector3] = Field(description="List of waypoints")
    loop: bool = Field(default=True, description="Whether to loop the animation")


class AddAnimationFromBasisCurve(Message):
    """
    Add an animation to the scene using a basis curve.
    """

    path: str = Field(description="USD path for the animation")
    basis_curve: str = Field(description="Path to the basis curve to use for the animation")
    samples_per_segment: int = Field(default=10, description="The number of samples per segment to use from the basis curve")
    sort_by: Literal["X", "Y", "Z"] | None = Field(default=None, description="The axis to sort the points by")
    ascending: bool = Field(default=True, description="Whether to sort the points in ascending order")


class UpdateAnimationWaypoints(Message):
    """
    Update the animation waypoints.
    """

    path: str = Field(description="USD path for the animation")
    waypoints: list[Vector3] = Field(description="List of waypoints")
    loop: bool = Field(default=True, description="Whether to loop the animation")


class UpdateAnimationBasisCurve(Message):
    """
    Update the animation using a basis curve.
    """

    path: str = Field(description="USD path for the animation")
    basis_curve: str = Field(description="Path to the basis curve to use for the animation")
    samples_per_segment: int = Field(default=10, description="The number of samples per segment to use from the basis curve")
    sort_by: Literal["X", "Y", "Z"] | None = Field(default=None, description="The axis to sort the points by")
    ascending: bool = Field(default=True, description="Whether to sort the points in ascending order")


class GetAnimation(Message):
    """
    Get an existing animation view from a prim.
    """

    path: str = Field(description="USD path for the animation")


class GetAnimationResponse(Message):
    """
    Response from getting an animation view.
    """

    path: str


class RemoveAnimation(Message):
    """
    Remove an animation from the scene (deletes the prim).
    """

    path: str = Field(description="USD path for the animation")
