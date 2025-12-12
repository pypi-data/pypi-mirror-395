from typing import Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.Entity import Entity
from LOGS.LOGSConnection import LOGSConnection


class IEntityWithIntId(Entity):
    _id: int = 0

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        self._id = Tools.checkAndConvert(value, int, "id")
