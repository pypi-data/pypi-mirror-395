import json
import os
import signal
import threading
from collections.abc import Callable

from antioch.module.execution import Execution
from antioch.module.node import Node
from common.ark.ark import Ark, Environment
from common.ark.module import ModuleParameter
from common.message import Message
from common.utils.comms import CommsSession
from common.utils.logger import Logger
from common.utils.time import now_us

AGENT_MODULE_READY_PATH = "_agent/module_ready"
AGENT_MODULE_START_PATH = "_agent/module_start"


class ModuleReady(Message):
    """
    Module ready message sent during handshake.
    """

    _type = "antioch/agent/module_ready"
    module_name: str


class ModuleStart(Message):
    """
    Module start message received during handshake.
    """

    _type = "antioch/agent/module_start"
    global_start_time_us: int


class Module:
    """
    Core module class for implementing Antioch modules in Python, which supports two
    mode of operation:

    > Container Mode (default): The module runs inside a Kubernetes pod managed by the
    Antioch agent. Configuration is automatically loaded from environment variables
    set by the agent (_MODULE_NAME, _ARK, _ENVIRONMENT, _DEBUG).

    > Local Mode: The module runs standalone for testing and development. Configuration
    must be explicitly provided via constructor parameters (module_name, ark, environment,
    debug).

    After creating a Module instance, you can access module metadata like module.ark,
    module.parameters, module.environment, and module.debug to initialize resources
    before registering node callbacks.

    Users register node callbacks via register() and then call spin() to start execution.
    The Ark will not start until spin() is called, which begins the handshake with the
    agent and starts processing node callbacks.

    Example:
        # Container mode
        module = Module()
        module.register("node1", callback1)
        module.register("node2", callback2)
        module.spin()

        # Local mode (for testing)
        module = Module(
            module_name="my_module",
            environment=Environment.SIM,
            ark=my_ark,
            debug=True,
        )
        module.register("node1", callback1)
        module.spin()
    """

    module_name: str
    ark: Ark
    environment: Environment
    debug: bool
    parameters: dict[str, "ModuleParameter"]

    def __init__(
        self,
        module_name: str | None = None,
        ark: Ark | None = None,
        environment: Environment = Environment.REAL,
        debug: bool = False,
    ):
        """
        Initialize module.

        :param module_name: Module name (for local mode).
        :param ark: Ark definition (for local mode).
        :param environment: Execution environment (for local mode).
        :param debug: Enable debug mode for loggers (for local mode).
        """

        # Parse module configuration
        self._is_local_mode = module_name is not None
        if not self._is_local_mode:
            module_name = os.environ.get("_MODULE_NAME")
            ark = Ark.model_validate(json.loads(os.environ["_ARK"])) if "_ARK" in os.environ else None
            environment = Environment(os.environ.get("_ENVIRONMENT", "real"))
            debug = os.environ.get("_DEBUG", "false").lower() == "true"

        # Validate required configuration
        if module_name is None:
            raise ValueError("Module is missing module name")
        if ark is None:
            raise ValueError("Module is missing ark configuration")

        # Extract module config from Ark
        module_config = next((m for m in ark.modules if m.name == module_name), None)
        if module_config is None:
            raise ValueError(f"Module '{module_name}' not found in Ark")

        self.module_name = module_name
        self.ark = ark
        self.environment = environment
        self.debug = debug
        self.parameters = module_config.parameters

        self._module_config = module_config
        self._shutdown_event = threading.Event()
        self._node_callbacks: dict[str, Callable[[Execution], None]] = {}
        self._nodes: dict[str, Node] = {}

    def register(self, name: str, callback: Callable[[Execution], None]) -> None:
        """
        Register a node callback.

        :param name: Node name.
        :param callback: User callback function invoked on each node execution.
        """

        self._node_callbacks[name] = callback

    def spin(self) -> None:
        """
        Initialize module and wait for shutdown signal.
        """

        comms = CommsSession()
        logger = Logger(comms, self.module_name, debug=self.debug, print_logs=True)
        global_start_time_us = now_us() if self._is_local_mode else self._perform_agent_handshake(comms)

        # Validate node callbacks
        for node_name in self._node_callbacks:
            if node_name not in self._module_config.nodes:
                raise ValueError(f"Node '{node_name}' not in module config")
        for node_name in self._module_config.nodes:
            if node_name not in self._node_callbacks:
                raise ValueError(f"Missing callback for node '{node_name}'")

        # Start node threads
        for name, callback in self._node_callbacks.items():
            self._nodes[name] = Node(
                module_name=self.module_name,
                node_name=name,
                module_config=self._module_config,
                node_config=self._module_config.nodes[name],
                ark_edges=self.ark.edges,
                ark_modules=self.ark.modules,
                global_start_time_us=global_start_time_us,
                environment=self.environment,
                debug=self.debug,
                callback=callback,
            )

        # Wait for shutdown signal
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)
        self._shutdown_event.wait()

        logger.info("Module exiting")
        comms.close()

    def join(self, timeout: float | None = None) -> None:
        """
        Wait for all node threads to finish.

        Blocks until all node threads have completed execution or until
        the timeout is reached. Useful for ensuring all nodes have finished
        processing before the module exits.

        :param timeout: Maximum time to wait per node in seconds (None for infinite).
        """

        for node in self._nodes.values():
            node.join(timeout=timeout)

    def _perform_agent_handshake(self, comms: CommsSession) -> int:
        """
        Perform handshake with agent to receive global start time.

        Publishes ready message and blocks waiting for start message containing
        the global start time for synchronization.

        :param comms: Comms session to use for communication.
        :return: Global start time in microseconds.
        """

        ready_publisher = comms.declare_publisher(AGENT_MODULE_READY_PATH)
        start_subscriber = comms.declare_subscriber(AGENT_MODULE_START_PATH)
        ready_publisher.publish(ModuleReady(module_name=self.module_name))
        start_msg = start_subscriber.recv(ModuleStart)
        return start_msg.global_start_time_us

    def _handle_shutdown(self, _signum, _frame) -> None:
        """
        Handle shutdown signal by stopping all node threads and
        exiting the module.
        """

        for node in self._nodes.values():
            node.stop()
        self._shutdown_event.set()
