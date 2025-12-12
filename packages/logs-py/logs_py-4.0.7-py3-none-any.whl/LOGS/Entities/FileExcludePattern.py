from typing import Optional

from LOGS.Entity.SerializableContent import SerializableClass


class FileExcludePattern(SerializableClass):
    name: Optional[str] = None
    regex: Optional[str] = None
