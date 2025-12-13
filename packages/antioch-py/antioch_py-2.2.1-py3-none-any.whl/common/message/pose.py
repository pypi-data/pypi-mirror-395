from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import Field, field_validator, model_validator

from common.message.base import Message
from common.message.vector import Vector3


class Pose(Message):
    """
    A pose representing position and orientation in 3D space.

    Serializes position as [x, y, z] and orientation as [roll, pitch, yaw] in radians.
    Orientation is stored as RPY (Roll-Pitch-Yaw) Euler angles.

    Automatically converts from common Python types:
    - Lists/tuples: Pose(position=[1.0, 2.0, 3.0], orientation=[0.0, 0.0, 1.57])
    - Dicts: Pose(position={"x": 1.0, "y": 2.0, "z": 3.0}, orientation={"x": 0.0, "y": 0.0, "z": 1.57})
    """

    _type = "antioch/pose"
    position: Vector3 = Field(default_factory=lambda: Vector3.zeros())
    orientation: Vector3 = Field(default_factory=lambda: Vector3.zeros())

    def __add__(self, other: Vector3) -> Pose:
        """
        Translate the pose by a vector (adds to position).

        :param other: A Vector3 representing the translation.
        :return: The translated pose.
        """

        return Pose(position=self.position + other, orientation=self.orientation)

    def __sub__(self, other: Vector3) -> Pose:
        """
        Translate the pose by a negative vector (subtracts from position).

        :param other: A Vector3 representing the translation.
        :return: The translated pose.
        """

        return Pose(position=self.position - other, orientation=self.orientation)

    @model_validator(mode="before")
    @classmethod
    def convert_nested_types(cls, data: Any) -> Any:
        """
        Allow passing position and orientation as lists/tuples that auto-convert to Vector3/Quaternion.
        Orientation can be 3 values (RPY) or 4 values (quaternion) - always stored as quaternion.
        """

        # Already a Pose instance
        if isinstance(data, cls):
            return data.model_dump()

        # Dict format - let Pydantic and nested validators handle it
        if isinstance(data, dict):
            return data

        return data

    @field_validator("position", mode="before")
    @classmethod
    def validate_position(cls, v: Any) -> Any:
        """
        Convert position from list/tuple/array to Vector3 format before type validation.
        """

        if isinstance(v, (list, tuple, np.ndarray)):
            return Vector3.convert_iterables.__func__(Vector3, v)
        return v

    @field_validator("orientation", mode="before")
    @classmethod
    def validate_orientation(cls, v: Any) -> Any:
        """
        Convert orientation from list/tuple/array to Vector3 format before type validation.
        """

        if isinstance(v, (list, tuple, np.ndarray)):
            return Vector3.convert_iterables.__func__(Vector3, v)
        return v

    @classmethod
    def from_any(cls, data: Any) -> Pose:
        """
        Create Pose from a dict or Pose instance.

        :param data: Dict with position/orientation fields, or a Pose instance.
        :return: A Pose instance.
        :raises ValueError: If conversion fails.
        """

        # Already a Pose - return as-is
        if isinstance(data, cls):
            return data

        try:
            if isinstance(data, dict):
                return cls(**data)
            raise ValueError("Pose requires a dict with position and orientation fields")
        except Exception as e:
            raise ValueError(f"Cannot convert to Pose: {e}") from None

    @classmethod
    def identity(cls) -> Pose:
        """
        Create an identity pose at origin with zero rotation.

        :return: Identity pose.
        """

        return cls(position=Vector3.zeros(), orientation=Vector3.zeros())

    @classmethod
    def from_position(cls, position: Vector3) -> Pose:
        """
        Create a pose from a position with zero rotation.

        :param position: The position.
        :return: The pose.
        """

        return cls(position=position, orientation=Vector3.zeros())

    def translate(self, offset: Vector3) -> Pose:
        """
        Create a new pose with the position translated by an offset.

        :param offset: The translation offset.
        :return: The translated pose.
        """

        return Pose(position=self.position + offset, orientation=self.orientation)

    def rotate(self, rotation: Vector3) -> Pose:
        """
        Create a new pose with additional rotation (in RPY).

        :param rotation: Additional rotation in Roll-Pitch-Yaw.
        :return: The rotated pose.
        """

        return Pose(position=self.position, orientation=self.orientation + rotation)
