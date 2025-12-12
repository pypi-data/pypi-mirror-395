from enum import Enum
from typing import List, Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableClass


class DatasetSourceType(Enum):
    ManualUpload = 0
    SFTPAutoload = 1
    ClientAutoload = 2
    APIUpload = 3


class ParsedMetadata(SerializableClass):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


class DatasetSource(SerializableClass):
    id: Optional[int] = None
    type: Optional[DatasetSourceType] = None
    name: Optional[str] = None

    def __str__(self):
        return Tools.ObjectToString(self)


class ViewableEntityTypes(Enum):
    ELN = "ELN"
    CustomField = "CustomField"
