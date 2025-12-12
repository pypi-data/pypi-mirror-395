from datetime import datetime
from enum import Enum

from common.message import Message


class TaskOutcome(str, Enum):
    """
    Task outcome status.
    """

    SUCCESS = "success"
    FAILURE = "failure"


class TaskCompletion(Message):
    """
    Task completion message (does not include task ID, as that is the lookup key).
    """

    ark_name: str
    ark_version: str
    ark_hash: str
    task_start_time: datetime
    task_complete_time: datetime
    outcome: TaskOutcome
    result: dict | None = None


class TaskFileType(str, Enum):
    """
    Task file type.
    """

    MCAP = "mcap"
    BUNDLE = "bundle"
