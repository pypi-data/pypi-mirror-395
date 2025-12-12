from typing import Generic, List, Optional, TypeVar

from LOGS.Auxiliary.Exceptions import NotConnectedException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.Entity import Entity
from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.LOGSConnection import LOGSConnection, ResponseTypes

# SELF = TypeVar("SELF", bound="EntityConnector")

_T = TypeVar("_T", bound=Entity)


class EntityConnector(Generic[_T]):
    """Represents a connected LOGS entity iterator"""

    _endpoint: Optional[List[str]] = None
    _firstUrl: Optional[str] = None

    _parameters: SerializableContent
    _responseType: ResponseTypes = ResponseTypes.JSON
    _includeUrl: bool = True
    _connection: Optional[LOGSConnection] = None

    def __init__(self, connection: Optional[LOGSConnection]):
        self._connection = connection

    def _getConnection(self):
        if not self._connection:
            raise NotConnectedException(
                "%s iterator not connected." % type(self).__name__
            )
        return self._connection

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for %s iterator." % (type(self).__name__.lower())
            )

        return self._getConnection(), self._endpoint

    def __str__(self):
        s = ""
        if self._endpoint:
            s = "/" + "/".join(self._endpoint)
        return "<%s %a>" % (type(self).__name__, s)

    def getBaseUrl(self):
        return (
            self._firstUrl
            if self._firstUrl
            else (
                self._connection.getEndpointUrl(
                    endpoint=self._endpoint if self._endpoint else ""
                )
                if self._connection
                else ""
            )
        )

    @property
    def connection(self) -> Optional[LOGSConnection]:
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = Tools.checkAndConvert(
            value, LOGSConnection, "connection", allowNone=True
        )
