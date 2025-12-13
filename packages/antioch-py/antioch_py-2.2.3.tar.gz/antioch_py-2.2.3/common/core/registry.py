import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from common.ark import Ark as ArkDefinition, ArkReference, ArkVersionReference, AssetReference, AssetVersionReference
from common.constants import ANTIOCH_API_URL, get_ark_dir, get_asset_dir
from common.core.auth import AuthError, AuthHandler
from common.rome import RomeClient


def list_local_arks() -> list[ArkReference]:
    """
    List all locally available Arks.

    :return: List of ArkReference objects from local storage.
    """

    arks_dir = get_ark_dir()
    files_by_name = defaultdict(list)
    for file_path in arks_dir.iterdir():
        if file_path.is_file() and (file_path.name.endswith(":ark.json") or file_path.name.endswith(":asset.usdz")):
            name = file_path.name.split(":")[0]
            files_by_name[name].append(file_path)

    results = []
    for name, files in files_by_name.items():
        ref = _build_ark_reference(name, files)
        if ref is not None:
            results.append(ref)

    return results


def load_local_ark(name: str, version: str) -> ArkDefinition:
    """
    Load Ark definition from local storage.

    :param name: Name of the Ark.
    :param version: Version of the Ark.
    :return: The loaded Ark definition.
    """

    with open(get_ark_version_reference(name, version).full_path) as f:
        return ArkDefinition(**json.load(f))


def get_ark_version_reference(name: str, version: str) -> ArkVersionReference:
    """
    Get version reference for an Ark.

    :param name: Name of the Ark.
    :param version: Version of the Ark.
    :return: Version reference for the Ark.
    """

    available_arks = list_local_arks()
    for ark_ref in available_arks:
        if ark_ref.name == name:
            for version_ref in ark_ref.versions:
                if version_ref.version == version:
                    return version_ref
            raise FileNotFoundError(f"Version {version} of Ark {name} not found in local storage")
    raise FileNotFoundError(f"No versions of Ark {name} found in local storage")


def get_asset_path(name: str, version: str, extension: str = "usdz", assert_exists: bool = True) -> Path:
    """
    Get the local file path for a specific asset version.

    :param name: Name of the asset.
    :param version: Version of the asset.
    :param extension: File extension (without dot), defaults to 'usdz'.
    :param assert_exists: If True, raises error if asset file doesn't exist.
    :return: Path to the asset file.
    """

    assets_dir = get_asset_dir()
    asset_file = assets_dir / f"{name}:{version}:file.{extension}"
    if assert_exists and not asset_file.exists():
        raise FileNotFoundError(f"Asset {name}:{version} with extension .{extension} does not exist")

    return asset_file


def list_local_assets() -> list[AssetReference]:
    """
    List all locally cached assets.

    :return: List of AssetReference objects from local storage.
    """

    assets_dir = get_asset_dir()
    if not assets_dir.exists():
        return []

    files_by_name: dict[str, list[Path]] = defaultdict(list)
    for file_path in assets_dir.iterdir():
        if file_path.is_file():
            # Parse filename format: {name}:{version}:file.{extension}
            parts = file_path.stem.split(":")
            if len(parts) == 3 and parts[-1] == "file":
                files_by_name[parts[0]].append(file_path)

    results = []
    for name, files in files_by_name.items():
        ref = _build_asset_reference(name, files)
        if ref is not None:
            results.append(ref)

    return results


def list_remote_arks() -> list[ArkReference]:
    """
    List all Arks from remote registry.

    Requires authentication.

    :return: List of ArkReference objects from remote registry.
    :raises AuthError: If not authenticated.
    """

    # Get auth token
    auth = AuthHandler()
    token = auth.get_token()
    if token is None:
        raise AuthError("User not authenticated. Please login first")

    # Create Rome client and list arks
    rome_client = RomeClient(api_url=ANTIOCH_API_URL, token=token)
    return rome_client.list_arks()


def pull_remote_ark(name: str, version: str, overwrite: bool = False) -> ArkDefinition:
    """
    Pull an Ark from remote registry to local storage.

    Requires authentication.

    :param name: Name of the Ark.
    :param version: Version of the Ark.
    :param overwrite: Overwrite local Ark if it already exists.
    :return: The loaded Ark definition.
    :raises AuthError: If not authenticated.
    """

    # Check if Ark already exists locally
    arks_dir = get_ark_dir()
    ark_json_path = arks_dir / f"{name}:{version}:ark.json"
    if ark_json_path.exists() and not overwrite:
        return load_local_ark(name, version)

    # Get auth token
    auth = AuthHandler()
    token = auth.get_token()
    if not token:
        raise AuthError("User not authenticated. Please login first")

    # Create Rome client and fetch Ark definition and save to local storage
    rome_client = RomeClient(api_url=ANTIOCH_API_URL, token=token)
    ark = rome_client.get_ark(name=name, version=version)

    # Save Ark JSON
    with open(ark_json_path, "wb") as f:
        f.write(json.dumps(ark).encode("utf-8"))

    # Download asset usdz only if ark has asset_hash (hardware modules exist)
    if ark.get("metadata", {}).get("asset_hash") is not None:
        asset_content = rome_client.download_ark_assets(name=name, version=version)
        with open(arks_dir / f"{name}:{version}:asset.usdz", "wb") as f:
            f.write(asset_content)

    return ArkDefinition(**ark)


