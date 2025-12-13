import traceback
from collections.abc import Callable
from threading import Event, Thread

from antioch.module.clock import Clock
from antioch.module.execution import Execution
from antioch.module.input import NodeInputBuffer
from antioch.module.token import Token, TokenType
from common.ark.ark import Environment
from common.ark.module import Module
from common.ark.node import Node as NodeConfig
from common.ark.scheduler import InputToken, NodeEdge, NodeStartEvent, OnlineScheduler
from common.ark.sim import SimNodeComplete, SimNodeStart
from common.utils.comms import CommsPublisher, CommsSession
from common.utils.logger import Logger
from common.utils.time import now_us

TOKEN_OUTPUT_PATH = "_token/{path}"
NODE_START_SUBSCRIBER_PATH = "_ark/node_start/{module}/{node}"
NODE_COMPLETE_PUBLISHER_PATH = "_ark/node_complete/{module}/{node}"


class Node:
    """
    Independent node execution thread.

    Each node runs in its own thread, walks the deterministic schedule independently,
    and executes user callbacks at the appropriate logical times.
    """

    def __init__(
        self,
        module_name: str,
        node_name: str,
        module_config: Module,
        node_config: NodeConfig,
        ark_edges: list[NodeEdge],
        ark_modules: list[Module],
        global_start_time_us: int,
        environment: Environment,
        debug: bool,
        callback: Callable[[Execution], None],
    ):
        """
        Initialize node and start thread immediately.

        :param module_name: Module containing this node.
        :param node_name: Name of this node.
        :param module_config: Module configuration from Ark.
        :param node_config: Node configuration.
        :param ark_edges: All edges in the Ark.
        :param ark_modules: All modules in the Ark.
        :param global_start_time_us: Global start time (only used in real mode).
        :param environment: Execution environment (SIM or REAL).
        :param debug: Enable debug mode for loggers.
        :param callback: User callback function to execute.
        """

        self._module_name = module_name
        self._node_name = node_name
        self._module_config = module_config
        self._node_config = node_config
        self._ark_edges = ark_edges
        self._ark_modules = ark_modules
        self._global_start_time_us = global_start_time_us
        self._environment = environment
        self._callback = callback

        self._comms = CommsSession()
        self._logger = Logger(self._comms, module_name, debug=debug, print_logs=True)
        self._execution_logger = Logger(self._comms, module_name, debug=debug, print_logs=True)
        self._shutdown_requested = Event()

        # Create input buffers for all inputs
        self._input_buffers: dict[str, NodeInputBuffer] = {}
        for input_name, input_config in node_config.inputs.items():
            self._input_buffers[input_name] = NodeInputBuffer(input_name, input_config, self._comms)

        # Create output publishers for all outputs
        self._output_publishers: dict[str, CommsPublisher] = {}
        for output_name, output_config in node_config.outputs.items():
            path = TOKEN_OUTPUT_PATH.format(path=output_config.path)
            self._output_publishers[output_name] = self._comms.declare_publisher(path)

        # Create reusable execution context
        self._execution = Execution(
            name=node_config.name,
            budget_us=node_config.budget_us,
            parameters=module_config.parameters,
            outputs=node_config.outputs,
            logger=self._execution_logger,
        )

        # Start thread immediately
        thread_target = self._run_sim if self._environment == Environment.SIM else self._run_real
        self._thread = Thread(target=thread_target, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the node and clean up resources.

        Sets the shutdown event, causing the node's execution loop to exit,
        and cleans up all communication resources.
        """

        self._logger.info("Stopping node")
        self._shutdown_requested.set()

        # Close all input buffers
        for input_buffer in self._input_buffers.values():
            input_buffer.close()

        # Close all output publishers
        for publisher in self._output_publishers.values():
            publisher.close()

        # Close comms session
        self._comms.close()

    def join(self, timeout: float | None = None) -> None:
        """
        Wait for node thread to finish.

        :param timeout: Maximum time to wait in seconds (None for infinite).
        """

        self._thread.join(timeout=timeout)

    def _run_sim(self) -> None:
        """
        Sim mode execution loop.

        Waits for SimNodeStart messages via async subscriber with timeout checking
        for shutdown events.
        """

        start_path = NODE_START_SUBSCRIBER_PATH.format(module=self._module_name, node=self._node_name)
        complete_path = NODE_COMPLETE_PUBLISHER_PATH.format(module=self._module_name, node=self._node_name)
        start_subscriber = self._comms.declare_async_subscriber(start_path)
        complete_publisher = self._comms.declare_publisher(complete_path)

        while not self._shutdown_requested.is_set():
            # Wait for node start event with shutdown check
            start = start_subscriber.recv_timeout(SimNodeStart, timeout=0.1)
            if start is None:
                continue

            # Update logger times
            self._logger.set_let(start.start_let_us)
            self._execution.logger.set_let(start.start_let_us)

            # Gather and filter input tokens
            input_data = self._gather_inputs(start.start_let_us, start.input_tokens)
            if input_data is None:
                self._logger.warning(f"Skipping node {self._node_name} at {start.start_let_us} because of missing inputs")
                self._publish_skipped_tokens(start.start_let_us, start.start_timestamp_us)
                continue

            # Start execution with runtime data
            self._execution.start(
                let_us=start.start_let_us,
                input_data=input_data,
                hardware_reads=start.hardware_reads,
            )

            # Execute user callback
            try:
                self._callback(self._execution)
            except Exception as e:
                self._publish_error_tokens(start.start_let_us, str(e), self._execution._start_timestamp_us)
                self._logger.error(f"Execution failed: {e}\n{traceback.format_exc()}")
                continue

            # Check for budget overrun
            if self._execution.elapsed_us > self._node_config.budget_us:
                self._logger.error(f"Overrun: {self._execution.elapsed_us}us > {self._node_config.budget_us}us at {start.start_let_us}us")
                continue

            # Publish output tokens
            for output_name, publisher in self._output_publishers.items():
                payload = self._execution._output_data.get(output_name)
                publisher.publish(
                    Token(
                        module_name=self._module_name,
                        node_name=self._node_name,
                        output_name=output_name,
                        let_us=start.start_let_us,
                        start_timestamp_us=self._execution._start_timestamp_us,
                        budget_us=self._node_config.budget_us,
                        status=TokenType.DATA if payload is not None else TokenType.SHORT_CIRCUIT,
                        payload=payload,
                    )
                )

            # Publish completion (only if no overrun or error)
            complete_publisher.publish(
                SimNodeComplete(
                    module_name=self._module_name,
                    node_name=self._node_name,
                    completion_let_us=start.start_let_us + self._node_config.budget_us,
                    hardware_writes=self._execution._hardware_writes if self._execution._hardware_writes else None,
                )
            )

    def _run_real(self) -> None:
        """
        Real mode execution loop.

        Sleeps until event times using clock-based synchronization.
        Creates scheduler locally since it's only needed in real mode.
        """

        scheduler = OnlineScheduler(self._ark_edges, self._ark_modules)
        clock = Clock(self._global_start_time_us, event=self._shutdown_requested)

        while not self._shutdown_requested.is_set():
            # Skip to next event for this node
            event = scheduler.next()
            if (
                not isinstance(event, NodeStartEvent)
                or (event.module, event.node) != (self._module_name, self._node_name)
                or clock.let_us > event.start_let_us
            ):
                continue

            # Sleep until event time with shutdown check
            if not clock.wait_until(event.start_let_us):
                break

            # Update logger times
            self._logger.set_let(event.start_let_us)
            self._execution_logger.set_let(event.start_let_us)

            # Gather and filter input tokens
            input_data = self._gather_inputs(event.start_let_us, event.input_tokens)
            if input_data is None:
                self._logger.warning(f"Skipping node {self._node_name} at {event.start_let_us} because of missing inputs")
                self._publish_skipped_tokens(event.start_let_us, now_us())
                continue

            # Start execution with runtime data (no hardware reads in real mode)
            self._execution.start(
                let_us=event.start_let_us,
                input_data=input_data,
                hardware_reads={},
            )

            # Execute user callback
            try:
                self._callback(self._execution)
            except Exception as e:
                self._publish_error_tokens(event.start_let_us, str(e), self._execution._start_timestamp_us)
                self._logger.error(f"Execution failed: {e}\n{traceback.format_exc()}")
                continue

            # Check for budget overrun
            if self._execution.elapsed_us > self._node_config.budget_us:
                self._logger.error(f"Overrun: {self._execution.elapsed_us}us > {self._node_config.budget_us}us at {event.start_let_us}us")
                continue

            # Publish output tokens
            for output_name, publisher in self._output_publishers.items():
                payload = self._execution._output_data.get(output_name)
                publisher.publish(
                    Token(
                        module_name=self._module_name,
                        node_name=self._node_name,
                        output_name=output_name,
                        let_us=event.start_let_us,
                        start_timestamp_us=self._execution._start_timestamp_us,
                        budget_us=self._node_config.budget_us,
                        status=TokenType.DATA if payload is not None else TokenType.SHORT_CIRCUIT,
                        payload=payload,
                    )
                )

    def _gather_inputs(self, let_us: int, expected_tokens: list[InputToken]) -> dict[str, list[Token]] | None:
        """
        Gather input tokens and apply buffer policies.

        Detects missing tokens (overruns) and adds them to buffers before execution.

        :param let_us: Current logical execution time.
        :param expected_tokens: List of InputToken objects expected for this execution.
        :return: Dictionary of filtered tokens by input name, or None if required input missing.
        """

        # Add missing tokens as overruns to buffers
        for tok in expected_tokens:
            input_buffer = self._input_buffers[tok.target_input_name]
            if input_buffer.get_token(tok.let_us, tok.source_module, tok.source_node) is None:
                input_buffer.add_token(
                    Token(
                        module_name=tok.source_module,
                        node_name=tok.source_node,
                        output_name=tok.source_output_name,
                        let_us=tok.let_us,
                        budget_us=tok.budget_us,
                        start_timestamp_us=tok.let_us,
                        status=TokenType.OVERRUN,
                    )
                )

        # Prepare execution by applying buffer policies
        input_data = {}
        for input_name, input_buffer in self._input_buffers.items():
            filtered_tokens = input_buffer.prepare_execution(let_us)
            if filtered_tokens is None:
                return None
            input_data[input_name] = filtered_tokens

        return input_data

    def _publish_skipped_tokens(self, let_us: int, start_timestamp_us: int) -> None:
        """
        Publish skipped tokens for all outputs.

        :param let_us: Logical execution time.
        :param start_timestamp_us: Start timestamp for token.
        """

        for output_name, publisher in self._output_publishers.items():
            publisher.publish(
                Token(
                    module_name=self._module_name,
                    node_name=self._node_name,
                    output_name=output_name,
                    let_us=let_us,
                    start_timestamp_us=start_timestamp_us,
                    budget_us=self._node_config.budget_us,
                    status=TokenType.SKIPPED,
                )
            )

    def _publish_error_tokens(self, let_us: int, error: str, start_timestamp_us: int) -> None:
        """
        Publish error tokens for all outputs.

        :param let_us: Logical execution time.
        :param error: Error message.
        :param start_timestamp_us: Start timestamp for token.
        """

        for output_name, publisher in self._output_publishers.items():
            publisher.publish(
                Token(
                    module_name=self._module_name,
                    node_name=self._node_name,
                    output_name=output_name,
                    let_us=let_us,
                    start_timestamp_us=start_timestamp_us,
                    budget_us=self._node_config.budget_us,
                    status=TokenType.ERROR,
                    error=error,
                )
            )
