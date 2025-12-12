from datetime import datetime
from pathlib import Path
from typing import Generator, overload

import httpx
import requests
from requests import Response
from tqdm.auto import tqdm

from common.ark import ArkReference, AssetReference
from common.core.task import TaskCompletion, TaskOutcome
from common.rome.error import RomeAuthError, RomeError, RomeNetworkError

DOWNLOAD_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB
UPLOAD_CHUNK_SIZE = 1024  # 1KB
FILE_TRANSFER_UNIT_DIVISOR = 1024


class RomeClient:
    """
    Client for interacting with Rome (Antioch's cloud API).

    Handles task completion, artifact uploads/downloads, and registry operations for Arks and Assets.
    """

    def __init__(self, api_url: str, token: str):
        """
        Initialize the Rome client.

        :param api_url: Base URL for Rome API.
        :param token: Authentication token.
        """

        self._api_url = api_url
        self._token = token

    def complete_task(
        self,
        ark_name: str,
        ark_version: str,
        ark_hash: str,
        task_start_time: datetime,
        task_complete_time: datetime,
        outcome: TaskOutcome,
        result: dict | None = None,
    ) -> str:
        """
        Complete a task by creating an entry in Antioch's database.

        :param ark_name: Name of the Ark.
        :param ark_version: Version of the Ark.
        :param ark_hash: Hash of the Ark.
        :param task_start_time: Task start time.
        :param task_complete_time: Task completion time.
        :param outcome: Task outcome (success or failure).
        :param result: Optional task result dictionary.
        :return: The task ID.
        """

        payload = TaskCompletion(
            ark_name=ark_name,
            ark_version=ark_version,
            ark_hash=ark_hash,
            task_start_time=task_start_time,
            task_complete_time=task_complete_time,
            outcome=outcome,
            result=result,
        )

        response = self._send_request("POST", "/tasks/complete", json=payload.model_dump(mode="json"))
        return response["task_id"]

    def upload_mcap(self, task_id: str, mcap_path: str, show_progress: bool = True) -> None:
        """
        Upload MCAP file to Rome's cloud storage using streaming.

        :param task_id: Unique task identifier.
        :param mcap_path: Path to the MCAP file.
        :param show_progress: Show upload progress bar.
        """

        self._upload_file(
            endpoint="/tasks/upload_mcap",
            task_id=task_id,
            file_path=mcap_path,
            content_type="application/octet-stream",
            show_progress=show_progress,
        )

    def upload_bundle(self, task_id: str, bundle_path: str, show_progress: bool = True) -> None:
        """
        Upload bundle tar.gz file to Rome's cloud storage using streaming.

        :param task_id: Unique task identifier.
        :param bundle_path: Path to the bundle tar.gz file.
        :param show_progress: Show upload progress bar.
        """

        self._upload_file(
            endpoint="/tasks/upload_bundle",
            task_id=task_id,
            file_path=bundle_path,
            content_type="application/gzip",
            show_progress=show_progress,
        )

    def download_mcap(self, task_id: str, output_path: str, show_progress: bool = True, overwrite: bool = False) -> str:
        """
        Download MCAP file from Rome's cloud storage.

        :param task_id: Unique task identifier.
        :param output_path: Path where the file should be saved.
        :param show_progress: Show download progress bar.
        :param overwrite: Overwrite existing file.
        :return: Path to the downloaded MCAP file.
        """

        if not output_path.endswith(".mcap"):
            raise ValueError("Output path must end with .mcap")

        return self._download_file(
            endpoint="/tasks/download-mcap",
            output_path=output_path,
            params={"task_id": task_id},
            show_progress=show_progress,
            overwrite=overwrite,
        )

    def download_bundle(self, task_id: str, output_path: str, show_progress: bool = True, overwrite: bool = False) -> str:
        """
        Download bundle tar.gz file from Rome's cloud storage.

        :param task_id: Unique task identifier.
        :param output_path: Path where the file should be saved.
        :param show_progress: Show download progress bar.
        :param overwrite: Overwrite existing file.
        :return: Path to the downloaded bundle file.
        """

        if not output_path.endswith(".tar.gz"):
            raise ValueError("Output path must end with .tar.gz")

        return self._download_file(
            endpoint="/tasks/download-bundle",
            output_path=output_path,
            params={"task_id": task_id},
            show_progress=show_progress,
            overwrite=overwrite,
        )

    def list_arks(self) -> list[ArkReference]:
        """
        List all Arks from Rome registry.

        :return: List of ArkReference objects from remote registry.
        """

        response = self._send_request("GET", "/ark/list")
        return [ArkReference(**ark) for ark in response.get("data", [])]

    def get_ark(self, name: str, version: str) -> dict:
        """
        Get Ark definition from Rome registry.

        :param name: Name of the Ark.
        :param version: Version of the Ark.
        :return: Ark definition as dictionary.
        """

        response = self._send_request("GET", "/ark/get", json={"name": name, "version": version})
        return response["ark"]

    def download_ark_assets(self, name: str, version: str) -> bytes:
        """
        Download Ark asset file from Rome registry.

        :param name: Name of the Ark.
        :param version: Version of the Ark.
        :return: Asset file content as bytes.
        """

        response = self._send_request("GET", "/ark/download-assets", params={"name": name, "version": version}, return_content=True)
        assert isinstance(response, bytes)
        return response

    def list_assets(self) -> list[AssetReference]:
        """
        List all assets from Rome registry.

        :return: List of AssetReference objects from remote registry.
        """

        response = self._send_request("GET", "/asset/list")
        return [AssetReference(**asset) for asset in response.get("data", [])]

    def get_asset_metadata(self, name: str, version: str) -> dict:
        """
        Get metadata for a specific asset version.

        :param name: Name of the asset.
        :param version: Version of the asset.
        :return: Asset metadata dictionary containing extension, file_size, and modified_time.
        """

        response = self._send_request("GET", "/asset/metadata", params={"name": name, "version": version})
        return response["data"]

    def download_asset(self, name: str, version: str, output_path: str, show_progress: bool = True) -> None:
        """
        Download asset from Rome registry to local storage.

        :param name: Name of the asset.
        :param version: Version of the asset.
        :param output_path: Path where the file should be saved.
        :param show_progress: Show download progress bar.
        """

        self._download_file(
            endpoint="/asset/download",
            output_path=output_path,
            params={"name": name, "version": version},
            show_progress=show_progress,
            description=f"Downloading {name}:{version}",
        )

    @overload
    def _send_request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        return_content: bool = False,
    ) -> dict: ...

    @overload
    def _send_request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        return_content: bool = True,
    ) -> bytes: ...

    def _send_request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
        params: dict | None = None,
        return_content: bool = False,
    ) -> dict | bytes:
        """
        Send a request to Rome API with standardized error handling.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint path.
        :param json: Optional JSON payload.
        :param params: Optional query parameters.
        :param return_content: If True, return raw bytes content instead of JSON.
        :return: Response JSON data or raw content bytes.
        :raises RomeAuthError: If user is not authenticated.
        :raises RomeError: If client error (4xx) occurs or JSON decode fails.
        :raises RomeNetworkError: If network error or server error (5xx) occurs.
        """

        if not self._token:
            raise RomeAuthError("User not authenticated")

        try:
            url = f"{self._api_url}{endpoint}"
            headers = {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}
            response = requests.request(method, url, json=json, params=params, headers=headers, timeout=30)
            self._check_response_errors(response)

            if return_content:
                return response.content

            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                raise RomeError(f"Invalid JSON response: {e}") from e
        except requests.exceptions.RequestException as e:
            raise RomeNetworkError(f"Network error: {e}") from e

    def _download_file(
        self,
        endpoint: str,
        output_path: str,
        params: dict | None = None,
        show_progress: bool = True,
        overwrite: bool = True,
        description: str | None = None,
    ) -> str:
        """
        Download a file from Rome's cloud storage with streaming.

        :param endpoint: API endpoint path.
        :param output_path: Path where the file should be saved.
        :param params: Optional query parameters.
        :param show_progress: Show download progress bar.
        :param overwrite: Overwrite existing file.
        :param description: Optional description for progress bar.
        :return: Path to the downloaded file.
        :raises RuntimeError: If file exists and overwrite is False.
        :raises RomeAuthError: If user is not authenticated.
        :raises RomeError: If client error (4xx) occurs.
        :raises RomeNetworkError: If network error or server error (5xx) occurs.
        """

        if not overwrite and Path(output_path).exists():
            raise RuntimeError(f"{output_path} already exists (pass overwrite=True to overwrite)")
        if not self._token:
            raise RomeAuthError("User not authenticated")

        try:
            url = f"{self._api_url}{endpoint}"
            headers = {"Authorization": f"Bearer {self._token}"}
            response = requests.get(url, params=params, headers=headers, stream=True, timeout=None)
            self._check_response_errors(response)

            with (
                open(output_path, "wb") as f,
                tqdm(
                    total=int(response.headers.get("content-length", 0)),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=FILE_TRANSFER_UNIT_DIVISOR,
                    desc=description or f"Downloading {Path(output_path).name}",
                    disable=not show_progress,
                ) as pbar,
            ):
                for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

            return output_path
        except requests.exceptions.RequestException as e:
            raise RomeNetworkError(f"Network error: {e}") from e

    def _upload_file_stream(self, file_path: Path, show_progress: bool = True) -> Generator[bytes, None, None]:
        """
        Generator for streaming file upload with progress tracking.

        :param file_path: Path to the file to upload.
        :param show_progress: Show upload progress bar.
        :return: Generator yielding file chunks as bytes.
        """

        with (
            tqdm(
                total=file_path.stat().st_size,
                unit="B",
                unit_scale=True,
                unit_divisor=FILE_TRANSFER_UNIT_DIVISOR,
                desc=f"Uploading {file_path.name}",
                disable=not show_progress,
            ) as pbar,
            open(file_path, "rb") as f,
        ):
            while data := f.read(UPLOAD_CHUNK_SIZE):
                pbar.update(len(data))
                yield data

    def _upload_file(
        self,
        endpoint: str,
        task_id: str,
        file_path: str,
        content_type: str,
        show_progress: bool,
    ) -> None:
        """
        Upload a file to Rome's cloud storage using streaming.

        :param endpoint: API endpoint path.
        :param task_id: Unique task identifier.
        :param file_path: Path to the file to upload.
        :param content_type: MIME type of the file.
        :param show_progress: Show upload progress bar.
        :raises RomeAuthError: If user is not authenticated.
        :raises RomeError: If client error (4xx) occurs.
        :raises RomeNetworkError: If network error or server error (5xx) occurs.
        """

        if not self._token:
            raise RomeAuthError("User not authenticated")

        try:
            url = f"{self._api_url}{endpoint}"
            headers = {"Authorization": f"Bearer {self._token}", "Content-Type": content_type}
            stream_data = self._upload_file_stream(Path(file_path), show_progress)
            with httpx.Client(timeout=None) as client:
                response = client.post(url, params={"task_id": task_id}, content=stream_data, headers=headers)
            self._check_response_errors(response)
        except httpx.HTTPError as e:
            raise RomeNetworkError(f"Network error: {e}") from e

    def _check_response_errors(self, response: Response | httpx.Response) -> None:
        """
        Check response for HTTP errors and raise appropriate exceptions.

        :param response: HTTP response object from requests or httpx.
        :raises RomeError: If client error (4xx) occurs.
        :raises RomeNetworkError: If server error (5xx) occurs.
        """

        if response.status_code >= 400:
            error_message = self._extract_error_message(response)
            if response.status_code < 500:
                raise RomeError(error_message)
            raise RomeNetworkError(f"Server error: {error_message}")

    def _extract_error_message(self, response: Response | httpx.Response) -> str:
        """
        Extract error message from response JSON or return generic message.

        :param response: HTTP response object from requests or httpx.
        :return: Error message string from response or generic HTTP status message.
        """

        try:
            data = response.json()
            if isinstance(data, dict) and "message" in data:
                return data["message"]
        except Exception:
            pass
        return f"HTTP {response.status_code}"
