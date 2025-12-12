"""Enum with common status for CompilerTasks SimulatorTasks."""

from enum import Enum


class TaskStatus(str, Enum):
    """Contains allowed statuses for Task objects.

    Args:
        Enum (enum): Class inherits from Enum
    """

    PENDING = "pending"
    PREPARING = "preparing"
    EXECUTING = "executing"
    POSTPROCESSING = "postprocessing"
    FINISHED = "finished"
    ERROR = "error"
    ABORTED = "aborted"
