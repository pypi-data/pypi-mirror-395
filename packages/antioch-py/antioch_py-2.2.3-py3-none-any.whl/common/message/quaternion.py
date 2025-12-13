from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation

from common.message.base import Message

try:
    from pxr import Gf  # type: ignore

    HAS_PXR = True
except ImportError:
    HAS_PXR = False


class Quaternion(Message):
    """
    A quaternion for 3D rotations.

    Serializes as a tuple [w, x, y, z] for space efficiency where w is the scalar component.

    Examples:
        Quaternion.new(1.0, 0.0, 0.0, 0.0)  # Create identity quaternion
        Quaternion.from_rpy(0.0, 0.0, 1.57)  # Create from RPY angles
    """

    _type = "antioch/quaternion"
    data: tuple[float, float, float, float]

    @property
    def w(self) -> float:
        """
        Get the w (scalar) component.

        :return: The w (scalar) component.
        """

        return self.data[0]

    @property
    def x(self) -> float:
        """
        Get the x component.

        :return: The x component.
        """

        return self.data[1]

    @property
    def y(self) -> float:
        """
        Get the y component.

        :return: The y component.
        """

        return self.data[2]

    @property
    def z(self) -> float:
        """
        Get the z component.

        :return: The z component.
        """

        return self.data[3]

    def __len__(self) -> int:
        """
        Get the length of the quaternion (always 4).

        :return: The length of the quaternion.
        """

        return 4

    def __iter__(self):
        """
        Iterate over quaternion components.

        :return: Iterator over [w, x, y, z].
        """

        return iter(self.data)

    def __getitem__(self, index: int) -> float:
        """
        Get quaternion component by index.

        :param index: Index (0=w, 1=x, 2=y, 3=z).
        :return: The component value.
        """

        return self.data[index]

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Quaternion.

        :param other: Another Quaternion.
        :return: True if equal.
        """

        if not isinstance(other, Quaternion):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Quaternion(w={self.w}, x={self.x}, y={self.y}, z={self.z})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Quaternion(w={self.w}, x={self.x}, y={self.y}, z={self.z})"

    @classmethod
    def new(cls, w: float, x: float, y: float, z: float) -> Quaternion:
        """
        Create a new quaternion.

        :param w: The w component.
        :param x: The x component.
        :param y: The y component.
        :param z: The z component.
        :return: A quaternion.
        """

        return cls(data=(w, x, y, z))

    @classmethod
    def identity(cls) -> Quaternion:
        """
        Create an identity quaternion (no rotation).

        :return: An identity quaternion [1, 0, 0, 0].
        """

        return cls(data=(1.0, 0.0, 0.0, 0.0))

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> Quaternion:
        """
        Create a quaternion from a numpy array [w, x, y, z].

        :param array: The numpy array to create the quaternion from (must have 4 elements).
        :return: A quaternion.
        :raises ValueError: If the array does not have exactly 4 elements.
        """

        if array.shape != (4,):
            raise ValueError(f"Quaternion array must have shape (4,), got {array.shape}")
        return cls(data=(float(array[0]), float(array[1]), float(array[2]), float(array[3])))

    @classmethod
    def from_rpy(cls, roll: float, pitch: float, yaw: float) -> Quaternion:
        """
        Create a quaternion from roll-pitch-yaw angles (in radians).

        :param roll: Roll angle in radians (rotation around x-axis).
        :param pitch: Pitch angle in radians (rotation around y-axis).
        :param yaw: Yaw angle in radians (rotation around z-axis).
        :return: A quaternion.
        """

        rotation = Rotation.from_euler("xyz", [roll, pitch, yaw])
        quat_xyzw = rotation.as_quat()
        return cls(
            data=(
                float(quat_xyzw[3]),
                float(quat_xyzw[0]),
                float(quat_xyzw[1]),
                float(quat_xyzw[2]),
            )
        )

    def to_numpy(self) -> np.ndarray:
        """
        Convert the quaternion to a numpy array.

        :return: The numpy array [w, x, y, z].
        """

        return np.array(self.data, dtype=np.float32)

    def to_list(self) -> list[float]:
        """
        Convert the quaternion to a list.

        :return: The list [w, x, y, z].
        """

        return list(self.data)

    def to_gf_quatf(self) -> Gf.Quatf:
        """
        Convert the quaternion to a Gf.Quatf.

        Note: Gf.Quatf expects (w, x, y, z) order.

        :return: The Gf.Quatf.
        :raises ImportError: If pxr is not installed.
        """

        if not HAS_PXR:
            raise ImportError("pxr is not installed")
        return Gf.Quatf(self.w, self.x, self.y, self.z)

    def to_gf_quatd(self) -> Gf.Quatd:
        """
        Convert the quaternion to a Gf.Quatd (double precision).

        Note: Gf.Quatd expects (w, x, y, z) order.

        :return: The Gf.Quatd.
        :raises ImportError: If pxr is not installed.
        """

        if not HAS_PXR:
            raise ImportError("pxr is not installed")
        return Gf.Quatd(self.w, self.x, self.y, self.z)

    def normalize(self) -> Quaternion:
        """
        Return a normalized version of this quaternion.

        :return: A normalized quaternion.
        """

        arr = self.to_numpy()
        norm = np.linalg.norm(arr)
        if norm > 0:
            normalized = arr / norm
            return self.__class__(
                data=(
                    float(normalized[0]),
                    float(normalized[1]),
                    float(normalized[2]),
                    float(normalized[3]),
                )
            )
        return self.identity()

    def to_rpy(self) -> tuple[float, float, float]:
        """
        Convert the quaternion to roll-pitch-yaw angles (in radians).

        :return: A tuple of (roll, pitch, yaw) angles in radians.
        """

        rotation = Rotation.from_quat([self.x, self.y, self.z, self.w])
        rpy = rotation.as_euler("xyz")
        return (float(rpy[0]), float(rpy[1]), float(rpy[2]))

    def as_array(self) -> list[float]:
        """
        Convert to a list (alias for to_list for Rust compatibility).

        :return: The list [w, x, y, z].
        """

        return self.to_list()
