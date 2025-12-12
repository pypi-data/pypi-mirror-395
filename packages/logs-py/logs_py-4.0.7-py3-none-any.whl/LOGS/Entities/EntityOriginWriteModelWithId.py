from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entities.OriginMinimal import OriginMinimal
from LOGS.Entity.SerializableContent import SerializableClass


@dataclass
class EntityOriginWriteModelWithId(SerializableClass):
    _noSerialize: List[str] = field(default_factory=lambda: ["asString"])
    id: Optional[Constants.ID_TYPE] = None
    uid: Optional[UUID] = None
    origin: Optional[OriginMinimal] = None
