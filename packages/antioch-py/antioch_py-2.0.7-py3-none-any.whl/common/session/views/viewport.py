from pydantic import Field

from common.message import Message, Vector3


class SetCameraView(Message):
    """
    Set the viewport camera view position and target.
    """

    eye: Vector3 = Field(description="Eye position (camera location) in world coordinates")
    target: Vector3 = Field(description="Target position (look-at point) in world coordinates")
    camera_prim_path: str | None = Field(default=None, description="Optional USD path to the camera prim to configure")


class SetActiveViewportCamera(Message):
    """
    Set which camera is active in the viewport.
    """

    camera_prim_path: str = Field(description="USD path to the camera prim to make active")
