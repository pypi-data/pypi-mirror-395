from pydantic import Field

from common.message import Message, Pose, Vector3


class GetXForm(Message):
    """
    Get an existing XForm prim.
    """

    path: str | None = Field(default=None, description="USD path of the XForm prim")


class GetXFormResponse(Message):
    """
    Response from getting an XForm.
    """

    path: str


class AddXForm(Message):
    """
    Add an XForm prim with optional pose and scale.
    """

    path: str = Field(description="USD path for the XForm")
    world_pose: Pose | None = Field(None, description="World pose to set on creation")
    local_pose: Pose | None = Field(None, description="Local pose to set on creation")
    scale: Vector3 | None = Field(None, description="Scale to set on creation")


class SetXformVisibility(Message):
    """
    Set xform visibility.
    """

    path: str
    visible: bool
