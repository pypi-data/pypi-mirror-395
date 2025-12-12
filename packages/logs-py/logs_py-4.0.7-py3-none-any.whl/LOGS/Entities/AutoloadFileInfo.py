from datetime import datetime
from typing import Optional

from LOGS.Entity.SerializableContent import SerializableClass


class AutoloadFileInfo(SerializableClass):
    name: Optional[str] = None
    fullPath: Optional[str] = None
    size: Optional[int] = None
    modTime: Optional[datetime] = None
    isDir: Optional[bool] = None
