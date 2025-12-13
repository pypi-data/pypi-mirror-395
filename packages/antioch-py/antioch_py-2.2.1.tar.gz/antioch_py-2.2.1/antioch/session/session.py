import os
import time
from typing import Any, overload

from antioch.session.error import (
    SessionSimRpcClientError,
    SessionSimRpcInternalError,
    SessionSimRpcInterruptedError,
    SessionSimRpcNotConnectedError,
)
from common.core.auth import AuthHandler
from common.message import Message
from common.session.sim import RpcCall, RpcResponse, SimulationInfo
from common.utils.comms import CommsSession


class SessionContainer:
    """
    Base class for all session containers.

    Provides common functionality for accessing the session client. Session containers
    include Scene, Ark, and SessionContainer subclasses. This base class only manages the
    session connection - path management is delegated to SessionContainer subclasses.
    """

    def __init__(self):
        """
        Initialize the session container.
        """

        self._session = Session.get_current()

    @property
    def connected(self) -> bool:
        """
        Check if the session is connected to the Sim RPC server.

        :return: True if connected, False otherwise.
        """

        return self._session.connected


class Session:
    """
    Singleton client for interacting with the Sim RPC server.

    Uses a lazy singleton pattern - the first call to get_current() creates the instance,
    and all subsequent calls return the same instance.

    Example:
        session = Session.get_current()
        result = session.query_sim_rpc("get_state")
    """

    _current: "Session | None" = None

    def __init__(self, timeout: float = 10.0, debug: bool = False):
        """
        Initialize the session client.

        :param timeout: Default timeout for Sim RPC calls in seconds.
        :param debug: Whether to enable debug mode.
        """

        self._comms = CommsSession()
        self._timeout = timeout
        self._debug = debug or os.environ.get("ANTIOCH_RPC_PROFILE", "0") == "1"
        Session._current = self

    def __del__(self):
        """
        Close the client connection.
        """

        self._comms.close()

    @classmethod
    def get_current(cls) -> "Session":
        """
        Get the current session client, creating it if it doesn't exist (lazy singleton).

        :return: The current session client.
        """

        if cls._current is None:
            cls._current = Session()
        return cls._current

    @property
    def connected(self) -> bool:
        """
        Check if the simulation RPC server is reachable.

        :return: True if connected, False otherwise.
        """

        try:
            self.query_sim_rpc("get_info", response_type=SimulationInfo, timeout=1.0)
            return True
        except Exception:
            return False

    @property
    def comms(self) -> CommsSession:
        """
        Get the comms session.

        :return: The comms session.
        """

        return self._comms

    @property
    def authenticated(self) -> bool:
        """
        Check if user is authenticated.

        :return: True if a valid access token exists, False otherwise.
        """

        return AuthHandler().get_token() is not None

    def login(self) -> None:
        """
        Authenticate user and cache access token.

        Initiates OAuth2 device code flow, prompting user to visit a URL and enter a code.
        The access token is cached locally for subsequent requests.

        :raises AuthError: If authentication fails.
        """

        AuthHandler().login()

    @overload
    def query_sim_rpc(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        *,
        timeout: float = 60.0,
    ) -> Any | None: ...

    @overload
    def query_sim_rpc[T](
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        *,
        response_type: type[T],
        timeout: float = 60.0,
    ) -> T: ...

    def query_sim_rpc[T](
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        *,
        response_type: type[T] | None = None,
        timeout: float = 60.0,
    ) -> T | Any | None:
        """
        Execute a sim RPC query.

        :param endpoint: The sim RPC endpoint.
        :param payload: Optional request payload dict.
        :param response_type: Expected response type (Message subclass or primitive like int, str, bool).
        :param timeout: Query timeout in seconds.
        :return: Response as typed object, arbitrary data, or None.
        :raises SessionSimRpcNotConnectedError: If the Sim RPC server is not reachable.
        :raises SessionSimRpcClientError: If the Sim RPC server returns a client error.
        :raises SessionSimRpcInternalError: If the Sim RPC server returns an internal error.
        """

        try:
            start_time = time.perf_counter() if self._debug else 0
            response = self._comms.query(
                path=f"_sim/rpc/{endpoint}",
                response_type=RpcResponse,
                request=RpcCall(data=payload),
                timeout=timeout or self._timeout,
            )

            # Check for errors in RPC response
            if response.error is not None:
                if response.error.internal:
                    raise SessionSimRpcInternalError(message=response.error.message, traceback=response.error.traceback)
                else:
                    raise SessionSimRpcClientError(response.error.message)

            # Print elapsed time in debug mode
            if self._debug:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                print(f"[SIM-RPC] {endpoint}: {elapsed_ms:.1f}ms", flush=True)

            # Return response data or None if no data
            if response.data is None:
                return None
            if response_type is not None:
                if issubclass(response_type, Message):
                    return response_type.model_validate(response.data)
                return response.data
            return response.data

        except TimeoutError as e:
            if not self.connected:
                raise SessionSimRpcNotConnectedError("Sim RPC server is not connected") from e
            raise
        except KeyboardInterrupt as e:
            raise SessionSimRpcInterruptedError("Sim RPC interrupted") from e
