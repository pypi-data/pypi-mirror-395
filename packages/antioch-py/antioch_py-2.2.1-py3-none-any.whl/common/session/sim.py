from enum import Enum
from typing import Any, TypeVar, cast

from common.message import Message

T = TypeVar("T")
_MISSING = object()


class SimulationState(str, Enum):
    """
    Represents the current state of the simulation.
    """

    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"


class SimulationInfo(Message):
    """
    Full simulation info.
    """

    state: SimulationState
    sim_time_us: int | None


class SimulationTime(Message):
    """
    Current simulation time in microseconds.
    """

    time_us: int


class RpcError(Message):
    """
    RPC error details.
    """

    message: str
    internal: bool = False
    traceback: str | None = None


class RpcCall(Message):
    """
    RPC request with dict payload.
    """

    data: dict[str, Any] | None = None

    def get(self, key: str, *, type: type[T] | None = None, default: T | object = _MISSING) -> T:
        """
        Get a value from the call data with optional type conversion.

        If type is a Message subclass, auto-converts via model_validate.
        Raises KeyError if key missing and no default provided.

        :param key: The key to lookup in data.
        :param type: The expected type class (optional).
        :param default: Default value to return if key is missing (can be None).
        :return: The value (converted if type provided).
        :raises KeyError: If key is missing and no default provided.
        """

        if self.data is None or key not in self.data:
            if default is not _MISSING:
                return cast(T, default)
            raise KeyError(f"Missing required field '{key}'")

        value = self.data[key]
        if type is not None and isinstance(value, dict) and issubclass(type, Message):
            return cast(T, type.model_validate(value))

        return cast(T, value)


class RpcResponse(Message):
    """
    RPC response with arbitrary payload or error.
    """

    data: Any = None
    error: RpcError | None = None


class SceneTarget(str, Enum):
    """
    Enum representing the different types of prims that can be queried in the scene.
    """

    XFORM = "xform"
    ARTICULATION = "articulation"
    RIGID_BODY = "rigid_body"
    JOINT = "joint"
    LIGHT = "light"
    GROUND_PLANE = "ground_plane"
    GEOMETRY = "geometry"
    CAMERA = "camera"
    RADAR = "radar"
    IMU = "imu"
    ANIMATION = "animation"


class PrimInfo(Message):
    """
    Information about a prim in the scene with its applicable view types.
    """

    path: str
    targets: list[SceneTarget]


class SceneQueryResponse(Message):
    """
    Response containing the results of a scene query.
    """

    prims: list[PrimInfo]


class PrimAttributeValue(Message):
    """
    Response containing an attribute value.
    """

    value: float | int | str | bool | list[float]
