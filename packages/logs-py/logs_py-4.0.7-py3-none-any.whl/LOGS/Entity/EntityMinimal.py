from typing import Generic, Optional, Type, TypeVar, cast
from uuid import UUID

from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.Entity import Entity
from LOGS.LOGSConnection import LOGSConnection

_FULL_ENTITY = TypeVar("_FULL_ENTITY", bound=Entity)
_ID_TYPE = TypeVar("_ID_TYPE", int, str)


class EntityMinimal(Generic[_ID_TYPE, _FULL_ENTITY], ConnectedEntity):
    _id: Optional[_ID_TYPE]
    _name: Optional[str]
    _fullEntityType: Optional[Type[_FULL_ENTITY]] = None
    _uid: Optional[UUID] = None
    _version: Optional[int] = None
    _isDeleted: Optional[bool] = None
    _isLocked: Optional[bool] = None
    _isSigned: Optional[bool] = None

    def __init__(
        self,
        ref=None,
        id: Optional[_ID_TYPE] = None,
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
    ):
        """Represents a connected LOGS entity type"""
        self._id = id
        self._name = name
        self._uid = None
        self._version = None

        if isinstance(ref, Entity):
            self._id = cast(_ID_TYPE, ref.id)
            if hasattr(ref, "name"):
                self._name = getattr(ref, "name")
            ref = None
        super().__init__(ref=ref, connection=connection)

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        return str(self)

    def __str__(self):
        s = " name:'%s'" % (self.name if self.name else "")
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)

    def _fetchEntity(self, connection: LOGSConnection):
        from LOGS.Interfaces.ITypedEntity import ITypedEntity

        if not self._endpoint:
            raise NotImplementedError(
                "Fetching of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != EntityMinimal.__name__
                    else "unknown"
                )
            )

        if not self._fullEntityType:
            raise LOGSException("Full entity type of %a not set." % type(self).__name__)

        entity = cast(Type[_FULL_ENTITY], self._fullEntityType)(
            id=self.id, connection=connection
        )
        entity.fetch()
        if isinstance(entity, ITypedEntity):
            entity = entity._getTypedInstance()

        return entity

    def fetchFullEntity(self):
        return self._fetchEntity(self._getConnection())

    @property
    def identifier(self):
        name = self.name
        return "%s(id:%s) %s" % (
            type(self).__name__,
            str(self.id),
            "'" + name + "'" if name else "",
        )

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvert(value, str, "name", allowNone=True)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def uid(self) -> Optional[UUID]:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = self.checkAndConvert(value, UUID, "uid", allowNone=True)

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvert(value, int, "uid", allowNone=True)

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = self.checkAndConvert(value, bool, "isDeleted", allowNone=True)

    @property
    def isLocked(self) -> Optional[bool]:
        return self._isLocked

    @isLocked.setter
    def isLocked(self, value):
        self._isLocked = self.checkAndConvert(value, bool, "isLocked", allowNone=True)

    @property
    def isSigned(self) -> Optional[bool]:
        return self._isSigned

    @isSigned.setter
    def isSigned(self, value):
        self._isSigned = self.checkAndConvert(value, bool, "isSigned", allowNone=True)
