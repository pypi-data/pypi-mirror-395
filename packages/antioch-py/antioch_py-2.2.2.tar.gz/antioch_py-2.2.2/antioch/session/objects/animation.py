from typing import Literal, overload

from antioch.session.session import Session, SessionContainer
from common.message import Vector3


class Animation(SessionContainer):
    """
    Ergonomic wrapper for animation operations.

    Animations should be added using scene.add_animation() or retrieved using scene.get_animation().
    Animations wrap around an existing skeleton UsdSkel.Root and provide a way to play and control the animation.

    Example:
        scene = Scene()

        # Add xform
        animation = scene.add_animation(
            path="/World/skeleton",
            waypoints=[Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(0.0, 0.0, 1.0)],
            loop=True,
        )
    """

    def __init__(self, path: str):
        """
        Initialize animation by resolving path and validating existence.

        :param path: USD path for the animation.
        """

        super().__init__()
        self._path = path

    @overload
    @classmethod
    def add(cls, path: str, *, waypoints: list[Vector3], loop: bool = True) -> "Animation": ...

    @overload
    @classmethod
    def add(
        cls,
        path: str,
        *,
        basis_curve: str,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
    ) -> "Animation": ...

    @classmethod
    def add(
        cls,
        path: str,
        *,
        waypoints: list[Vector3] | None = None,
        basis_curve: str | None = None,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
        loop: bool = True,
    ) -> "Animation":
        """
        Add an animation to the scene.

        :param path: USD path for the animation.
        :param waypoints: List of waypoints.
        :param basis_curve: Path to the basis curve to use for the animation.
        :param samples_per_segment: The number of samples per segment to use from the basis curve.
        :param sort_by: The axis to sort the points by.
        :param ascending: Whether to sort the points in ascending order.
        :param loop: Whether to loop the animation (waypoints only).
        :return: The animation instance.
        """

        if waypoints is not None:
            Session.get_current().query_sim_rpc(
                endpoint="animation/add_from_waypoints",
                payload={"path": path, "waypoints": waypoints, "loop": loop},
            )
        elif basis_curve is not None:
            Session.get_current().query_sim_rpc(
                endpoint="animation/add_from_basis_curve",
                payload={
                    "path": path,
                    "basis_curve": basis_curve,
                    "samples_per_segment": samples_per_segment,
                    "sort_by": sort_by,
                    "ascending": ascending,
                },
            )
        else:
            raise ValueError("Must provide either waypoints or basis_curve")

        return cls(path)

    @overload
    def update(self, *, waypoints: list[Vector3], loop: bool = True) -> "Animation": ...

    @overload
    def update(
        self,
        *,
        basis_curve: str,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
    ) -> "Animation": ...

    def update(
        self,
        *,
        waypoints: list[Vector3] | None = None,
        basis_curve: str | None = None,
        samples_per_segment: int = 10,
        sort_by: Literal["X", "Y", "Z"] | None = None,
        ascending: bool = True,
        loop: bool = True,
    ) -> "Animation":
        """
        Update the animation.

        :param waypoints: List of waypoints.
        :param basis_curve: Path to the basis curve to use for the animation.
        :param samples_per_segment: The number of samples per segment to use from the basis curve.
        :param sort_by: The axis to sort the points by.
        :param ascending: Whether to sort the points in ascending order.
        :param loop: Whether to loop the animation (waypoints only).
        :raises ValueError: If both waypoints and basis curve are provided.
        :return: The animation instance.
        """

        if waypoints is not None and basis_curve is not None:
            raise ValueError("Must provide either waypoints or basis_curve")

        if waypoints is not None:
            Session.get_current().query_sim_rpc(
                endpoint="animation/update_waypoints",
                payload={"path": self._path, "waypoints": waypoints, "loop": loop},
            )
        elif basis_curve is not None:
            Session.get_current().query_sim_rpc(
                endpoint="animation/update_basis_curve",
                payload={
                    "path": self._path,
                    "basis_curve": basis_curve,
                    "samples_per_segment": samples_per_segment,
                    "sort_by": sort_by,
                    "ascending": ascending,
                },
            )
        else:
            raise ValueError("Must provide either waypoints or basis_curve")

        return self

    def remove(self) -> None:
        """
        Remove the animation from the scene (deletes the character).
        """

        self._session.query_sim_rpc(endpoint="animation/remove", payload={"path": self._path})
