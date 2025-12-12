from collections import deque
from threading import Lock
from typing import TypeVar, overload

from antioch.module.node import TOKEN_OUTPUT_PATH
from antioch.module.token import Token, TokenType
from antioch.session.error import SessionRecordError
from common.ark.ark import Ark as ArkDefinition
from common.message import Message
from common.utils.comms import CommsSession

T = TypeVar("T", bound=Message)


class NodeOutputRecorder:
    """
    Records node outputs by subscribing to token stream with filtering and buffering.

    Maintains a circular buffer of recent tokens using async callback for efficient updates.
    Validates that module/node/output exists in the Ark definition.
    """

    def __init__(
        self,
        comms: CommsSession,
        ark_def: ArkDefinition,
        module_name: str,
        node_name: str,
        output_name: str,
        token_type: TokenType | None = TokenType.DATA,
        last_n: int = 10,
    ):
        """
        Initialize node output recorder with validation and subscription.

        :param comms: Communication session for subscribing to token stream.
        :param ark_def: Ark definition used to validate module/node/output exists.
        :param module_name: Name of module containing the node.
        :param node_name: Name of node containing the output.
        :param output_name: Name of output to record tokens from.
        :param token_type: Token type to filter (None records all types).
        :param last_n: Maximum number of recent tokens to buffer.
        :raises SessionRecordError: If module, node, or output doesn't exist in Ark.
        """

        # Validate module exists
        module = next((m for m in ark_def.modules if m.name == module_name), None)
        if module is None:
            raise SessionRecordError(f"Module '{module_name}' not found in Ark")

        # Validate node exists
        node = module.nodes.get(node_name)
        if node is None:
            raise SessionRecordError(f"Node '{node_name}' not found in module '{module_name}'")

        # Validate output exists
        output = node.outputs.get(output_name)
        if output is None:
            raise SessionRecordError(f"Output '{output_name}' not found in node '{module_name}/{node_name}'")

        self._token_type = token_type
        self._buffer: deque[Token] = deque(maxlen=last_n)
        self._buffer_lock = Lock()
        self._subscriber = comms.declare_callback_subscriber(TOKEN_OUTPUT_PATH.format(path=output.path), self._on_token)

    @overload
    def next(self, message_cls: type[T]) -> T | None: ...

    @overload
    def next(self, message_cls: None = None) -> dict | None: ...

    def next(self, message_cls: type[T] | None = None) -> T | dict | None:
        """
        Return next deserialized payload in order and remove from buffer.

        :param message_cls: Message class to deserialize payload (None for generic JSON dict).
        :return: Deserialized payload, or None if buffer empty.
        """

        token = self.next_token()
        if token is None:
            return None
        return self._deserialize_payload(token, message_cls)

    @overload
    def latest(self, message_cls: type[T]) -> T | None: ...

    @overload
    def latest(self, message_cls: None = None) -> dict | None: ...

    def latest(self, message_cls: type[T] | None = None) -> T | dict | None:
        """
        Return latest deserialized payload and clear entire buffer.

        :param message_cls: Message class to deserialize payload (None for generic JSON dict).
        :return: Deserialized payload, or None if buffer empty.
        """

        token = self.latest_token()
        if token is None:
            return None
        return self._deserialize_payload(token, message_cls)

    def next_token(self) -> Token | None:
        """
        Return next token in order and remove from buffer.

        :return: Token, or None if buffer empty.
        """

        with self._buffer_lock:
            if not self._buffer:
                return None
            return self._buffer.popleft()

    def latest_token(self) -> Token | None:
        """
        Return latest buffered token and clear entire buffer.

        :return: Token, or None if buffer empty.
        """

        with self._buffer_lock:
            if not self._buffer:
                return None
            token = self._buffer[-1]
            self._buffer.clear()
            return token

    def _on_token(self, sample) -> None:
        """
        Callback invoked when token arrives, filters by type and adds to buffer.

        :param sample: Zenoh sample containing token payload.
        """

        token = Token.unpack(sample.payload.to_bytes())
        if self._token_type is not None and token.status != self._token_type:
            return

        with self._buffer_lock:
            self._buffer.append(token)

    def _deserialize_payload(self, token: Token, message_cls: type[T] | None) -> T | dict | None:
        """
        Deserialize token payload as specific message type or generic JSON dict.

        :param token: Token containing payload to deserialize.
        :param message_cls: Message class to deserialize as (None for generic JSON).
        :return: Deserialized payload.
        """

        if token.payload is None:
            return None
        elif message_cls is None:
            return Message.extract_data_as_json(token.payload)
        else:
            return message_cls.unpack(token.payload)
