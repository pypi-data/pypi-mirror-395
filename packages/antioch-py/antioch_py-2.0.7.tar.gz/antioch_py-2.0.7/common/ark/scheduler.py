from abc import ABC, abstractmethod

from sortedcontainers import SortedDict

from common.ark.module import Module
from common.message import Message


class NodeEdge(Message):
    """
    Directed edge representing data flow between nodes.
    """

    _type = "antioch/ark/node_edge"
    source_module: str
    source_node: str
    source_output_name: str
    target_module: str
    target_node: str
    target_input_name: str
    type: str


class InputToken(Message):
    """
    Input token representing data flow to a node.
    """

    _type = "antioch/ark/input_token"
    source_module: str
    source_node: str
    source_output_name: str
    target_input_name: str
    let_us: int
    budget_us: int


class ScheduleEvent(Message, ABC):
    """
    Base class for schedule events.

    Events represent discrete occurrences in the execution schedule,
    ordered by logical execution time (LET).
    """

    module: str
    node: str

    @property
    @abstractmethod
    def let_us(self) -> int:
        """
        Logical execution time in microseconds.
        """

    @property
    @abstractmethod
    def priority(self) -> int:
        """
        Event priority for ordering (0=complete, 1=start).
        """


class NodeCompleteEvent(ScheduleEvent):
    """
    Node execution completes.
    """

    _type = "antioch/ark/node_complete_event"
    completion_let_us: int

    @property
    def let_us(self) -> int:
        return self.completion_let_us

    @property
    def priority(self) -> int:
        return 0


class NodeStartEvent(ScheduleEvent):
    """
    Node execution starts.
    """

    _type = "antioch/ark/node_start_event"
    start_let_us: int
    input_tokens: list[InputToken]

    @property
    def let_us(self) -> int:
        return self.start_let_us

    @property
    def priority(self) -> int:
        return 1


class NodeState:
    """
    Runtime state of a node during scheduling.

    Tracks execution status and pending inputs for a single node.
    """

    def __init__(self, module: str, node: str, required_inputs: set[str]):
        """
        Create a new node state.

        :param module: Module containing the node.
        :param node: Name of the node.
        :param required_inputs: Set of input names that are required for execution.
        """

        self.module = module
        self.node = node
        self.is_executing = False
        self.queued_execution: int | None = None
        self.pending_tokens: dict[str, list[InputToken]] = {}
        self.required_inputs = required_inputs

    def record_token(self, token: InputToken) -> None:
        """
        Buffer a token for this input.

        :param token: Input token to buffer.
        """

        if token.target_input_name not in self.pending_tokens:
            self.pending_tokens[token.target_input_name] = []
        self.pending_tokens[token.target_input_name].append(token)

    def has_all_required_inputs(self) -> bool:
        """
        Check if all required inputs have at least one token.

        :return: True if all required inputs have tokens, False otherwise.
        """

        return all(self.pending_tokens.get(inp, []) for inp in self.required_inputs)

    def collect_tokens(self) -> list[InputToken]:
        """
        Collect all buffered tokens, ordered by let_us.

        :return: List of all tokens sorted by start time.
        """

        all_tokens: list[InputToken] = []
        for tokens in self.pending_tokens.values():
            all_tokens.extend(tokens)
        self.pending_tokens.clear()
        all_tokens.sort(key=lambda t: t.let_us)
        return all_tokens


