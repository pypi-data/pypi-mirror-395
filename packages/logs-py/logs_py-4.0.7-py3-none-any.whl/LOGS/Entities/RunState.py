from enum import Enum


class RunState(Enum):
    Running = "Running"
    Failed = "Failed"
    Finished = "Finished"
    Waiting = "Waiting"
    Aborted = "Aborted"
