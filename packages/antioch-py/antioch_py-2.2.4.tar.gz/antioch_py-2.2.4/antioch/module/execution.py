import time
from typing import TypeVar, overload

from antioch.module.token import Token, TokenType
from common.ark.module import ModuleParameter
from common.ark.node import NodeOutput
from common.message import Image, ImuSample, JointStates, JointTargets, Message, PirStatus, RadarScan
from common.utils.logger import Logger
from common.utils.time import now_us

T = TypeVar("T", bound=Message)


class Execution:
    """
    Node execution context.

    Provides access to inputs, outputs, hardware, logger, and module parameters
    for user callbacks.
    """

    name: str
    let_us: int
    budget_us: int
    parameters: dict[str, ModuleParameter]
    logger: Logger

    def __init__(
        self,
        name: str,
        budget_us: int,
        parameters: dict[str, ModuleParameter],
        outputs: dict[str, NodeOutput],
        logger: Logger,
    ):
        """
        Initialize execution context with static configuration.

        :param name: Node name.
        :param budget_us: Node execution budget in microseconds.
        :param parameters: Module parameters.
        :param outputs: Node output configurations.
        :param logger: Logger for this execution context.
        """

        self.name = name
        self.budget_us = budget_us
        self.parameters = parameters
        self.logger = logger

        self._output_configs = outputs
        self._outputs = {name: Output(name, output_config, self) for name, output_config in outputs.items()}

        # Execution runtime state
        self.let_us = 0
        self._start_timestamp_us = 0
        self._start_time_us = 0
        self._inputs: dict[str, Input] = {}
        self._output_data: dict[str, bytes | None] = {}
        self._hardware_reads: dict[str, bytes] = {}
        self._hardware_writes: dict[str, bytes] = {}

    def start(
        self,
        let_us: int,
        input_data: dict[str, list[Token]] = {},
        hardware_reads: dict[str, bytes] = {},
    ) -> None:
        """
        Start a new execution with runtime data.

        :param let_us: Logical execution time.
        :param input_data: Input tokens keyed by input name.
        :param hardware_reads: Hardware read data keyed by hardware name.
        """

        self.let_us = let_us
        self._start_timestamp_us = now_us()
        self._start_time_us = time.monotonic_ns() // 1000
        self._inputs = {name: Input(tokens) for name, tokens in input_data.items()}
        self._output_data.clear()
        self._hardware_reads = hardware_reads
        self._hardware_writes.clear()

    @property
    def elapsed_us(self) -> int:
        """
        Get elapsed time in microseconds since execution start.

        :return: Elapsed time in microseconds.
        """

        return time.monotonic_ns() // 1000 - self._start_time_us

    @property
    def remaining_us(self) -> int:
        """
        Get remaining time in microseconds until execution budget is exhausted.

        :return: Remaining time in microseconds.
        """

        return max(0, self.budget_us - self.elapsed_us)

    def input(self, name: str) -> "Input":
        """
        Get input by name.

        :param name: Input name.
        :return: Input wrapper.
        :raises KeyError: If input not found.
        """

        if name not in self._inputs:
            raise KeyError(f"Input '{name}' not found")
        return self._inputs[name]

    def output(self, name: str) -> "Output":
        """
        Get output by name.

        :param name: Output name.
        :return: Output wrapper.
        :raises KeyError: If output not found.
        """

        if name not in self._outputs:
            raise KeyError(f"Output '{name}' not found")
        return self._outputs[name]

    def read_camera(self, name: str) -> Image | None:
        """
        Read camera image.

        :param name: Hardware name.
        :return: Camera image, or None if no data.
        """

        data = self._hardware_reads.get(name)
        return Image.unpack(data) if data else None

    def read_imu(self, name: str) -> ImuSample | None:
        """
        Read IMU sample.

        :param name: Hardware name.
        :return: IMU sensor measurements, or None if no data.
        """

        data = self._hardware_reads.get(name)
        return ImuSample.unpack(data) if data else None

    def read_radar(self, name: str) -> RadarScan | None:
        """
        Read radar scan.

        :param name: Hardware name.
        :return: Radar scan with detections, or None if no data.
        """

        data = self._hardware_reads.get(name)
        return RadarScan.unpack(data) if data else None

    def read_pir(self, name: str) -> PirStatus | None:
        """
        Read PIR sensor status.

        :param name: Hardware name.
        :return: PIR status with detection state and signal info, or None if no data.
        """

        data = self._hardware_reads.get(name)
        return PirStatus.unpack(data) if data else None

    def read_actuator_group(self, name: str) -> JointStates | None:
        """
        Read joint states from actuator group.

        :param name: Hardware name.
        :return: Joint states, or None if no data.
        """

        data = self._hardware_reads.get(name)
        return JointStates.unpack(data) if data else None

    def write_actuator_group(self, name: str, targets: JointTargets) -> None:
        """
        Write joint targets to actuator group.

        Queues joint targets for node completion.

        :param name: Hardware name.
        :param targets: Joint targets to apply.
        """

        self._hardware_writes[name] = targets.pack()


class Input:
    """
    Input wrapper for accessing tokens.
    """

    def __init__(self, tokens: list[Token]):
        """
        Initialize input.

        :param tokens: List of tokens for this input.
        """

        self._tokens = tokens

    @overload
    def data(self, message_cls: type[T], n: int = 1) -> T | None: ...

    @overload
    def data(self, message_cls: type[T], n: int) -> list[T]: ...

    def data(self, message_cls: type[T], n: int = 1) -> list[T] | T | None:
        """
        Get deserialized data from tokens.

        :param message_cls: Message type to deserialize.
        :param n: Number of tokens to return (1 for single, >1 for list).
        :return: Single message, list of messages, or None if no data.
        """

        data = []
        for token in reversed(self._tokens):
            if token.status == TokenType.DATA and token.payload:
                data.append(message_cls.unpack(token.payload))
                if len(data) >= n:
                    break
        return data if n > 1 else (data[0] if data else None)

    def tokens(self) -> list[Token]:
        """
        Get all tokens for this input.

        :return: List of tokens.
        """

        return self._tokens


class Output:
    """
    Output wrapper for setting data.
    """

    def __init__(self, name: str, output_config: NodeOutput, execution: Execution):
        """
        Initialize output.

        :param name: Output name.
        :param output_config: Output configuration from node.
        :param execution: Parent execution context.
        """

        self._name = name
        self._output_config = output_config
        self._execution = execution

    def set(self, message: Message) -> "Output":
        """
        Set output data.

        :param message: Message to serialize and set.
        :return: Self for chaining.
        :raises ValueError: If message type doesn't match expected output type.
        """

        # Validate message type matches expected output type
        if message.get_type() != self._output_config.type:
            raise ValueError(f"Output '{self._name}' expects type '{self._output_config.type}', got '{message.get_type()}'")

        self._execution._output_data[self._name] = message.pack()
        return self
