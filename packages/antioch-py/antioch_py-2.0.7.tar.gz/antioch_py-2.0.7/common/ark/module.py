from enum import Enum

from common.ark.node import Node
from common.message import Message


class ModuleKind(str, Enum):
    """
    Defines the type of module in the system.

    Modules can be either software primitives that run in containers
    or hardware abstractions that interface with physical/simulated arks.
    """

    SOFTWARE = "software"
    HARDWARE = "hardware"

    def __str__(self) -> str:
        return self.value


class ModuleInfo(Message):
    """
    Information about a module.
    """

    name: str
    description: str | None = None


class ParamType(str, Enum):
    """
    Supported parameter types for module configuration.

    These types define what kinds of configuration values can be
    passed to modules at runtime.
    """

    BOOLEAN = "boolean"
    NUMBER = "number"
    TEXT = "text"
    NULL = "null"

    def __str__(self):
        return self.value


class ModuleParameter(Message):
    """
    Type-safe parameter for module configuration.

    Wraps parameter values with type information to ensure type safety
    when passing configuration to modules at runtime.
    """

    description: str | None = None
    type: ParamType
    value: bool | int | float | str | None


class ModuleImage(Message):
    """
    Image configuration for hardware module deployment.
    """

    sim: str | None = None
    real: str | None = None


class Module(Message):
    """
    Complete specification for a module in the middleware system.

    A module is a containerized primitive that contains one or more processing nodes.
    Each module has build configuration, metadata, runtime parameters, and defines
    the nodes it contains. Modules are the unit of deployment and execution in
    the middleware system.
    """

    name: str
    kind: ModuleKind
    image: str | ModuleImage
    info: ModuleInfo
    parameters: dict[str, ModuleParameter]
    nodes: dict[str, Node]
