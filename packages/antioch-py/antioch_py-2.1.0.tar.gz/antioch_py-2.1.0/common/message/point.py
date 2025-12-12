from __future__ import annotations

from common.message.base import Message


class Point2(Message):
    """
    A point representing a position in 2D space.

    Used in image annotations and 2D coordinate systems.
    """

    _type = "antioch/point2"
    x: float
    y: float

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Point2(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Point2(x={self.x}, y={self.y})"

    @classmethod
    def new(cls, x: float, y: float) -> Point2:
        """
        Create a new 2D point.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: A 2D point.
        """

        return cls(x=x, y=y)

    @classmethod
    def zero(cls) -> Point2:
        """
        Create a point at the origin.

        :return: A point at (0, 0).
        """

        return cls(x=0.0, y=0.0)


class Point3(Message):
    """
    A point representing a position in 3D space.

    Used in 3D graphics and spatial coordinate systems.
    """

    _type = "antioch/point3"
    x: float
    y: float
    z: float

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Point3(x={self.x}, y={self.y}, z={self.z})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Point3(x={self.x}, y={self.y}, z={self.z})"

    @classmethod
    def new(cls, x: float, y: float, z: float) -> Point3:
        """
        Create a new 3D point.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :param z: The z coordinate.
        :return: A 3D point.
        """

        return cls(x=x, y=y, z=z)

    @classmethod
    def zero(cls) -> Point3:
        """
        Create a point at the origin.

        :return: A point at (0, 0, 0).
        """

        return cls(x=0.0, y=0.0, z=0.0)
