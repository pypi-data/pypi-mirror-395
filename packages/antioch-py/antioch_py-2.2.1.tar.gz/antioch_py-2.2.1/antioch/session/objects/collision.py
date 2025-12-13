from antioch.session.session import Session
from common.session.config import MeshApproximation


def set_collision(path: str, mesh_approximation: MeshApproximation | None = None) -> None:
    """
    Apply collision API to a prim, optionally with mesh approximation.

    :param path: USD path to the prim.
    :param mesh_approximation: Optional mesh approximation method for collision geometry.
    """

    Session.get_current().query_sim_rpc(endpoint="set_collision", payload={"path": path, "mesh_approximation": mesh_approximation})


def remove_collision(path: str) -> None:
    """
    Remove collision API from a prim.

    :param path: USD path to the prim.
    """

    Session.get_current().query_sim_rpc(endpoint="remove_collision", payload={"path": path})


def has_collision(path: str) -> bool:
    """
    Check if a prim has collision API applied.

    :param path: USD path to the prim.
    :return: True if collision API is applied.
    """

    return Session.get_current().query_sim_rpc(endpoint="has_collision", payload={"path": path}, response_type=bool)


def get_mesh_approximation(path: str) -> MeshApproximation | None:
    """
    Get mesh collision approximation from a prim.

    :param path: USD path to the prim.
    :return: Mesh approximation method, or None if not set.
    """

    result = Session.get_current().query_sim_rpc(endpoint="get_mesh_approximation", payload={"path": path})
    return MeshApproximation(result) if result else None
