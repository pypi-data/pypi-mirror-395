import dataclasses
from typing import Any, Generic, List, Optional, Type, TypeVar, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.Entity import Entity
from LOGS.Entity.EntityConnector import EntityConnector
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IdIterator import EmptyIdIterator, IdIterator
from LOGS.LOGSConnection import RESPONSE_TYPES, LOGSConnection, ResponseTypes

# SELF = TypeVar("SELF", bound="EntityConnector")

_ENTITY = TypeVar("_ENTITY", bound=Entity)
_REQUEST = TypeVar("_REQUEST", bound=EntityRequestParameter)


class EntityIterator(Generic[_ENTITY, _REQUEST], EntityConnector[_ENTITY]):
    """Represents a connected LOGS entity iterator"""

    _firstUrl: Optional[str] = None
    _entityIterator: int
    _currentResults: Optional[RESPONSE_TYPES]
    _generatorType: Optional[Type[_ENTITY]] = None
    _parameterType: Optional[Type[_REQUEST]] = None

    _parameters: _REQUEST
    _responseType: ResponseTypes = ResponseTypes.JSON
    _includeUrl: bool = True
    _connection: Optional[LOGSConnection]
    _count: Optional[int]

    def __init__(
        self,
        connection: Optional[LOGSConnection],
        parameters: Optional[_REQUEST] = None,
    ):
        super().__init__(connection=connection)

        if not self._parameterType:
            raise NotImplementedError(
                "Entity connection cannot be initialized without the request 'parameterType' field in class %a"
                % type(self).__name__
            )

        if not isinstance(self._parameterType, type):
            raise NotImplementedError(
                "The field 'parameterType' must be a 'type' got %a in class %a"
                % (type(self._parameterType), type(self).__name__)
            )

        if parameters and not isinstance(parameters, self._parameterType):
            raise LOGSException(
                "Parameter for iterator %a must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self._parameterType.__name__,
                    type(parameters).__name__,
                )
            )

        self._parameters = Tools.checkAndConvert(
            parameters, self._parameterType, "parameters", initOnNone=True
        )

        self._entityIterator = 0
        self._currentResults = None
        self._count = None

    def __iter__(self):
        self._initEntityIterator()
        return self

    def __next__(self) -> _ENTITY:
        from LOGS.Auxiliary.CustomEntityClassGenerator import CustomEntityClassGenerator
        from LOGS.Entity.ConnectedEntity import ConnectedEntity
        from LOGS.Interfaces.ITypedEntity import ITypedEntity

        if not self._generatorType:
            raise NotImplementedError(
                "Iterator cannot generate items without a specified 'generatorType' field in class %a"
                % type(self).__name__
            )

        if issubclass(self._generatorType, ConnectedEntity):
            next = cast(Any, self._generatorType)(
                self._getNextEntity(), connection=self._connection
            )
        else:
            next = cast(Any, self._generatorType)(self._getNextEntity())

        if issubclass(self._generatorType, ITypedEntity):
            next = CustomEntityClassGenerator.convertFromUntyped(
                next, limitToEntityType=self._generatorType
            )

        return next

    def _getNextPage(self, result):
        if not self._connection:
            raise LOGSException("Connection of %a is not defined" % type(self).__name__)

        if "hasNext" not in result or not result["hasNext"]:
            return None, None

        url = result["url"]

        page = 1
        if "page" in result:
            page = int(result["page"])
        elif self._parameters.page:
            page = self._parameters.page
        self._parameters.page = page + 1
        return self._connection.postUrl(
            url=url,
            data=self._parameters.toDict(),
            responseType=self._responseType,
            includeUrl=self._includeUrl,
        )

        # ### code for using get ###
        # o = urlparse(result["url"])
        # params = parse_qs(o.query)
        # params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}

        # page = 1
        # if "page" in params:
        #     page = int(params["page"])
        # params["page"] = page + 1

        # urlList = list(o)
        # urlList[4] = None
        # url = cast(str, urlunparse(urlList))

        # return self._connection.getUrl(
        #     url,
        #     parameters=params,
        #     responseType=self._responseType,
        #     includeUrl=self._includeUrl,
        # )

    def _initEntityIterator(self):
        url = self.getBaseUrl()
        self._entityIterator = 0

        if not self._connection:
            raise LOGSException(
                "Entity connector %a is not connected" % type(self).__name__
            )

        # ### code for using get ###
        # self._currentResults, error = self._connection.getUrl(
        #     url=url,
        #     parameters=self._parameters.toDict(),
        #     responseType=self._responseType,
        #     includeUrl=self._includeUrl,
        # )
        tmp = False
        if hasattr(self._parameters, "includeCount"):
            tmp = self._parameters.includeCount
            self._parameters.includeCount = True

        self._currentResults, responseError = self._connection.postUrl(
            url=url + "/list",
            data=self._parameters.toDict(),
            responseType=self._responseType,
            includeUrl=self._includeUrl,
        )

        if hasattr(self._parameters, "includeCount"):
            self._parameters.includeCount = tmp

        if isinstance(self._currentResults, dict) and "count" in self._currentResults:
            self._count = int(self._currentResults["count"])

        if responseError:
            raise LOGSException(responseError=responseError)

    def _getNextEntity(self):
        if not isinstance(self._currentResults, dict):
            raise StopIteration

        results = self._currentResults["results"]
        if self._entityIterator < len(results):
            result = results[self._entityIterator]
            self._entityIterator += 1
            return result

        self._currentResults, error = self._getNextPage(self._currentResults)
        if error:
            raise Exception("Connection error: %a", error)
        self._entityIterator = 0

        if (
            not self._currentResults
            or not isinstance(self._currentResults, dict)
            or len(self._currentResults["results"]) < 1
        ):
            raise StopIteration

        return self._getNextEntity()

    def split(self, size=20):
        connection, _ = self._getConnectionData()

        items = iter(self)
        ids = []
        for item in items:
            ids.append(item.id)
            if len(ids) >= size:
                param = dataclasses.replace(self._parameters)
                param.ids = ids
                iterator = type(self)(connection=connection)
                iterator._parameters = param
                yield iterator
                ids = []
        if ids:
            param = dataclasses.replace(self._parameters)
            param.ids = ids
            iterator = type(self)(connection=connection)
            iterator._parameters = param
            yield iterator

    def ids(self):
        if not self._generatorType:
            return EmptyIdIterator[Constants.ID_TYPE]()
        d = self._generatorType()
        iterator = IdIterator[type(d.id), _REQUEST](connection=self._connection)
        iterator._endpoint = self._endpoint
        iterator._parameters = self._parameters
        iterator._parameterType = self._parameterType
        iterator._generatorType = type(d.id)
        return iterator

    def first(self):
        i = iter(self)
        try:
            return cast(_ENTITY, next(i))
        except StopIteration:
            return None

    def toList(self, count: Optional[int] = None):
        if count:
            count = int(count)
            if count < 0:
                raise Exception("Invalid negative count %d" % count)
            result = cast(List[_ENTITY], [])
            num = 0
            for entity in self:
                result.append(entity)
                num += 1
                if num >= count:
                    break
            return result

        return list(self)

    @property
    def count(self) -> int:
        if self._count is None:
            self._initEntityIterator()
        return self._count if self._count else 0
