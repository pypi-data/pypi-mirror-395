from pathlib import Path

from antioch.session.session import SessionContainer
from common.ark import AssetReference
from common.core import list_local_assets, list_remote_assets, pull_remote_asset


class Asset(SessionContainer):
    """
    Provides methods for interacting with the asset registry.

    All methods handle authentication automatically using the current session's auth context.
    This is a lightweight wrapper around registry functions that manages auth token complexity.

    Example:
        # List local assets
        local_assets = Asset.list_local()

        # List remote assets (requires auth)
        remote_assets = Asset.list_remote()

        # Pull an asset from remote registry
        asset_path = Asset.pull(name="my_asset", version="1.0.0")
    """

    @staticmethod
    def list_local() -> list[AssetReference]:
        """
        List all locally available assets.

        :return: List of AssetReference objects from local storage.
        """

        return list_local_assets()

    @staticmethod
    def list_remote() -> list[AssetReference]:
        """
        List all assets from remote registry.

        Requires authentication. Call session.login() first if not authenticated.

        :return: List of AssetReference objects from remote registry.
        :raises SessionAuthError: If not authenticated.
        """

        return list_remote_assets()

    @staticmethod
    def pull(name: str, version: str, overwrite: bool = False, show_progress: bool = True) -> Path:
        """
        Pull an asset from remote registry to local storage.

        Requires authentication. Call session.login() first if not authenticated.
        If the asset already exists locally, returns the existing path unless overwrite=True.

        :param name: Name of the asset.
        :param version: Version of the asset.
        :param overwrite: Overwrite local asset if it already exists.
        :param show_progress: Show download progress bar.
        :return: Path to the downloaded asset file.
        :raises SessionAuthError: If not authenticated.
        """

        return pull_remote_asset(name=name, version=version, overwrite=overwrite, show_progress=show_progress)
