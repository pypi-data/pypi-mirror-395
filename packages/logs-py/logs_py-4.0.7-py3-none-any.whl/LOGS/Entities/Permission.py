from typing import Optional

from LOGS.Entity.SerializableContent import SerializableClass


class Permission(SerializableClass):
    name: Optional[str] = None
    shortDescription: Optional[str] = None
    longDescription: Optional[str] = None
