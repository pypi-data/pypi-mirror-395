from enum import Enum
from typing import Literal, TypeVar

from common.ark import Ark as ArkDefinition, Environment
from common.message import Message
from common.utils.comms import CommsSession

T = TypeVar("T", bound=Message)


class ContainerSource(str, Enum):
    """
    Source for container images.
    """

    LOCAL = "Local"
    REMOTE = "Remote"


class ContainerState(Message):
    """
    State of a container with metadata.
    """

    _type = "antioch/agent/container_state"

    module_name: str
    running: bool


class StartArkRequest(Message):
    """
    Request to start an Ark.
    """

    _type = "antioch/agent/start_ark_request"

    ark: ArkDefinition
    source: ContainerSource
    environment: Environment
    debug: bool
    timeout: float


class StopArkRequest(Message):
    """
    Request to stop an Ark.
    """

    _type = "antioch/agent/stop_ark_request"

    timeout: float


class RecordTelemetryRequest(Message):
    """
    Request to start recording telemetry.
    """

    _type = "antioch/agent/record_telemetry_request"

    mcap_path: str | None = None
    websocket_port: int | None = None


class SaveTelemetryRequest(Message):
    """
    Request to save telemetry (finalize MCAP without resetting session).
    """

    _type = "antioch/agent/save_telemetry_request"


class AgentResponse(Message):
    """
    Generic response for agent operations.
    """

    _type = "antioch/agent/response"

    success: bool
    error: str | None = None


class AgentStateResponse(Message):
    """
    Agent state response.
    """

    _type = "antioch/agent/state_response"

    running: bool
    ark_active: bool


class ArkStateResponse(Message):
    """
    Ark state response.
    """

    _type = "antioch/agent/ark_state_response"

    state: Literal["started", "stopped"]
    ark_name: str | None = None
    environment: Literal["sim", "real"] | None = None
    debug: bool | None = None
    global_start_time_us: int | None = None
    containers: list[ContainerState] | None = None


class AgentError(Exception):
    """
    Agent operation error.
    """


class AgentValidationError(Exception):
    """
    Agent validation error.
    """


class Agent:
    """
    Client for interacting with the agent that manages Ark containers.

    The agent is a long-lived container that can start, stop, and manage Arks.
    This class provides a simple interface for all agent operations and works
    across all environments (sim/real, local/remote).

    Example:
        agent = Agent()
        agent.start_ark(ark_def, source=ContainerSource.LOCAL)
        state = agent.get_ark_state()
        agent.stop_ark()
    """

    def __init__(self):
        """
        Initialize the agent client.
        """

        self.comms = CommsSession()

    @property
    def connected(self) -> bool:
        """
        Check if the agent is reachable.

        :return: True if connected, False otherwise.
        """

        try:
            self._query_agent(
                path="_agent/get_state",
                response_type=AgentStateResponse,
                timeout=1.0,
            )
            return True
        except Exception:
            return False

    def start_ark(
        self,
        ark: ArkDefinition,
        source: ContainerSource = ContainerSource.LOCAL,
        environment: Environment = Environment.SIM,
        debug: bool = False,
        timeout: float = 30.0,
    ) -> None:
        """
        Start an Ark on the agent by launching all module containers.

        This operation is idempotent. If an Ark is already running, it will be
        gracefully stopped before starting the new one.

        :param ark: Ark definition to start.
        :param source: Container image source (local or remote).
        :param environment: Environment to run in (sim or real).
        :param debug: Enable debug mode.
        :param timeout: Timeout in seconds for modules to become ready (default: 30.0).
        :raises AgentError: If the agent fails to start the Ark.
        """

        response = self._query_agent(
            path="_agent/start_ark",
            response_type=AgentResponse,
            request=StartArkRequest(
                ark=ark,
                source=source,
                environment=environment,
                debug=debug,
                timeout=timeout,
            ),
            timeout=timeout + 10.0,
        )

        if not response.success:
            raise AgentError(f"Failed to start Ark: {response.error}")

    def stop_ark(
        self,
        timeout: float = 30.0,
    ) -> None:
        """
        Stop the currently running Ark on the agent.

        Removes all module containers. The agent continues running and can
        accept requests to start a new Ark.

        :param timeout: Timeout in seconds for stopping containers (default: 30.0).
        :raises AgentError: If the agent fails to stop the Ark.
        """

        response = self._query_agent(
            path="_agent/stop_ark",
            response_type=AgentResponse,
            request=StopArkRequest(timeout=timeout),
            timeout=timeout + 10.0,
        )

        if not response.success:
            raise AgentError(f"Failed to stop Ark: {response.error}")

    def get_ark_state(self) -> ArkStateResponse:
        """
        Get the current state of the Ark running on the agent.

        Returns the current state including all container statuses.

        :return: Current Ark state with container information.
        """

        return self._query_agent(
            path="_agent/ark_state",
            response_type=ArkStateResponse,
            timeout=10.0,
        )

    def record_telemetry(self, mcap_path: str | None = None) -> None:
        """
        Start recording telemetry to an MCAP file.

        Creates an MCAP writer at the specified path. The WebSocket server (port 8765)
        and subscriber task are always active, streaming telemetry continuously.
        If already recording, finalizes the current recording before starting a new one.

        :param mcap_path: Optional path where the MCAP file will be saved.
        :raises AgentError: If the agent fails to start recording telemetry.
        """

        response = self.comms.query(
            path="_agent/record_telemetry",
            response_type=AgentResponse,
            request=RecordTelemetryRequest(mcap_path=mcap_path),
            timeout=5.0,
        )

        if not response.success:
            raise AgentError(f"Failed to start recording telemetry: {response.error}")

    def save_telemetry(self) -> None:
        """
        Save telemetry by finalizing the MCAP file.

        Closes the current MCAP recording if one is active. Does NOT reset the websocket
        session or time tracking - telemetry continues streaming to connected clients.

        :raises AgentError: If the agent fails to save telemetry.
        """

        response = self.comms.query(
            path="_agent/save_telemetry",
            response_type=AgentResponse,
            request=SaveTelemetryRequest(),
            timeout=5.0,
        )

        if not response.success:
            raise AgentError(f"Failed to save telemetry: {response.error}")

    def reset_telemetry(self) -> None:
        """
        Reset telemetry session completely.

        Finalizes any active MCAP recording, resets time tracking, and clears the websocket
        session causing all clients to reset their state. This is useful when clearing the
        scene and starting a new Ark to ensure LET times start from 0 again.

        :raises AgentError: If the agent fails to reset telemetry.
        """

        response = self.comms.query(
            path="_agent/reset_telemetry",
            response_type=AgentResponse,
            timeout=5.0,
        )

        if not response.success:
            raise AgentError(f"Failed to reset telemetry: {response.error}")

    def _query_agent(
        self,
        path: str,
        response_type: type[T],
        request: Message | None = None,
        timeout: float = 10.0,
    ) -> T:
        """
        Execute an agent query.

        :param path: The agent query path.
        :param response_type: Expected response type.
        :param request: Optional request message.
        :param timeout: Query timeout in seconds.
        :return: The response message.
        """

        return self.comms.query(
            path=path,
            response_type=response_type,
            request=request,
            timeout=timeout,
        )
