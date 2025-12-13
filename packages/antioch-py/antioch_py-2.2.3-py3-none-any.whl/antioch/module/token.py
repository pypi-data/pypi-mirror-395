from enum import Enum

from common.message import Message
from common.utils.time import now_us


class TokenType(str, Enum):
    """
    Token status types.
    """

    DATA = "data"
    SHORT_CIRCUIT = "short_circuit"
    ERROR = "error"
    OVERRUN = "overrun"
    SKIPPED = "skipped"


class Token(Message):
    """
    Token representing data flow between nodes.
    """

    _type = "antioch/token"
    module_name: str
    node_name: str
    output_name: str
    let_us: int
    budget_us: int
    start_timestamp_us: int
    status: TokenType
    payload: bytes | None = None
    error: str | None = None

    def elapsed(self) -> int:
        """
        Get elapsed time in microseconds since token creation.

        :return: Elapsed time in microseconds.
        """

        return now_us() - self.start_timestamp_us