def list_remote_assets() -> list[AssetReference]:
    """
    List all assets from remote registry.

    Requires authentication.

    :return: List of AssetReference objects from remote registry.
    :raises AuthError: If not authenticated.
    """

    # Get auth token
    token = AuthHandler().get_token()
    if token is None:
        raise AuthError("User not authenticated. Please login first")

    # Create Rome client and list assets
    rome_client = RomeClient(api_url=ANTIOCH_API_URL, token=token)
    return rome_client.list_assets()


def pull_remote_asset(name: str, version: str, overwrite: bool = False, show_progress: bool = True) -> Path:
    """
    Pull an asset from remote registry to local storage.

    Requires authentication.

    :param name: Name of the asset.
    :param version: Version of the asset.
    :param overwrite: Overwrite local asset if it already exists.
    :param show_progress: Show download progress bar.
    :return: Path to the downloaded asset file.
    :raises AuthError: If not authenticated.
    """

    # Get auth token
    token = AuthHandler().get_token()
    if token is None:
        raise AuthError("User not authenticated. Please login first")

    # Create Rome client and get asset metadata to determine extension
    rome_client = RomeClient(api_url=ANTIOCH_API_URL, token=token)
    metadata = rome_client.get_asset_metadata(name=name, version=version)
    extension = metadata.get("extension", "usdz")

    # Check if asset already exists locally
    asset_file_path = get_asset_path(name=name, version=version, extension=extension, assert_exists=False)
    if asset_file_path.exists() and not overwrite:
        print(f"Asset {name}:{version} already exists locally, skipping download")
        return asset_file_path

    # Download the asset file
    rome_client.download_asset(name=name, version=version, output_path=str(asset_file_path), show_progress=show_progress)
    return asset_file_path


def _build_ark_reference(name: str, files: list[Path]) -> ArkReference | None:
    """
    Create an ArkReference from a list of files for a given ark.

    :param name: The name of the ark.
    :param files: List of file paths (ark JSON and asset USDZ files).
    :return: ArkReference object or None if no valid versions found.
    """

    file_stats = [f.stat() for f in files]
    created_at = min(datetime.fromtimestamp(stat.st_ctime) for stat in file_stats).isoformat()
    updated_at = max(datetime.fromtimestamp(stat.st_mtime) for stat in file_stats).isoformat()

    # Group files by version - parse from {name}:{version}:ark.json or {name}:{version}:asset.usdz
    files_by_version: dict[str, list[Path]] = defaultdict(list)
    for file_path in files:
        files_by_version[file_path.name.split(":")[1]].append(file_path)

    # Create an ArkVersionReference for each version
    version_refs = []
    for version, version_files in files_by_version.items():
        ark_file = None
        asset_file = None
        for file_path in version_files:
            if file_path.name.endswith(":ark.json"):
                ark_file = file_path
            elif file_path.name.endswith(":asset.usdz"):
                asset_file = file_path
        if ark_file is None:
            continue

        ark_stat = ark_file.stat()
        version_refs.append(
            ArkVersionReference(
                version=version,
                full_path=str(ark_file),
                asset_path=str(asset_file) if asset_file else None,
                size_bytes=ark_stat.st_size,
                created_at=datetime.fromtimestamp(ark_stat.st_ctime).isoformat(),
                updated_at=datetime.fromtimestamp(ark_stat.st_mtime).isoformat(),
                asset_size_bytes=asset_file.stat().st_size if asset_file else None,
            )
        )

    if not version_refs:
        return None

    return ArkReference(
        name=name,
        versions=version_refs,
        created_at=created_at,
        updated_at=updated_at,
    )


def _build_asset_reference(name: str, files: list[Path]) -> AssetReference | None:
    """
    Create an AssetReference from a list of files for a given asset.

    :param name: The name of the asset.
    :param files: List of file paths (.usdz files).
    :return: AssetReference object or None if no valid versions found.
    """

    file_stats = [f.stat() for f in files]
    created_at = min(datetime.fromtimestamp(stat.st_ctime) for stat in file_stats).isoformat()
    updated_at = max(datetime.fromtimestamp(stat.st_mtime) for stat in file_stats).isoformat()

    # Group files by version
    files_by_version: dict[str, list[Path]] = defaultdict(list)
    for file_path in files:
        # Parse filename format: {name}:{version}:file.usdz
        version = file_path.name.split(":")[1]
        files_by_version[version].append(file_path)

    # Create an AssetVersionReference for each version
    version_refs = []
    for version, version_files in files_by_version.items():
        # Should only be one file per version, but take first if multiple
        asset_file = version_files[0]
        asset_stat = asset_file.stat()
        version_refs.append(
            AssetVersionReference(
                version=version,
                full_path=str(asset_file),
                size_bytes=asset_stat.st_size,
                created_at=datetime.fromtimestamp(asset_stat.st_ctime).isoformat(),
                updated_at=datetime.fromtimestamp(asset_stat.st_mtime).isoformat(),
            )
        )

    if not version_refs:
        return None

    return AssetReference(
        name=name,
        versions=version_refs,
        created_at=created_at,
        updated_at=updated_at,
    )
