import time
from enum import Enum

from pydantic import Field

from common.message.base import Message


class LogLevel(str, Enum):
    """
    Log level.
    """

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Log(Message):
    """
    Log entry structure.
    """

    _type = "antioch/log"
    timestamp_us: int = Field(default_factory=lambda: int(time.time_ns() // 1000))
    let_us: int
    level: LogLevel
    message: str | None = None
    channel: str | None = None
    telemetry: bytes | None = None
