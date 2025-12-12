import json
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from antioch.session.error import SessionTaskError
from antioch.session.scene import Scene
from antioch.session.session import SessionContainer
from common.constants import ANTIOCH_API_URL
from common.core import Agent, AuthHandler
from common.core.task import TaskOutcome
from common.rome import RomeClient
from common.utils.logger import Logger


class Task(SessionContainer):
    """
    Singleton for task management and telemetry recording.

    Uses a lazy singleton pattern - the first instantiation or call to get_current()
    creates the instance, and all subsequent calls return the same instance.

    Provides logging with simulation time context and telemetry recording.
    A task represents a single simulation run with defined outcomes.
    Telemetry is always streamed to WebSocket on port 8765 when started.

    Example:
        scene = Scene()
        task = Task()  # or Task.get_current()

        # Start task (streams to WebSocket on port 8765)
        task.start()

        # Or start task with MCAP recording
        task.start(mcap_path="/tmp/task_telemetry.mcap")

        # Run simulation
        scene.step(dt=0.01)

        # Log telemetry with sim time (automatically recorded when started)
        task.logger.telemetry("velocity", VelocityMessage(...))

        # Finish task with outcome (finalizes telemetry and uploads to cloud)
        task.finish(TaskOutcome.SUCCESS)

        # Or finish without uploading MCAP
        task.finish(TaskOutcome.SUCCESS, upload_mcap=False)
    """

    _current: "Task | None" = None

    def __init__(self):
        """
        Initialize the task.
        """

        super().__init__()
        self._agent = Agent()
        self._scene = Scene()

        self._logger: Logger | None = None
        self._started = False
        self._mcap_path: str | None = None

        # Task metadata for cloud storage
        self._ark_name: str | None = None
        self._ark_version: str | None = None
        self._ark_hash: str | None = None
        self._task_start_time: datetime | None = None

        Task._current = self

    @property
    def logger(self) -> Logger:
        """
        Get the logger with current simulation time.

        Sets the logger's logical execution time to match the current
        simulation time before returning. We lazy load the scene to avoid
        circular dependencies.

        :return: The task logger.
        :raises SessionTaskError: If task has not been started.
        """

        if self._logger is None:
            raise SessionTaskError("Task not started")

        self._logger.set_let(self._scene.time_us)
        return self._logger

    @classmethod
    def get_current(cls) -> "Task":
        """
        Get the current task, creating it if it doesn't exist (lazy singleton).

        :return: The current task.
        """

        if cls._current is None:
            cls._current = Task()
        return cls._current

    @property
    def started(self) -> bool:
        """
        Check if the task is currently started.

        :return: True if task is started, False otherwise.
        """

        return self._started

    def start(self, mcap_path: str | None = None) -> None:
        """
        Start the task and begin streaming telemetry to WebSocket (always active on port 8765).
        Optionally records telemetry to an MCAP file.

        This operation is idempotent - calling it multiple times will finish the previous
        task and start a new one.

        :param mcap_path: Optional path to save MCAP telemetry file (defaults to None for no MCAP recording).
        :raises SessionTaskError: If no Ark is loaded in the scene or if user is not authenticated.
        """

        if self._started:
            print("Task already started. Finish or clear the task before starting a new one")
            return

        # Check that an Ark is loaded
        if self._scene.ark is None:
            raise SessionTaskError("No Ark loaded. Please load an Ark before starting a task")

        # Get auth token
        auth = AuthHandler()
        token = auth.get_token()
        if not token:
            raise SessionTaskError("User not authenticated. Please login first")

        # Store task metadata
        self._ark_name = self._scene.ark.definition.name
        self._ark_version = self._scene.ark.definition.info.version
        self._ark_hash = self._scene.ark.definition.metadata.digest
        self._task_start_time = datetime.now(timezone.utc)

        # Start recording telemetry
        self._agent.record_telemetry(mcap_path)

        # Update task state
        self._logger = Logger(self._session.comms, base_channel="task", print_logs=True)
        self._started = True
        self._mcap_path = mcap_path

    def finish(
        self,
        outcome: TaskOutcome,
        result: dict | None = None,
        bundle_paths: list[Path] | None = None,
        upload_mcap: bool = True,
        show_progress: bool = True,
    ) -> None:
        """
        Finish the task with the specified outcome and optionally upload results to cloud storage.

        Resets telemetry session (finalizes MCAP file if one was created and resets time tracking).
        The WebSocket server remains active.

        If result and/or bundle_paths are provided, uploads them to Antioch for cloud storage.

        :param outcome: The task outcome (defaults to SUCCESS).
        :param result: Optional dictionary of task results (must be JSON-serializable).
        :param bundle_paths: Optional list of file paths to bundle and upload to cloud storage.
        :param upload_mcap: Upload MCAP file to cloud storage if one was recorded (defaults to True).
        :param show_progress: Show upload progress bars (defaults to True).
        :raises SessionTaskError: If task not started or if result is not JSON-serializable.
        """

        if not self._started:
            raise SessionTaskError("Task not started")

        # Validate result is JSON-serializable if provided
        if result is not None:
            try:
                json.dumps(result)
            except (TypeError, ValueError) as e:
                raise SessionTaskError(f"Task result must be JSON-serializable: {e}") from e

        # Validate bundle paths exist and are accessible
        bundle_tar_path = None
        if bundle_paths is not None and len(bundle_paths) > 0:
            for path in bundle_paths:
                if not Path(path).exists():
                    raise SessionTaskError(f"Bundle path does not exist: {path}")
                if not Path(path).is_file():
                    raise SessionTaskError(f"Bundle path is not a file: {path}")

            # Create tar.gz bundle
            try:
                bundle_tar_path = self._create_bundle(bundle_paths)
            except Exception as e:
                raise SessionTaskError(f"Failed to create bundle: {e}") from e

        # Save the MCAP file to disk (does not reset websocket session)
        self._agent.save_telemetry()

        # Upload task to Antioch Cloud
        try:
            task_complete_time = datetime.now(timezone.utc)
            self._upload_task_to_antioch(outcome, result, bundle_tar_path, task_complete_time, upload_mcap, show_progress)
        except Exception as e:
            raise SessionTaskError(f"Failed to upload task to Antioch Cloud: {e}") from e

        # Clean up temp bundle file
        if bundle_tar_path and Path(bundle_tar_path).exists():
            Path(bundle_tar_path).unlink()

        # Reset task state
        self._logger = None
        self._started = False
        self._mcap_path = None
        self._ark_name = None
        self._ark_version = None
        self._ark_hash = None
        self._task_start_time = None

    def _create_bundle(self, bundle_paths: list[Path]) -> str:
        """
        Create a tar.gz archive from the provided file paths.

        :param bundle_paths: List of file paths to include in the bundle.
        :return: Path to the created tar.gz file.
        """

        # Create temp file for the bundle
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as temp_file:
            temp_path = temp_file.name
        with tarfile.open(temp_path, "w:gz") as tar:
            for path in bundle_paths:
                tar.add(str(path), arcname=Path(path).name)

        return temp_path

    def _upload_task_to_antioch(
        self,
        outcome: TaskOutcome,
        result: dict | None,
        bundle_tar_path: str | None,
        task_complete_time: datetime,
        upload_mcap: bool,
        show_progress: bool,
    ) -> None:
        """
        Upload task completion data to Antioch Cloud.

        :param outcome: The task outcome.
        :param result: Optional task result dictionary.
        :param bundle_tar_path: Optional path to bundle tar.gz file.
        :param task_complete_time: ISO 8601 timestamp of task completion.
        :param upload_mcap: Upload MCAP file if one was recorded.
        :param show_progress: Show upload progress bars.
        :raises SessionTaskError: If upload operations fail.
        """

        # Get auth token
        token = AuthHandler().get_token()
        if token is None:
            raise SessionTaskError("User not authenticated. Please login first")

        # Create Rome client
        rome_client = RomeClient(api_url=ANTIOCH_API_URL, token=token)

        # Assert all required fields are set (should never be None at this point)
        assert self._ark_name is not None, "Ark name should be set"
        assert self._ark_version is not None, "Ark version should be set"
        assert self._ark_hash is not None, "Ark hash should be set"
        assert self._task_start_time is not None, "Task start time should be set"

        # Complete the task (creates ES entry)
        try:
            task_id = rome_client.complete_task(
                ark_name=self._ark_name,
                ark_version=self._ark_version,
                ark_hash=self._ark_hash,
                task_start_time=self._task_start_time,
                task_complete_time=task_complete_time,
                outcome=outcome,
                result=result,
            )
        except Exception as e:
            raise SessionTaskError(f"Failed to complete task in Antioch: {e}") from e

        # Upload MCAP if it exists and upload_mcap is True
        if upload_mcap and self._mcap_path:
            if not Path(self._mcap_path).exists():
                raise SessionTaskError(f"MCAP file does not exist, or is inaccessible: {self._mcap_path}")
            try:
                rome_client.upload_mcap(task_id=task_id, mcap_path=self._mcap_path, show_progress=show_progress)
            except Exception as e:
                raise SessionTaskError(f"Failed to upload MCAP to Antioch: {e}") from e

        # Upload bundle if it exists
        if bundle_tar_path:
            if not Path(bundle_tar_path).exists():
                raise SessionTaskError(f"Bundle file does not exist, or is inaccessible: {bundle_tar_path}")
            try:
                rome_client.upload_bundle(task_id=task_id, bundle_path=bundle_tar_path, show_progress=show_progress)
            except Exception as e:
                raise SessionTaskError(f"Failed to upload bundle to Antioch: {e}") from e
