from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
from pydantic import model_validator

from common.message.base import Message
from common.message.point import Point2, Point3

if TYPE_CHECKING:
    from common.message.quaternion import Quaternion

try:
    from pxr import Gf  # type: ignore

    HAS_PXR = True
except ImportError:
    HAS_PXR = False


class Vector2(Message):
    """
    A 2D vector (x, y).

    Serializes as a tuple [x, y] for space efficiency.
    Automatically converts from common Python types:
    - Lists: Vector2.from_any([1.0, 2.0])
    - Tuples: Vector2.from_any((1.0, 2.0))
    - Dicts: Vector2.from_any({"x": 1.0, "y": 2.0})
    - Numpy arrays: Vector2.from_any(np.array([1.0, 2.0]))

    When used as a field in Messages, conversion happens automatically:
        pose = SomeMessage(position_2d=[10.0, 20.0])  # List auto-converts!
    """

    _type = "antioch/vector2"
    data: tuple[float, float]

    @property
    def x(self) -> float:
        """Get the x component.

        :return: The x component.
        """

        return self.data[0]

    @property
    def y(self) -> float:
        """Get the y component.

        :return: The y component.
        """

        return self.data[1]

    def __len__(self) -> int:
        """
        Get the length of the vector (always 2).

        :return: The length of the vector.
        """

        return 2

    def __iter__(self):
        """
        Iterate over vector components.

        :return: Iterator over [x, y].
        """

        return iter(self.data)

    def __getitem__(self, index: int) -> float:
        """
        Get vector component by index.

        :param index: Index (0=x, 1=y).
        :return: The component value.
        """

        return self.data[index]

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Vector2.

        :param other: Another Vector2.
        :return: True if equal.
        """

        if not isinstance(other, Vector2):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Vector2(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Vector2(x={self.x}, y={self.y})"

    def __add__(self, other: Vector2) -> Vector2:
        """
        Add two vectors component-wise.

        :param other: Another Vector2.
        :return: The sum vector.
        """

        return Vector2(data=(self.x + other.x, self.y + other.y))

    def __sub__(self, other: Vector2) -> Vector2:
        """
        Subtract two vectors component-wise.

        :param other: Another Vector2.
        :return: The difference vector.
        """

        return Vector2(data=(self.x - other.x, self.y - other.y))

    def __mul__(self, scalar: float) -> Vector2:
        """
        Multiply vector by a scalar.

        :param scalar: The scalar value.
        :return: The scaled vector.
        """

        return Vector2(data=(self.x * scalar, self.y * scalar))

    def __rmul__(self, scalar: float) -> Vector2:
        """
        Multiply vector by a scalar (reversed operands).

        :param scalar: The scalar value.
        :return: The scaled vector.
        """

        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector2:
        """
        Divide vector by a scalar.

        :param scalar: The scalar value.
        :return: The scaled vector.
        :raises ZeroDivisionError: If scalar is zero.
        """

        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero")
        return Vector2(data=(self.x / scalar, self.y / scalar))

    def __neg__(self) -> Vector2:
        """
        Negate the vector.

        :return: The negated vector.
        """

        return Vector2(data=(-self.x, -self.y))

    @model_validator(mode="before")
    @classmethod
    def convert_iterables(cls, data: Any) -> Any:
        """
        Automatically convert lists, tuples, dicts, and numpy arrays to Vector2 format.
        """

        # Already a Vector2 instance
        if isinstance(data, cls):
            return {"data": data.data}

        # Tuple format - already correct
        if isinstance(data, tuple) and len(data) == 2:
            return {"data": (float(data[0]), float(data[1]))}

        # Dict format with x, y - convert to tuple
        if isinstance(data, dict):
            if "data" in data:
                return data
            if "x" in data and "y" in data:
                return {"data": (float(data["x"]), float(data["y"]))}
            raise ValueError("Dict must have either 'data' or 'x' and 'y' fields")

        # Numpy array - convert
        if isinstance(data, np.ndarray):
            if data.shape != (2,):
                raise ValueError(f"Vector2 array must have shape (2,), got {data.shape}")
            return {"data": (float(data[0]), float(data[1]))}

        # List - convert
        if isinstance(data, list):
            if len(data) != 2:
                raise ValueError(f"Vector2 requires 2 values, got {len(data)}")
            return {"data": (float(data[0]), float(data[1]))}

        return data

    @classmethod
    def new(cls, x: float, y: float) -> Vector2:
        """
        Create a new 2D vector.

        :param x: The x component.
        :param y: The y component.
        :return: A 2D vector.
        """

        return cls(data=(x, y))

    @classmethod
    def zeros(cls) -> Vector2:
        """
        Create a zero vector.

        :return: A zero vector.
        """

        return cls(data=(0.0, 0.0))

    @classmethod
    def ones(cls) -> Vector2:
        """
        Create a ones vector.

        :return: A ones vector.
        """

        return cls(data=(1.0, 1.0))

    @classmethod
    def from_any(cls, data: Any) -> Vector2:
        """
        Create Vector2 from any iterable (list, tuple, numpy array).

        :param data: Iterable with 2 values, dict, or a Vector2 instance.
        :return: A Vector2 instance.
        :raises ValueError: If conversion fails.
        """

        # Already a Vector2 - return as-is
        if isinstance(data, cls):
            return data

        try:
            # Will be handled by validator
            return cls.model_validate(data)
        except Exception as e:
            raise ValueError(f"Cannot convert to Vector2: {e}") from None

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> Vector2:
        """
        Create from a numpy array.

        :param array: The numpy array (must have shape (2,)).
        :return: A Vector2.
        :raises ValueError: If array shape is not (2,).
        """

        if array.shape != (2,):
            raise ValueError(f"Vector2 array must have shape (2,), got {array.shape}")
        return cls(data=(float(array[0]), float(array[1])))

    @classmethod
    def from_list(cls, values: list[float]) -> Vector2:
        """
        Create from a list of 2 values.

        :param values: List of 2 float values.
        :return: A Vector2.
        :raises ValueError: If list does not have exactly 2 values.
        """

        if len(values) != 2:
            raise ValueError(f"Vector2 requires 2 values, got {len(values)}")
        return cls(data=(values[0], values[1]))

    def dot(self, other: Vector2) -> float:
        """
        Compute dot product with another vector.

        :param other: Another Vector2.
        :return: The dot product.
        """

        return self.x * other.x + self.y * other.y

    def magnitude(self) -> float:
        """
        Compute the magnitude (length) of the vector.

        :return: The magnitude.
        """

        return (self.x**2 + self.y**2) ** 0.5

    def magnitude_squared(self) -> float:
        """
        Compute the squared magnitude of the vector.

        :return: The squared magnitude.
        """

        return self.x**2 + self.y**2

    def normalize(self) -> Vector2:
        """
        Return a normalized (unit length) version of this vector.

        :return: The normalized vector.
        :raises ValueError: If the vector has zero magnitude.
        """

        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / mag

    def to_numpy(self) -> np.ndarray:
        """
        Convert to a numpy array.

        :return: The numpy array.
        """

        return np.array(self.data, dtype=np.float32)

    def to_list(self) -> list[float]:
        """
        Convert to a list.

        :return: The list of values.
        """

        return list(self.data)

    def to_point(self) -> Point2:
        """
        Convert to a Point2.

        :return: A Point2 with the same x, y coordinates.
        """

        return Point2(x=self.x, y=self.y)

    def as_array(self) -> list[float]:
        """
        Convert to a list (alias for to_list for Rust compatibility).

        :return: The list of values.
        """

        return self.to_list()


class Vector3(Message):
    """
    A 3D vector (x, y, z).

    Serializes as a tuple [x, y, z] for space efficiency.
    Automatically converts from common Python types:
    - Lists: Vector3.from_any([1.0, 2.0, 3.0])
    - Tuples: Vector3.from_any((1.0, 2.0, 3.0))
    - Dicts: Vector3.from_any({"x": 1.0, "y": 2.0, "z": 3.0})
    - Numpy arrays: Vector3.from_any(np.array([1.0, 2.0, 3.0]))

    When used as a field in Messages, conversion happens automatically:
        pose = SomeMessage(position=[10.0, 20.0, 30.0])  # List auto-converts!
    """

    _type = "antioch/vector3"
    data: tuple[float, float, float]

    @property
    def x(self) -> float:
        """Get the x component.

        :return: The x component.
        """

        return self.data[0]

    @property
    def y(self) -> float:
        """Get the y component.

        :return: The y component.
        """

        return self.data[1]

    @property
    def z(self) -> float:
        """Get the z component.

        :return: The z component.
        """

        return self.data[2]

    def __len__(self) -> int:
        """
        Get the length of the vector (always 3).

        :return: The length of the vector.
        """

        return 3

    def __iter__(self):
        """
        Iterate over vector components.

        :return: Iterator over [x, y, z].
        """

        return iter(self.data)

    def __getitem__(self, index: int) -> float:
        """
        Get vector component by index.

        :param index: Index (0=x, 1=y, 2=z).
        :return: The component value.
        """

        return self.data[index]

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Vector3.

        :param other: Another Vector3.
        :return: True if equal.
        """

        if not isinstance(other, Vector3):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

    def __add__(self, other: Vector3) -> Vector3:
        """
        Add two vectors component-wise.

        :param other: Another Vector3.
        :return: The sum vector.
        """

        return Vector3(data=(self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other: Vector3) -> Vector3:
        """
        Subtract two vectors component-wise.

        :param other: Another Vector3.
        :return: The difference vector.
        """

        return Vector3(data=(self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, scalar: float) -> Vector3:
        """
        Multiply vector by a scalar.

        :param scalar: The scalar value.
        :return: The scaled vector.
        """

        return Vector3(data=(self.x * scalar, self.y * scalar, self.z * scalar))

    def __rmul__(self, scalar: float) -> Vector3:
        """
        Multiply vector by a scalar (reversed operands).

        :param scalar: The scalar value.
        :return: The scaled vector.
        """

        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector3:
        """
        Divide vector by a scalar.

        :param scalar: The scalar value.
        :return: The scaled vector.
        :raises ZeroDivisionError: If scalar is zero.
        """

        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero")
        return Vector3(data=(self.x / scalar, self.y / scalar, self.z / scalar))

    def __neg__(self) -> Vector3:
        """
        Negate the vector.

        :return: The negated vector.
        """

        return Vector3(data=(-self.x, -self.y, -self.z))

    @model_validator(mode="before")
    @classmethod
    def convert_iterables(cls, data: Any) -> Any:
        """
        Automatically convert lists, tuples, dicts, and numpy arrays to Vector3 format.
        """

        # Already a Vector3 instance
        if isinstance(data, cls):
            return {"data": data.data}

        # Tuple format - already correct
        if isinstance(data, tuple) and len(data) == 3:
            return {"data": (float(data[0]), float(data[1]), float(data[2]))}

        # Dict format with x, y, z - convert to tuple
        if isinstance(data, dict):
            if "data" in data:
                return data
            if "x" in data and "y" in data and "z" in data:
                return {"data": (float(data["x"]), float(data["y"]), float(data["z"]))}
            raise ValueError("Dict must have either 'data' or 'x', 'y', and 'z' fields")

        # Numpy array - convert
        if isinstance(data, np.ndarray):
            if data.shape != (3,):
                raise ValueError(f"Vector3 array must have shape (3,), got {data.shape}")
            return {"data": (float(data[0]), float(data[1]), float(data[2]))}

        # List - convert
        if isinstance(data, list):
            if len(data) != 3:
                raise ValueError(f"Vector3 requires 3 values, got {len(data)}")
            if all(item is None for item in data):
                return {"data": (0.0, 0.0, 0.0)}
            return {"data": (float(data[0]), float(data[1]), float(data[2]))}

        return data

    @classmethod
    def new(cls, x: float, y: float, z: float) -> Vector3:
        """
        Create a new 3D vector.

        :param x: The x component.
        :param y: The y component.
        :param z: The z component.
        :return: A 3D vector.
        """

        return cls(data=(x, y, z))

    @classmethod
    def zeros(cls) -> Vector3:
        """
        Create a zero vector.

        :return: A zero vector.
        """

        return cls(data=(0.0, 0.0, 0.0))

    @classmethod
    def ones(cls) -> Vector3:
        """
        Create a ones vector.

        :return: A ones vector.
        """

        return cls(data=(1.0, 1.0, 1.0))

    @classmethod
    def from_any(cls, data: Any) -> Vector3:
        """
        Create Vector3 from any iterable (list, tuple, numpy array).

        :param data: Iterable with 3 values, dict, or a Vector3 instance.
        :return: A Vector3 instance.
        :raises ValueError: If conversion fails.
        """

        # Already a Vector3 - return as-is
        if isinstance(data, cls):
            return data

        try:
            # Will be handled by validator
            return cls.model_validate(data)
        except Exception as e:
            raise ValueError(f"Cannot convert to Vector3: {e}") from None

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> Vector3:
        """
        Create from a numpy array.

        :param array: The numpy array (must have shape (3,)).
        :return: A Vector3.
        :raises ValueError: If array shape is not (3,).
        """

        if array.shape != (3,):
            raise ValueError(f"Vector3 array must have shape (3,), got {array.shape}")
        return cls(data=(float(array[0]), float(array[1]), float(array[2])))

    @classmethod
    def from_list(cls, values: list[float]) -> Vector3:
        """
        Create from a list of 3 values.

        :param values: List of 3 float values.
        :return: A Vector3.
        :raises ValueError: If list does not have exactly 3 values.
        """

        if len(values) != 3:
            raise ValueError(f"Vector3 requires 3 values, got {len(values)}")
        return cls(data=(values[0], values[1], values[2]))

    def dot(self, other: Vector3) -> float:
        """
        Compute dot product with another vector.

        :param other: Another Vector3.
        :return: The dot product.
        """

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        """
        Compute cross product with another vector.

        :param other: Another Vector3.
        :return: The cross product vector.
        """

        return Vector3(
            data=(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        )

    def magnitude(self) -> float:
        """
        Compute the magnitude (length) of the vector.

        :return: The magnitude.
        """

        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def magnitude_squared(self) -> float:
        """
        Compute the squared magnitude of the vector.

        :return: The squared magnitude.
        """

        return self.x**2 + self.y**2 + self.z**2

    def normalize(self) -> Vector3:
        """
        Return a normalized (unit length) version of this vector.

        :return: The normalized vector.
        :raises ValueError: If the vector has zero magnitude.
        """

        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / mag

    def to_numpy(self) -> np.ndarray:
        """
        Convert to a numpy array.

        :return: The numpy array.
        """

        return np.array(self.data, dtype=np.float32)

    def to_list(self) -> list[float]:
        """
        Convert to a list.

        :return: The list of values.
        """

        return list(self.data)

    def to_gf_vec3f(self) -> Gf.Vec3f:
        """
        Convert to a Gf.Vec3f.

        :return: The Gf.Vec3f.
        :raises ImportError: If pxr is not installed.
        """

        if not HAS_PXR:
            raise ImportError("pxr is not installed")
        return Gf.Vec3f(self.x, self.y, self.z)

    def to_gf_vec3d(self) -> Gf.Vec3d:
        """
        Convert to a Gf.Vec3d (double precision).

        :return: The Gf.Vec3d.
        :raises ImportError: If pxr is not installed.
        """

        if not HAS_PXR:
            raise ImportError("pxr is not installed")
        return Gf.Vec3d(self.x, self.y, self.z)

    def to_quat(self) -> "Quaternion":
        """
        Convert RPY angles to quaternion.

        Assumes this Vector3 contains roll-pitch-yaw angles in radians.

        :return: Quaternion representation.
        """

        from common.message.quaternion import Quaternion

        return Quaternion.from_rpy(self.x, self.y, self.z)

    def to_point(self) -> Point3:
        """
        Convert to a Point3.

        :return: A Point3 with the same x, y, z coordinates.
        """

        return Point3(x=self.x, y=self.y, z=self.z)

    def as_array(self) -> list[float]:
        """
        Convert to a list (alias for to_list for Rust compatibility).

        :return: The list of values.
        """

        return self.to_list()
