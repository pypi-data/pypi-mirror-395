from enum import Enum

from pydantic import Field

from common.message import Message, Pose, Vector3


class LightType(str, Enum):
    """
    Supported light types.
    """

    SPHERE = "sphere"
    RECT = "rect"
    DISK = "disk"
    CYLINDER = "cylinder"
    DISTANT = "distant"
    DOME = "dome"


class LightConfig(Message):
    """
    Configuration for creating a light.
    """

    light_type: LightType = Field(default=LightType.SPHERE, description="Light type")
    intensity: float = Field(default=30000.0, description="Light intensity")
    exposure: float = Field(default=10.0, description="Light exposure")
    color: Vector3 = Field(default_factory=Vector3.ones, description="RGB color (0-1)")
    radius: float = Field(default=0.1, description="Radius for sphere lights (meters)")
    width: float | None = Field(default=None, description="Width for rect lights (meters)")
    height: float | None = Field(default=None, description="Height for rect/cylinder lights (meters)")
    length: float | None = Field(default=None, description="Length for cylinder lights (meters)")
    angle: float | None = Field(default=None, description="Angle for distant lights (degrees)")
    texture_file: str | None = Field(default=None, description="Texture file for dome lights")


class GetLight(Message):
    """
    Get an existing light source.
    """

    path: str | None = Field(default=None, description="USD path of the light prim")


class GetLightResponse(Message):
    """
    Response from getting a light.
    """

    path: str


class AddLight(Message):
    """
    Add a light source.
    """

    path: str = Field(description="USD path for the light")
    config: LightConfig
    world_pose: Pose | None = Field(default=None, description="World pose (position and orientation)")
    local_pose: Pose | None = Field(default=None, description="Local pose (translation and orientation)")


class SetLightIntensity(Message):
    """
    Set light intensity.
    """

    path: str
    intensity: float


class SetLightColor(Message):
    """
    Set light color.
    """

    path: str
    color: Vector3


class EnableLight(Message):
    """
    Enable light.
    """

    path: str


class DisableLight(Message):
    """
    Disable light.
    """

    path: str
