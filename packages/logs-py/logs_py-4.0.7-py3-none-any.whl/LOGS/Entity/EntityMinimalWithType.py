from typing import Optional

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.EntityMinimal import EntityMinimal
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.LOGSConnection import LOGSConnection


class EntityMinimalWithType(EntityMinimal):
    _id: int
    _type: str
    _defaultRequestParameter: dict = EntityRequestParameter().toDict()

    def __init__(
        self,
        ref=None,
        id: Optional[Constants.ID_TYPE] = None,
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
        type: str = "",
    ):
        """Represents a connected LOGS entity type"""

        self._type = type
        super().__init__(ref=ref, id=id, name=name, connection=connection)

    def __str__(self):
        n = " name:'%s'" % (self.name if self.name else "")
        t = " type:'%s'" % (self.type if self.type else "")
        return "<%s id:%s%s%s>" % (type(self).__name__, str(self.id), n, t)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        self._id = Tools.checkAndConvert(value, int, "id")

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value):
        self._type = Tools.checkAndConvert(value, str, "type")
