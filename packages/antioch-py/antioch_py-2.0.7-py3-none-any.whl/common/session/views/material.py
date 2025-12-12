from pydantic import Field

from common.message import Message


class SetNonVisualMaterial(Message):
    """
    Set non-visual material properties on all Material prims in a subtree.

    These properties define how objects appear to RTX sensors (LiDAR and Radar).
    Based on Isaac Sim's isaacsim.sensors.rtx.nonvisual_materials system.
    """

    path: str = Field(description="USD path of the root prim to configure")
    base: str = Field(description="Base material type (e.g. 'aluminum', 'skin', 'plastic')")
    coating: str = Field(default="none", description="Coating type (e.g. 'none', 'paint', 'clearcoat')")
    attribute: str = Field(default="none", description="Material attribute (e.g. 'none', 'emissive', 'retroreflective')")


class SetNonVisualMaterialResponse(Message):
    """
    Response from setting non-visual material.
    """

    materials_modified: int = Field(description="Number of Material prims modified")
