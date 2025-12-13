from typing import Literal

from antioch.session.session import Session, SessionContainer
from common.message import Vector3


class BasisCurve(SessionContainer):
    """
    Ergonomic wrapper for basis curve operations.

    BasisCurves should be added using scene.add_basis_curve() or retrieved using scene.get_basis_curve().

    Example:
        scene = Scene()

        # Add basis curve
        basis_curve = scene.add_basis_curve(
            path="/World/curve",
            center=[1.0, 2.0, 3.0],
            radius=2.0,
            min_angle_deg=0.0,
            max_angle_deg=180.0,
        )

        extents = basis_curve.get_extents()
    """

    def __init__(self, path: str):
        """
        Initialize basis curve by resolving path and validating existence.

        :param path: USD path for the basis curve.
        """

        super().__init__()
        self._session.query_sim_rpc(endpoint="basis_curve/get", payload={"path": path})
        self._path = path

    @property
    def path(self) -> str:
        """
        Get the path of the basis curve.

        :return: The path of the basis curve.
        """

        return self._path

    @classmethod
    def add(
        cls,
        path: str,
        center: Vector3 = Vector3.zeros(),
        radius: float = 1.0,
        min_angle_deg: float = 0.0,
        max_angle_deg: float = 180.0,
        guide: bool = False,
        color: Vector3 | None = None,
        width: float = 0.005,
    ) -> "BasisCurve":
        """
        Add a semi-circle basis curve to the scene.

        :param path: USD path for the basis curve.
        :param center: Center of the basis curve.
        :param radius: Radius of the basis curve.
        :param min_angle_deg: Minimum angle of the basis curve in degrees.
        :param max_angle_deg: Maximum angle of the basis curve in degrees.
        :param guide: If True, mark as guide purpose (invisible to cameras). If False, default purpose.
        :param color: Optional RGB color [0-1].
        :param width: Width of the curve.
        :return: The basis curve instance.
        """

        Session.get_current().query_sim_rpc(
            endpoint="basis_curve/add_semi_circle",
            payload={
                "path": path,
                "center": center,
                "radius": radius,
                "min_angle_deg": min_angle_deg,
                "max_angle_deg": max_angle_deg,
                "guide": guide,
                "color": color,
                "width": width,
            },
        )
        return cls(path)

    @classmethod
    def add_line(
        cls,
        path: str,
        start: Vector3,
        end: Vector3 | None = None,
        angle_deg: float | None = None,
        length: float | None = None,
        guide: bool = False,
        color: Vector3 | None = None,
        width: float = 0.005,
    ) -> "BasisCurve":
        """
        Add a line basis curve to the scene.

        Supports two modes:
        - Cartesian: Provide start and end points directly
        - Polar: Provide start point, angle (degrees from +X axis in XY plane), and length

        :param path: USD path for the basis curve.
        :param start: Start point of the line.
        :param end: End point of the line (Cartesian mode).
        :param angle_deg: Angle in degrees from +X axis in XY plane (polar mode).
        :param length: Length of the line (polar mode).
        :param guide: If True, mark as guide purpose (invisible to cameras). If False, default purpose.
        :param color: Optional RGB color [0-1].
        :param width: Width of the curve.
        :return: The basis curve instance.
        :raises ValueError: If both modes are specified or neither mode is complete.
        """

        Session.get_current().query_sim_rpc(
            endpoint="basis_curve/add_line",
            payload={
                "path": path,
                "start": start,
                "end": end,
                "angle_deg": angle_deg,
                "length": length,
                "guide": guide,
                "color": color,
                "width": width,
            },
        )
        return cls(path)

    def get_extents(self) -> tuple[Vector3, Vector3]:
        """
        Get the extents of the basis curve.

        :return: Extents as tuple of start and end points.
        """

        result = self._session.query_sim_rpc(endpoint="basis_curve/get_extents", payload={"path": self._path})
        if result is None:
            raise RuntimeError("Failed to get extents")
        return Vector3(**result[0]), Vector3(**result[1])

    def get_points(
        self, samples_per_segment: int = 10, sort_by: Literal["X", "Y", "Z"] | None = None, ascending: bool = True
    ) -> list[Vector3]:
        """
        Get the points of the basis curve.

        :param samples_per_segment: The number of samples per segment.
        :param sort_by: The axis to sort the points by.
        :param ascending: Whether to sort the points in ascending order.
        :return: The points of the basis curve.
        """

        response = self._session.query_sim_rpc(
            endpoint="basis_curve/get_points",
            payload={"path": self._path, "samples_per_segment": samples_per_segment, "sort_by": sort_by, "ascending": ascending},
        )
        return [Vector3(**pt) for pt in response] if response else []

    def set_visibility(self, visible: bool) -> None:
        """
        Set the visibility of the basis curve.

        :param visible: True to make visible, False to hide.
        """

        self._session.query_sim_rpc(endpoint="basis_curve/set_visibility", payload={"path": self._path, "visible": visible})

    def remove(self) -> None:
        """
        Remove the basis curve from the scene.
        """

        self._session.query_sim_rpc(endpoint="basis_curve/remove", payload={"path": self._path})
