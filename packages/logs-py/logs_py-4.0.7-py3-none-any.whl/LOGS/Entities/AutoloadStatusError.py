from typing import Optional

from LOGS.Entity.SerializableContent import SerializableClass


class AutoloadStatusError(SerializableClass):
    message: Optional[str] = None
