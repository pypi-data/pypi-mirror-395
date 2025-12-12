class SessionError(Exception):
    """
    Base exception for all session-related errors.
    """


class SessionSimRpcNotConnectedError(SessionError):
    """
    Raised when the Sim RPC server is not reachable.
    """


class SessionSimRpcInterruptedError(SessionError):
    """
    Raised when the Sim RPC is interrupted.
    """


class SessionSimRpcClientError(SessionError):
    """
    Raised when the Sim RPC server returns a client error (user error).
    """


class SessionSimRpcInternalError(SessionError):
    """
    Raised when the Sim RPC server returns an internal error with traceback.
    """

    def __init__(self, message: str, traceback: str | None = None):
        super().__init__(message)
        self.traceback = traceback


class SessionAuthError(SessionError):
    """
    Raised when authentication fails.
    """


class SessionAgentError(SessionError):
    """
    Raised when an agent operation fails (start/stop ark, telemetry, etc).
    """


class SessionTaskError(SessionError):
    """
    Raised when a task operation fails (invalid lifecycle, etc).
    """


class SessionArkError(SessionError):
    """
    Raised when an Ark operation fails (loading, stepping, hardware access, etc).
    """


class SessionHardwareError(SessionError):
    """
    Raised when a hardware operation fails.
    """


class SessionAssetError(SessionError):
    """
    Raised when an asset operation fails.
    """


class SessionRecordError(SessionError):
    """
    Raised when a recording operation fails (node output recording, etc).
    """


class SessionValidationError(SessionError):
    """
    Raised when input validation fails (user error).
    """
