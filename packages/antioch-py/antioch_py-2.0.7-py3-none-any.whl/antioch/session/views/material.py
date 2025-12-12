from antioch.session.session import Session
from common.session.views.material import SetNonVisualMaterial, SetNonVisualMaterialResponse


def set_nonvisual_material(
    path: str,
    base: str,
    coating: str = "none",
    attribute: str = "none",
) -> int:
    """
    Set non-visual material properties on all Material prims in a subtree.

    These properties define how objects appear to RTX sensors (LiDAR and Radar).

    Valid base materials:
        Metals: aluminum, steel, oxidized_steel, iron, oxidized_iron, silver, brass,
                bronze, oxidized_bronze_patina, tin
        Polymers: plastic, fiberglass, carbon_fiber, vinyl, plexiglass, pvc, nylon, polyester
        Glass: clear_glass, frosted_glass, one_way_mirror, mirror, ceramic_glass
        Other: asphalt, concrete, leaf_grass, dead_leaf_grass, rubber, wood, bark,
               cardboard, paper, fabric, skin, fur_hair, leather, marble, brick,
               stone, gravel, dirt, mud, water, salt_water, snow, ice, calibration_lambertion
        Default: none

    Valid coatings: none, paint, clearcoat, paint_clearcoat

    Valid attributes: none, emissive, retroreflective, single_sided, visually_transparent

    Example:
        # Make a person visible to radar/lidar with skin material
        count = set_nonvisual_material("/World/person", base="skin")

        # Make a car with aluminum body and paint coating
        count = set_nonvisual_material("/World/car", base="aluminum", coating="paint")

    :param path: USD path of the root prim to configure.
    :param base: Base material type.
    :param coating: Coating type.
    :param attribute: Material attribute.
    :return: Number of Material prims modified.
    """

    response = Session.get_current().query_sim_rpc(
        endpoint="set_nonvisual_material",
        payload=SetNonVisualMaterial(
            path=path,
            base=base,
            coating=coating,
            attribute=attribute,
        ),
        response_type=SetNonVisualMaterialResponse,
    )
    return response.materials_modified