class OnlineScheduler:
    """
    Online deterministic scheduler for Ark execution.

    Computes execution schedule deterministically from edges and modules using
    Logical Execution Time (LET) semantics. Events are computed lazily on-demand,
    enabling infinite schedules driven by timer nodes. Nodes execute in parallel
    with only per-node sequential constraints.

    The scheduler implements:
    - Timer-driven execution with periodic node firing
    - Token-based data flow between nodes
    - Queued execution for timer overruns
    - Deterministic event ordering (completions before starts at same LET)
    """

    def __init__(self, edges: list[NodeEdge], modules: list[Module]):
        """
        Create a new online scheduler.

        Initializes the scheduler and seeds initial timer fires.
        Events are computed lazily on-demand via next().

        :param edges: List of node edges.
        :param modules: List of modules.
        :raises ValueError: If a module or node is not found.
        :raises RuntimeError: If the schedule is exhausted.
        """

        # Build outgoing edge map for O(1) lookups
        self.modules: dict[str, Module] = {m.name: m for m in modules}
        self.outgoing_edges: dict[tuple[str, str], list[NodeEdge]] = {}
        for edge in edges:
            key = (edge.source_module, edge.source_node)
            if key not in self.outgoing_edges:
                self.outgoing_edges[key] = []
            self.outgoing_edges[key].append(edge)

        # Compute timer periods once
        self.timer_periods_us: dict[tuple[str, str], int] = {}
        for module in self.modules.values():
            for node_name, node_def in module.nodes.items():
                if node_def.timer:
                    key = (module.name, node_name)
                    self.timer_periods_us[key] = node_def.timer.to_period_us()

        # Initialize state
        self.node_states: dict[tuple[str, str], NodeState] = {}
        self.events: SortedDict = SortedDict()
        self.processed_events: SortedDict = SortedDict()
        self.last_event_let_us: int = 0
        self.last_event_index: int = -1
        for module in self.modules.values():
            for node_name, node_def in module.nodes.items():
                key = (module.name, node_name)
                required_inputs = {name for name, inp in node_def.inputs.items() if inp.required}
                self.node_states[key] = NodeState(module.name, node_name, required_inputs)

        # Seed timer fires
        for module_name, node_name in self.timer_periods_us:
            self._try_schedule_node_start(module_name, node_name, 0)

    def next(self) -> ScheduleEvent:
        """
        Get the next event in the schedule.

        Returns the next event in chronological order, processing multiple events
        at the same LET in priority order. Computes schedule lazily as needed.

        :return: The next event in the schedule.
        :raises RuntimeError: If the schedule is exhausted.
        """

        while True:
            # Check if we have more events at current LET
            if self.last_event_let_us in self.processed_events:
                events = self.processed_events[self.last_event_let_us]
                next_index = 0 if self.last_event_index == -1 else self.last_event_index + 1
                if next_index < len(events):
                    self.last_event_index = next_index
                    return events[next_index]

            # Move to next LET with events
            range_start = self.last_event_let_us if self.last_event_index == -1 else self.last_event_let_us + 1

            # Find next processed LET
            for let_us in self.processed_events.irange(minimum=range_start):
                if self.processed_events[let_us]:
                    self.last_event_let_us = let_us
                    self.last_event_index = 0
                    return self.processed_events[let_us][0]

            # No more processed events, need to process next unprocessed LET
            if not self.events:
                raise RuntimeError("Schedule exhausted")

            next_let_us = next(iter(self.events.keys()))
            events = self._process_let(next_let_us)
            self.processed_events[next_let_us] = events

    def _process_let(self, let_us: int) -> list[ScheduleEvent]:
        """
        Process all events at a specific LET and return them.

        Retrieves all events scheduled for this LET, sorts them by priority
        (completions before starts), and processes each one. May generate
        additional events at the same LET through cascading effects.

        :param let_us: Logical execution time to process.
        :return: List of all events processed at this LET.
        """

        all_events: list[ScheduleEvent] = []
        while let_us in self.events:
            events: list[ScheduleEvent] = self.events.pop(let_us, [])  # type: ignore[assignment]
            if not events:
                break

            # Sort: completions before starts
            events.sort(key=lambda e: (e.let_us, e.priority))
            all_events.extend(events)
            for event in events:
                if isinstance(event, NodeCompleteEvent):
                    self._handle_node_complete(event)
                elif isinstance(event, NodeStartEvent):
                    self._handle_node_start(event)

        return all_events

    def _handle_node_complete(self, event: NodeCompleteEvent) -> None:
        """
        Handle node completion event.

        Marks node as idle, processes queued executions, and creates InputTokens
        for all downstream nodes connected via edges.

        :param event: Node complete event to process.
        """

        # Mark node as idle and process queued execution
        key = (event.module, event.node)
        if key in self.node_states:
            state = self.node_states[key]
            state.is_executing = False
            if state.queued_execution is not None:
                queued_let = state.queued_execution
                state.queued_execution = None
                if state.has_all_required_inputs():
                    input_tokens = state.collect_tokens()
                    self._schedule_event(
                        NodeStartEvent(
                            module=event.module,
                            node=event.node,
                            start_let_us=queued_let,
                            input_tokens=input_tokens,
                        )
                    )

        # Create InputTokens and buffer them in target nodes
        if key in self.outgoing_edges:
            source_node_def = self._get_node(event.module, event.node)
            budget_us = source_node_def.budget_us
            for edge in self.outgoing_edges[key]:
                token = InputToken(
                    source_module=edge.source_module,
                    source_node=edge.source_node,
                    source_output_name=edge.source_output_name,
                    target_input_name=edge.target_input_name,
                    let_us=event.completion_let_us - budget_us,
                    budget_us=budget_us,
                )

                target_key = (edge.target_module, edge.target_node)
                if target_key in self.node_states:
                    target_state = self.node_states[target_key]
                    target_state.record_token(token)

                    # Only schedule nodes without timers when inputs arrive
                    # Timer nodes are scheduled by their timer, inputs are just buffered
                    if target_key not in self.timer_periods_us and target_state.has_all_required_inputs() and not target_state.is_executing:
                        self._try_schedule_node_start(edge.target_module, edge.target_node, event.completion_let_us)

    def _handle_node_start(self, event: NodeStartEvent) -> None:
        """
        Handle node start event.

        For nodes with all required inputs: marks as executing and schedules completion.
        For timer nodes without required inputs: skips execution but schedules next timer fire.

        :param event: Node start event to process.
        """

        key = (event.module, event.node)
        node_def = self._get_node(event.module, event.node)

        # Get current input tokens from node state (not from event)
        state = self.node_states.get(key)
        current_input_tokens: list[InputToken] = (
            [token for tokens_list in state.pending_tokens.values() for token in tokens_list] if state else []
        )

        # Check if required inputs are satisfied
        required_inputs = {name for name, inp in node_def.inputs.items() if inp.required}
        provided_inputs = {token.target_input_name for token in current_input_tokens}

        # Only execute if required inputs are satisfied
        if state and all(req in provided_inputs for req in required_inputs):
            state.is_executing = True
            state.collect_tokens()  # Clear tokens now that we're executing

            # Schedule completion
            self._schedule_event(
                NodeCompleteEvent(
                    module=event.module,
                    node=event.node,
                    completion_let_us=event.start_let_us + node_def.budget_us,
                )
            )

        # For timer nodes, always schedule next timer fire (regardless of whether we executed)
        if key in self.timer_periods_us:
            period_us = self.timer_periods_us[key]
            next_start_let = event.start_let_us + period_us
            self._try_schedule_node_start(event.module, event.node, next_start_let)

    def _try_schedule_node_start(self, module: str, node: str, let_us: int) -> None:
        """
        Try to schedule a node start if ready and not executing.

        For timer nodes: always creates start events to maintain schedule.
        For non-timer nodes: only creates start events when all required inputs are available.

        :param module: Module containing the node.
        :param node: Name of the node to schedule.
        :param let_us: Logical execution time when node should start.
        """

        key = (module, node)
        state = self.node_states.get(key)
        if state is None:
            return

        # If node is currently executing, queue this execution
        if state.is_executing:
            state.queued_execution = let_us
            return

        # For timer nodes, always create start events to maintain schedule
        # For non-timer nodes, only create start events when inputs are ready
        if key in self.timer_periods_us or state.has_all_required_inputs():
            input_tokens = [token for tokens_list in state.pending_tokens.values() for token in tokens_list]
            self._schedule_event(NodeStartEvent(module=module, node=node, start_let_us=let_us, input_tokens=input_tokens))

    def _schedule_event(self, event: ScheduleEvent) -> None:
        """
        Schedule an event for future processing.

        Adds the event to the unprocessed events queue at its LET for
        later processing by the scheduler.

        :param event: Event to schedule (NodeStartEvent or NodeCompleteEvent).
        """

        let_us = event.let_us
        if let_us not in self.events:
            self.events[let_us] = []
        self.events[let_us].append(event)

    def _get_node(self, module: str, node: str):
        """
        Get node definition from modules.

        :param module: Module containing the node.
        :param node: Name of the node.
        :return: Node definition.
        :raises ValueError: If module or node is not found.
        """

        if module not in self.modules:
            raise ValueError(f"Module '{module}' not found")
        if node not in self.modules[module].nodes:
            raise ValueError(f"Node '{module}::{node}' not found")
        return self.modules[module].nodes[node]
