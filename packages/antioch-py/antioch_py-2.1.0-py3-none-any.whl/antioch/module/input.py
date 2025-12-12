from threading import Lock

import zenoh
from sortedcontainers import SortedDict

from antioch.module.token import Token, TokenType
from common.ark.node import NodeInput
from common.utils.comms import CommsSession

TOKEN_INPUT_PATH = "_token/{path}"


class NodeInputBuffer:
    """
    Thread-safe input buffer with policy-based token retention.

    Manages tokens for a single node input with automatic arrival validation
    and buffer policy enforcement (last_n, max_age_ms, always_run, required, consume_inputs).
    """

    def __init__(self, input_name: str, config: NodeInput, comms: CommsSession):
        """
        Create a new node input buffer.

        :param input_name: Name of the input.
        :param config: Input configuration with buffer policies.
        :param comms: Communication session for subscribing to tokens.
        """

        self._input_name = input_name
        self._config = config
        self._lock = Lock()
        self._tokens: SortedDict[tuple[int, str, str], Token] = SortedDict()

        # Subscribe to token path with callback
        path = TOKEN_INPUT_PATH.format(path=config.path)
        self._subscriber = comms.declare_callback_subscriber(path, self._on_token)

    def close(self) -> None:
        """
        Close the input buffer and clean up resources.
        """

        self._subscriber.undeclare()

    def add_token(self, token: Token) -> None:
        """
        Add token to buffer.

        :param token: Token to add.
        """

        with self._lock:
            key = (token.let_us, token.module_name, token.node_name)
            self._tokens[key] = token

    def get_token(self, let_us: int, source_module: str, source_node: str) -> Token | None:
        """
        Get specific token or None if not arrived.

        :param let_us: Logical execution time of the token.
        :param source_module: Source module name.
        :param source_node: Source node name.
        :return: Token if found, None otherwise.
        """

        with self._lock:
            key = (let_us, source_module, source_node)
            return self._tokens.get(key)

    def prepare_execution(self, let_us: int) -> list[Token] | None:
        """
        Prepare tokens for execution by collecting and applying buffer policies.

        :param let_us: Current logical execution time.
        :return: Filtered tokens ready for execution, or None if required input missing.
        """

        with self._lock:
            # Collect tokens with let_us <= current execution time
            tokens = [t for t in self._tokens.values() if t.let_us <= let_us]

            # Filter to data tokens only (unless always_run allows errors/overruns)
            if not self._config.always_run:
                tokens = [t for t in tokens if t.status == TokenType.DATA]

            # Check required input constraint
            if self._config.required and len(tokens) == 0:
                return None

            # Keep only last N tokens
            if len(tokens) > self._config.last_n:
                tokens = tokens[-self._config.last_n :]

            # Filter out stale tokens based on max age
            if self._config.max_age_ms is not None:
                max_age_us = self._config.max_age_ms * 1000
                tokens = [t for t in tokens if let_us - t.let_us <= max_age_us]

            # Add filtered tokens back to buffer if not consuming
            if not self._config.consume_inputs:
                for t in tokens:
                    key = (t.let_us, t.module_name, t.node_name)
                    self._tokens[key] = t

            return tokens

    def _on_token(self, sample: zenoh.Sample) -> None:
        """
        Callback thread: receive and buffer token.

        :param sample: Zenoh sample containing token.
        """

        token = Token.unpack(sample.payload.to_bytes())
        if token.elapsed() > token.budget_us:
            token = Token(
                module_name=token.module_name,
                node_name=token.node_name,
                output_name=token.output_name,
                let_us=token.let_us,
                start_timestamp_us=token.start_timestamp_us,
                budget_us=token.budget_us,
                status=TokenType.OVERRUN,
            )

        self.add_token(token)
