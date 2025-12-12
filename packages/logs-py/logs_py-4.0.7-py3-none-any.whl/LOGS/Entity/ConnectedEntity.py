import inspect
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast

from LOGS.Auxiliary.Exceptions import EntityNotConnectedException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.LOGSConnection import LOGSConnection

_T = TypeVar("_T")


class ConnectedEntity(SerializableContent):
    _connection: Optional[LOGSConnection] = None
    _endpoint: Optional[List[str]] = None
    _uiEndpoint: Optional[List[str]] = None
    _noSerialize = ["connection", "cachePath", "cacheId", "cacheDir"]
    _cacheDir: Optional[str] = None
    _cacheId: str = cast(str, None)

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._connection = connection

        if not self._uiEndpoint and self._endpoint and len(self._endpoint) == 1:
            self._uiEndpoint = ["#" + self._endpoint[0]]

        super().__init__(ref=ref)

    def _getConnection(self):
        if not self._connection:
            raise EntityNotConnectedException(self)
        return self._connection

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != ConnectedEntity.__name__
                    else "unknown"
                )
            )

        return self._getConnection(), self._endpoint

    def _setConnection(self, value):
        self._connection = Tools.checkAndConvert(
            value, LOGSConnection, "connection", allowNone=True
        )
        for k in self.__dict__:
            a = getattr(self, k)
            if issubclass(type(a), ConnectedEntity):
                cast(ConnectedEntity, a)._setConnection(self._connection)

    def clearCache(self):
        raise NotImplementedError(
            "Clearing cache of %a class is not implemented." % type(self).__name__
        )

    @classmethod
    def checkAndConvertWithConnection(
        cls,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
        connection: Optional[LOGSConnection] = None,
    ) -> _T:
        if (
            inspect.isclass(fieldType)
            and issubclass(fieldType, ConnectedEntity)
            and isinstance(value, dict)
        ):
            return cast(Any, fieldType)(ref=value, connection=connection)

        return Tools.checkAndConvert(value, fieldType, fieldName, converter, allowNone)

    @classmethod
    def checkListAndConvertWithConnection(
        cls,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        connection: Optional[LOGSConnection] = None,
    ) -> List[_T]:
        if isinstance(value, (list, tuple)):
            value = [
                cls.checkAndConvertWithConnection(
                    v, fieldType, fieldName, converter, allowNone, connection
                )
                for v in value
            ]

        return Tools.checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=allowNone,
        )

    def checkAndConvert(
        self,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
    ) -> _T:
        if (
            inspect.isclass(fieldType)
            and issubclass(fieldType, ConnectedEntity)
            and isinstance(value, dict)
        ):
            return cast(Any, fieldType)(ref=value, connection=self._connection)

        return super().checkAndConvert(
            value, fieldType, fieldName, converter, allowNone
        )

    def checkListAndConvert(
        self,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ) -> List[_T]:
        if isinstance(value, (list, tuple)):
            value = [
                self.checkAndConvert(v, fieldType, fieldName, converter, allowNone)
                for v in value
            ]

        return super().checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=allowNone,
            singleToList=singleToList,
            length=length,
        )

    @property
    def identifier(self):
        return "%s" % (type(self).__name__)

    @property
    def cacheDir(self) -> Optional[str]:
        return self._cacheDir

    @cacheDir.setter
    def cacheDir(self, value):
        self._cacheDir = Tools.checkAndConvert(value, str, "cacheDir", allowNone=True)

    @property
    def cacheId(self) -> str:
        if self._cacheId is None:
            if not hasattr(self, "id"):
                setattr(self, "id", Tools.generateRandomString())

            return f"{type(self).__name__}_{str(getattr(self, 'id'))}"
        else:
            return self._cacheId
