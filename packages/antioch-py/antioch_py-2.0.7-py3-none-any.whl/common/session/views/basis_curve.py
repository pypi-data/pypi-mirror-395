from typing import Literal

from pydantic import Field

from common.message import Message, Vector3


class AddBasisCurveSemiCircle(Message):
    """
    Add a basis curve semi-circle to the scene.
    """

    path: str = Field(description="USD path for the basis curve")
    center: Vector3 = Field(default_factory=Vector3.zeros, description="Center of the basis curve")
    radius: float = Field(default=1.0, description="Radius of the basis curve")
    min_angle_deg: float = Field(default=0.0, description="Minimum angle of the basis curve in degrees")
    max_angle_deg: float = Field(default=180.0, description="Maximum angle of the basis curve in degrees")


class AddBasisCurveLine(Message):
    """
    Add a basis curve line to the scene.

    Supports two modes:
    - Cartesian: Specify start and end points directly
    - Polar: Specify start point, angle (degrees), and length
    """

    path: str = Field(description="USD path for the basis curve")
    start: Vector3 = Field(description="Start point of the line")
    end: Vector3 | None = Field(default=None, description="End point of the line (Cartesian mode)")
    angle_deg: float | None = Field(default=None, description="Angle in degrees from +X axis in XY plane (polar mode)")
    length: float | None = Field(default=None, description="Length of the line (polar mode)")


class GetBasisCurve(Message):
    """
    Get an existing basis curve view from a prim.
    """

    path: str = Field(description="USD path for the basis curve")


class GetBasisCurveResponse(Message):
    """
    Response from getting a basis curve.
    """

    path: str


class GetBasisCurveExtents(Message):
    """
    Get the extents of a basis curve.
    """

    path: str = Field(description="USD path for the basis curve")


class GetBasisCurveExtentsResponse(Message):
    """
    Response from getting the extents of a basis curve.
    """

    start: Vector3 = Field(description="Start point of the basis curve")
    end: Vector3 = Field(description="End point of the basis curve")


class GetBasisCurvePoints(Message):
    """
    Get the points of a basis curve.
    """

    path: str = Field(description="USD path for the basis curve")
    samples_per_segment: int = Field(default=10, description="The number of samples per segment")
    sort_by: Literal["X", "Y", "Z"] | None = Field(default=None, description="The axis to sort the points by")
    ascending: bool = Field(default=True, description="Whether to sort the points in ascending order")


class GetBasisCurvePointsResponse(Message):
    """
    Response from getting the points of a basis curve.
    """

    points: list[Vector3] = Field(description="The points of the basis curve")


class SetBasisCurveVisibility(Message):
    """
    Set the visibility of a basis curve.
    """

    path: str = Field(description="USD path for the basis curve")
    visible: bool = Field(description="True to make visible, False to hide")


class RemoveBasisCurve(Message):
    """
    Remove a basis curve from the scene.
    """

    path: str = Field(description="USD path for the basis curve")
