from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import Field, PrivateAttr, model_validator

from common.message.base import Message


class Array(Message):
    """
    A message type for representing an unbounded array of float32 values.
    Serialized as bytes, with lazy numpy array conversion for operations.

    Arrays automatically convert from common Python types:
    - Lists: Array(data=[1.0, 2.0, 3.0]) or Array.from_any([1.0, 2.0, 3.0])
    - Tuples: Array(data=(1.0, 2.0, 3.0))
    - Sets: Array(data={1.0, 2.0, 3.0})
    - Numpy arrays: Array(data=np.array([1.0, 2.0, 3.0]))
    - Any iterable: Array(data=range(10))

    When used as a field in Messages, conversion happens automatically:
        class RobotCommand(Message):
            joint_positions: Array

        cmd = RobotCommand(joint_positions=[0.1, 0.2, 0.3])  # List auto-converts!

    This makes it seamless to use in APIs without explicit conversion calls.
    """

    _type = "antioch/array"
    _arr: np.ndarray | None = PrivateAttr(default=None)
    data: bytes = Field(description="Serialized array data as bytes")

    def __len__(self) -> int:
        """
        Get the length of the array.

        :return: The length.
        """

        return len(self.data) // 4  # 4 bytes per float32

    def __iter__(self):
        """
        Iterate over array elements.

        :return: Iterator over float values.
        """

        return iter(self.to_numpy())

    def __getitem__(self, key: Any) -> Any:
        """
        Get an item from the array.

        :param key: The index or slice.
        :return: The item.
        """

        return self.to_numpy()[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set an item in the array.

        :param key: The index or slice.
        :param value: The value to set.
        """

        arr = self.to_numpy().copy()
        arr[key] = value
        self.data = arr.tobytes()
        self._arr = arr

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Array.

        :param other: Another Array.
        :return: True if arrays are equal.
        """

        if not isinstance(other, Array):
            return False
        return self.data == other.data

    def __repr__(self) -> str:
        """
        Return a readable string representation showing array values.

        :return: String representation.
        """

        arr = self.to_numpy()
        return f"Array({arr!r})"

    def __str__(self) -> str:
        """
        Return a readable string representation showing array values.

        :return: String representation.
        """

        arr = self.to_numpy()
        return f"Array({arr!r})"

    def __add__(self, other: Array | float | int) -> Array:
        """
        Add arrays element-wise or add a scalar to all elements.

        :param other: Another Array or a scalar value.
        :return: The result array.
        """

        if isinstance(other, Array):
            result = self.to_numpy() + other.to_numpy()
        elif isinstance(other, (int, float)):
            result = self.to_numpy() + other
        return Array.from_numpy(result)

    def __radd__(self, other: float | int) -> Array:
        """
        Add a scalar to all elements (reversed operands).

        :param other: A scalar value.
        :return: The result array.
        """

        return self.__add__(other)

    def __sub__(self, other: Array | float | int) -> Array:
        """
        Subtract arrays element-wise or subtract a scalar from all elements.

        :param other: Another Array or a scalar value.
        :return: The result array.
        """

        if isinstance(other, Array):
            result = self.to_numpy() - other.to_numpy()
        elif isinstance(other, (int, float)):
            result = self.to_numpy() - other
        return Array.from_numpy(result)

    def __rsub__(self, other: float | int) -> Array:
        """
        Subtract all elements from a scalar (reversed operands).

        :param other: A scalar value.
        :return: The result array.
        """

        result = other - self.to_numpy()
        return Array.from_numpy(result)

    def __mul__(self, other: Array | float | int) -> Array:
        """
        Multiply arrays element-wise or multiply all elements by a scalar.

        :param other: Another Array or a scalar value.
        :return: The result array.
        """

        if isinstance(other, Array):
            result = self.to_numpy() * other.to_numpy()
        elif isinstance(other, (int, float)):
            result = self.to_numpy() * other
        return Array.from_numpy(result)

    def __rmul__(self, other: float | int) -> Array:
        """
        Multiply all elements by a scalar (reversed operands).

        :param other: A scalar value.
        :return: The result array.
        """

        return self.__mul__(other)

    def __truediv__(self, other: Array | float | int) -> Array:
        """
        Divide arrays element-wise or divide all elements by a scalar.

        :param other: Another Array or a scalar value.
        :return: The result array.
        :raises ZeroDivisionError: If dividing by zero scalar.
        """

        if isinstance(other, Array):
            result = self.to_numpy() / other.to_numpy()
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide array by zero")
            result = self.to_numpy() / other
        return Array.from_numpy(result)

    def __rtruediv__(self, other: float | int) -> Array:
        """
        Divide a scalar by all elements (reversed operands).

        :param other: A scalar value.
        :return: The result array.
        """

        result = other / self.to_numpy()
        return Array.from_numpy(result)

    def __neg__(self) -> Array:
        """
        Negate all elements in the array.

        :return: The negated array.
        """

        return Array.from_numpy(-self.to_numpy())

    def __pow__(self, other: float | int) -> Array:
        """
        Raise all elements to a power.

        :param other: The exponent.
        :return: The result array.
        """

        result = self.to_numpy() ** other
        return Array.from_numpy(result)

    @model_validator(mode="before")
    @classmethod
    def convert_iterables(cls, data: Any) -> Any:
        """
        Automatically convert common Python types to Array format.

        Supports: lists, tuples, sets, numpy arrays, and any iterable.
        This allows seamless usage without explicit Array.from_*() calls.
        """

        # Already an Array instance
        if isinstance(data, cls):
            return data.model_dump()

        # Dict format - check if data field needs conversion
        if isinstance(data, dict):
            # If data field is already bytes, no conversion needed
            if "data" in data and isinstance(data["data"], bytes):
                return data
            # If data field is an iterable, convert it
            if "data" in data:
                data_value = data["data"]
                if isinstance(data_value, np.ndarray):
                    data["data"] = data_value.astype(np.float32).tobytes()
                    return data
                if hasattr(data_value, "__iter__") and not isinstance(data_value, (str, bytes)):
                    try:
                        arr = np.array(list(data_value), dtype=np.float32)
                        data["data"] = arr.tobytes()
                        return data
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"Failed to convert iterable to Array: {e}") from None
            return data

        # Raw bytes (used internally)
        if isinstance(data, bytes):
            return {"data": data}

        # Numpy array - convert directly
        if isinstance(data, np.ndarray):
            return {"data": data.astype(np.float32).tobytes()}

        # Any iterable (list, tuple, set, generator, etc.) - exclude strings and bytes
        if hasattr(data, "__iter__") and not isinstance(data, (str, bytes)):
            try:
                arr = np.array(list(data), dtype=np.float32)
                return {"data": arr.tobytes()}
            except (ValueError, TypeError) as e:
                raise ValueError(f"Failed to convert iterable to Array: {e}") from None

        return data

    @classmethod
    def from_any(cls, data: Any) -> Array:
        """
        Create Array from any iterable type (list, tuple, set, numpy array, etc.).

        :param data: Any iterable containing numeric values, or an Array instance.
        :return: An Array instance.
        :raises ValueError: If conversion fails.
        """

        # Already an Array - return as-is
        if isinstance(data, cls):
            return data

        # Let the validator handle the conversion
        try:
            return cls(data=data)
        except Exception as e:
            raise ValueError(f"Cannot convert to Array: {e}") from None

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> Array:
        """
        Create from a numpy array.

        :param array: The numpy array.
        :return: An Array instance.
        """

        return cls(data=array.astype(np.float32).tobytes())

    @classmethod
    def from_list(cls, values: list[float]) -> Array:
        """
        Create from a list of floats.

        :param values: List of float values.
        :return: An Array instance.
        """

        return cls(data=np.array(values, dtype=np.float32).tobytes())

    @classmethod
    def zeros(cls, size: int) -> Array:
        """
        Create an array of zeros.

        :param size: The size of the array.
        :return: An Array of zeros.
        """

        return cls(data=np.zeros(size, dtype=np.float32).tobytes())

    @classmethod
    def ones(cls, size: int) -> Array:
        """
        Create an array of ones.

        :param size: The size of the array.
        :return: An Array of ones.
        """

        return cls(data=np.ones(size, dtype=np.float32).tobytes())

    def sum(self) -> float:
        """
        Compute the sum of all elements.

        :return: The sum.
        """

        return float(np.sum(self.to_numpy()))

    def mean(self) -> float:
        """
        Compute the mean of all elements.

        :return: The mean.
        """

        return float(np.mean(self.to_numpy()))

    def min(self) -> float:
        """
        Find the minimum element.

        :return: The minimum value.
        """

        return float(np.min(self.to_numpy()))

    def max(self) -> float:
        """
        Find the maximum element.

        :return: The maximum value.
        """

        return float(np.max(self.to_numpy()))

    def std(self) -> float:
        """
        Compute the standard deviation.

        :return: The standard deviation.
        """

        return float(np.std(self.to_numpy()))

    def dot(self, other: Array) -> float:
        """
        Compute dot product with another array.

        :param other: Another Array.
        :return: The dot product.
        :raises ValueError: If arrays have different lengths.
        """

        if len(self) != len(other):
            raise ValueError(f"Arrays must have same length for dot product: {len(self)} != {len(other)}")
        return float(np.dot(self.to_numpy(), other.to_numpy()))

    def magnitude(self) -> float:
        """
        Compute the magnitude (L2 norm) of the array.

        :return: The magnitude.
        """

        return float(np.linalg.norm(self.to_numpy()))

    def magnitude_squared(self) -> float:
        """
        Compute the squared magnitude of the array.

        :return: The squared magnitude.
        """

        return float(np.sum(self.to_numpy() ** 2))

    def normalize(self) -> Array:
        """
        Return a normalized version of this array (unit magnitude).

        :return: The normalized array.
        :raises ValueError: If the array has zero magnitude.
        """

        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize zero-magnitude array")
        return self / mag

    def to_numpy(self) -> np.ndarray:
        """
        Convert to a numpy array (cached).

        :return: The numpy array.
        """

        if self._arr is None:
            self._arr = np.frombuffer(self.data, dtype=np.float32)
        return self._arr

    def to_list(self) -> list[float]:
        """
        Convert to a list.

        :return: The list of values.
        """

        return self.to_numpy().tolist()

    def is_empty(self) -> bool:
        """
        Check if the array is empty.

        :return: True if empty, False otherwise.
        """

        return len(self.data) == 0

    def as_bytes(self) -> bytes:
        """
        Get the raw byte data (alias for data field for Rust compatibility).

        :return: The raw bytes.
        """

        return self.data

    def get(self, index: int) -> float | None:
        """
        Get element at index (returns None if out of bounds).

        :param index: The index.
        :return: The value or None.
        """

        if index < 0 or index >= len(self):
            return None
        return float(self.to_numpy()[index])

    def set(self, index: int, value: float) -> bool:
        """
        Set element at index.

        :param index: The index.
        :param value: The value to set.
        :return: True if successful, False if out of bounds.
        """

        if index < 0 or index >= len(self):
            return False
        arr = self.to_numpy().copy()
        arr[index] = value
        self.data = arr.tobytes()
        self._arr = arr
        return True
