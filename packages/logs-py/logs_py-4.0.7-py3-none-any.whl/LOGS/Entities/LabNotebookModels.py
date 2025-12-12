from enum import Enum


class LabNotebookStatus(Enum):
    CLOSED = "CLOSED"
    ACTIVE = "ACTIVE"


class LabNotebookExperimentStatus(Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
