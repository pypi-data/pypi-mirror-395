from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.EntityMinimal import EntityMinimal
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entity.Entity import Entity

_FULL_ENTITY = TypeVar("_FULL_ENTITY", bound="Entity")


class EntityMinimalWithStrId(Generic[_FULL_ENTITY], EntityMinimal[str, _FULL_ENTITY]):
    _id: str

    def __init__(
        self,
        ref=None,
        id: Optional[str] = "",
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
    ):
        """Represents a connected LOGS entity type"""
        super().__init__(ref=ref, id=id, name=name, connection=connection)

    def __str__(self):
        s = " name:'%s'" % (self.name if self.name else "")
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value):
        self._id = Tools.checkAndConvert(value, str, "id")
