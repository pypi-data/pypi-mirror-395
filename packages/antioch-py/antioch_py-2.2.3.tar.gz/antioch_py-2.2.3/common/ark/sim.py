from common.ark.scheduler import InputToken
from common.message import Message


class SimNodeStart(Message):
    """
    Ark signals node to start execution (sim mode).

    Sent from Ark to node via publisher to trigger node start with hardware reads.
    Includes expected input tokens for overrun detection and authoritative start timestamp.
    """

    _type = "antioch/ark/sim_node_start"
    module_name: str
    node_name: str
    start_let_us: int
    start_timestamp_us: int
    input_tokens: list[InputToken]
    hardware_reads: dict[str, bytes]


class SimNodeComplete(Message):
    """
    Node signals completion to Ark (sim mode).

    Sent from node to Ark to indicate completion with optional hardware writes.
    """

    _type = "antioch/ark/sim_node_complete"
    module_name: str
    node_name: str
    completion_let_us: int
    hardware_writes: dict[str, bytes] | None = None
