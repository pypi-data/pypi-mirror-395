from enum import Enum

from pydantic import Field
from pydantic.alias_generators import to_camel

from common.message import Message, Pose, Vector3


class GeometryType(str, Enum):
    """
    Supported geometry types.
    """

    SPHERE = "sphere"
    CUBE = "cube"
    CYLINDER = "cylinder"
    CONE = "cone"
    CAPSULE = "capsule"
    MESH = "mesh"


class MeshApproximation(str, Enum):
    """
    Collision mesh approximation type.

    Values are stored in snake_case for consistency with Rust. Use to_usd()
    to get the camelCase format required by USD/Isaac Sim.
    """

    NONE = "none"
    CONVEX_HULL = "convex_hull"
    CONVEX_DECOMPOSITION = "convex_decomposition"
    BOUNDING_SPHERE = "bounding_sphere"
    BOUNDING_CUBE = "bounding_cube"
    MESH_SIMPLIFICATION = "mesh_simplification"
    SDF = "sdf"
    SPHERE_FILL = "sphere_fill"

    def to_usd(self) -> str:
        """
        Convert to USD camelCase format.

        :return: The USD camelCase format.
        """

        return to_camel(self.value)


class GeometryConfig(Message):
    """
    Configuration for creating geometry.
    """

    geometry_type: GeometryType = Field(description="Geometry type")
    radius: float | None = Field(default=None, description="Radius for sphere/cylinder/cone/capsule")
    height: float | None = Field(default=None, description="Height for cylinder/cone/capsule")
    size: float | None = Field(default=None, description="Size for cube (uniform)")
    color: Vector3 | None = Field(default=None, description="RGB color (0-1)")
    opacity: float = Field(default=1.0, description="Opacity (0=transparent, 1=opaque)")
    enable_collision: bool = Field(default=True, description="Whether to enable collision on this geometry")
    static_friction: float = Field(default=0.5, description="Static friction coefficient")
    dynamic_friction: float = Field(default=0.5, description="Dynamic friction coefficient")
    restitution: float = Field(default=0.2, description="Restitution (bounciness)")
    mesh_file_path: str | None = Field(
        default=None,
        description="Path to mesh file (FBX, OBJ, glTF, STL, etc.) - required for MESH type",
    )
    mesh_approximation: MeshApproximation = Field(
        default=MeshApproximation.CONVEX_DECOMPOSITION,
        description="Mesh approximation method",
    )
    contact_offset: float | None = Field(default=None, description="Distance at which collision detection begins")
    rest_offset: float | None = Field(default=None, description="Minimum separation distance between objects")
    torsional_patch_radius: float | None = Field(default=None, description="Radius for torsional friction calculations")
    min_torsional_patch_radius: float | None = Field(default=None, description="Minimum radius for torsional friction")


class GetGeometry(Message):
    """
    Get an existing geometry view from a prim.
    """

    path: str | None = Field(default=None, description="USD path of the geometry prim")


class GetGeometryResponse(Message):
    """
    Response from getting a geometry.
    """

    path: str


class AddGeometry(Message):
    """
    Add a geometry prim with optional pose.
    """

    path: str = Field(description="USD path for the geometry")
    config: GeometryConfig
    world_pose: "Pose | None" = Field(default=None, description="Optional world pose")
    local_pose: "Pose | None" = Field(default=None, description="Optional local pose")
