import time
from enum import Enum
from typing import Any

from pydantic import Field

from common.message import Message, Pose, Vector3


class SimulationState(str, Enum):
    """
    Represents the current state of the simulation.
    """

    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"


class Step(Message):
    """
    Step the simulation forward by a specified amount of time in microseconds.
    """

    dt_us: int = 10000  # Default 10ms


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


class ToggleUi(Message):
    """
    Toggle the UI visibility.
    """

    show_ui: bool


class GetObject(Message):
    """
    Get information about a specific object.
    """

    path: str


class ObjectInfo(Message):
    """
    Information about a simulation object.
    """

    path: str
    type: str
    config: dict[str, Any]


class AllObjectInfo(Message):
    """
    All objects in the scene.
    """

    objects: list[ObjectInfo]


class GetWorldPose(Message):
    """
    Get the world pose of an object.
    """

    path: str = Field(description="USD path of the object")


class GetLocalPose(Message):
    """
    Get the local pose of an object.
    """

    path: str = Field(description="USD path of the object")


class SetWorldPose(Message):
    """
    Set the world pose of an object.
    """

    path: str = Field(description="USD path of the object")
    pose: Pose


class SetLocalPose(Message):
    """
    Set the local pose of an object.
    """

    path: str = Field(description="USD path of the object")
    pose: Pose


class RpcError(Message):
    """
    RPC error.
    """

    message: str
    internal: bool = False
    traceback: str | None = None


class RpcCall(Message):
    """
    RPC call with optional payload.
    """

    ts: int = Field(default_factory=lambda: int(time.time_ns() // 1000))
    payload: bytes | None = None


class RpcResponse(Message):
    """
    RPC response with optional payload and error.
    """

    ts: int = Field(default_factory=lambda: int(time.time_ns() // 1000))
    payload: bytes | None = None
    error: RpcError | None = None


class AddAsset(Message):
    """
    Add an asset to the simulation.
    """

    path: str = Field(description="USD path where asset will be added")
    asset_file_path: str = Field(description="Path to asset file (USD, FBX, OBJ, etc.)")
    asset_prim_path: str | None = Field(default=None, description="Full path to prim in the Usd file to reference")
    remove_articulation: bool = Field(default=True, description="Whether to remove articulation APIs")
    remove_rigid_body: bool = Field(default=False, description="Whether to remove rigid body APIs")
    remove_sensors: bool = Field(default=False, description="Whether to remove sensor and graph prims")
    world_pose: Pose | None = Field(default=None, description="Optional world pose")
    local_pose: Pose | None = Field(default=None, description="Optional local pose")
    scale: Vector3 | None = Field(default=None, description="Optional scale")


class GetPrimAttribute(Message):
    """
    Get an attribute value from a prim.

    Supports primitive and vector types (float, int, bool, string, Vec2/3/4, Quat).
    """

    path: str = Field(description="USD path to the prim")
    attribute_name: str = Field(description="Name of the attribute to get")


class SetPrimAttribute(Message):
    """
    Set an attribute value on a prim.

    Supports primitive and vector types (float, int, bool, string, Vec2/3/4, Quat).
    The attribute must already exist on the prim.
    """

    path: str = Field(description="USD path to the prim")
    attribute_name: str = Field(description="Name of the attribute to set")
    value: float | int | str | bool | list[float] = Field(description="Value to set (must match attribute type)")


class PrimAttributeValue(Message):
    """
    Response containing an attribute value.
    """

    value: float | int | str | bool | list[float]


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

    path: str = Field(description="USD path to the prim")
    targets: list[SceneTarget] = Field(description="List of applicable scene targets/view types for this prim")


class QueryScene(Message):
    """
    Query the scene hierarchy for prims matching specific criteria.
    """

    root_path: str = Field(default="/World", description="Root path to start the query from")
    target: SceneTarget | None = Field(default=None, description="Specific target type to filter for (None returns all)")


class SceneQueryResponse(Message):
    """
    Response containing the results of a scene query.
    """

    prims: list[PrimInfo] = Field(description="List of matching prims with their applicable targets")


class SetSimulationControls(Message):
    """
    Set simulation control parameters.
    """

    max_physics_dt_us: int | None = Field(default=None, description="Maximum physics timestep in microseconds")
    render_interval_us: int | None = Field(default=None, description="Render interval in microseconds")
