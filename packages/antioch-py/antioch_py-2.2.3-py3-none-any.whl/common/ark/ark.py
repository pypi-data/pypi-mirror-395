from enum import Enum

from common.ark.hardware import Hardware
from common.ark.kinematics import Joint, Link
from common.ark.module import Module
from common.ark.scheduler import NodeEdge
from common.message import Message


class Environment(str, Enum):
    """
    The environment of the Ark.

    :cvar SIM: The simulation environment.
    :cvar REAL: The real environment.
    :cvar ALL: All environments.
    """

    SIM = "sim"
    REAL = "real"
    ALL = "all"

    def __str__(self) -> str:
        return self.value


class ArkMetadata(Message):
    """
    Metadata about the Ark.
    """

    digest: str
    version: str
    timestamp: str
    asset_hash: str | None = None


class ArkInfo(Message):
    """
    Information about the Ark.
    """

    description: str
    version: str


class Kinematics(Message):
    """
    The kinematics of the Ark.
    """

    links: list[Link]
    joints: list[Joint]


class ArkVersionReference(Message):
    """
    Reference to an Ark version in the remote Ark registry.
    """

    version: str
    created_at: str
    updated_at: str
    full_path: str
    size_bytes: int
    asset_path: str | None = None
    asset_size_bytes: int | None = None
    metadata: dict[str, str] = {}


class ArkReference(Message):
    """
    Reference to an Ark in the remote Ark registry.
    """

    name: str
    versions: list[ArkVersionReference]
    created_at: str
    updated_at: str


class AssetVersionReference(Message):
    """
    Reference to a specific asset version.
    """

    version: str
    full_path: str
    size_bytes: int
    created_at: str
    updated_at: str
    metadata: dict[str, str] = {}


class AssetReference(Message):
    """
    Reference to an asset with all its versions.
    """

    name: str
    versions: list[AssetVersionReference]
    created_at: str
    updated_at: str


class Ark(Message):
    """
    Antioch Ark specification.
    """

    metadata: ArkMetadata
    name: str
    capability: Environment
    info: ArkInfo
    modules: list[Module]
    edges: list[NodeEdge]
    kinematics: Kinematics
    hardware: list[Hardware]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ark_file", type=str, help="The Ark json file to serialize")
    args = parser.parse_args()

    with open(args.ark_file) as f:
        ark = Ark.model_validate_json(f.read())
        print(ark.to_json(2))
