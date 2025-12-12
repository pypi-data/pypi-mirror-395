from typing import Generic, List, Optional, Type, TypeVar, Union, cast

from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.Entity import Entity
from LOGS.Entity.EntityConnector import EntityConnector
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.LOGSConnection import RESPONSE_TYPES, LOGSConnection, ResponseTypes

# SELF = TypeVar("SELF", bound="EntityConnector")

_idType = TypeVar("_idType", bound=Union[int, str])
REQUEST = TypeVar("REQUEST", bound=EntityRequestParameter)


class EmptyIdIterator(Generic[_idType]):
    def __iter__(self):
        return self

    def __next__(self) -> _idType:
        raise StopIteration

    def first(self) -> Union[_idType, None]:
        return None

    def toList(self, count: Optional[int] = None) -> List[_idType]:
        return []

    @property
    def count(self) -> int:
        return 0


class IdIterator(Generic[_idType, REQUEST], EntityConnector[Entity]):
    """Represents a connected LOGS entity id iterator"""

    _entityIterator: int
    _currentResults: Optional[RESPONSE_TYPES]
    _generatorType: Optional[Type[_idType]] = None
    _parameterType: Optional[Type[REQUEST]] = None

    _parametersInput: Optional[REQUEST]
    _parameters: REQUEST
    _responseType: ResponseTypes = ResponseTypes.JSON
    _includeUrl: bool = True
    _connection: Optional[LOGSConnection]
    _count: Optional[int]

    def __init__(
        self, connection: Optional[LOGSConnection], parameters: Optional[REQUEST] = None
    ):
        super().__init__(connection=connection)

        self._parametersInput = parameters

        self._entityIterator = 0
        self._currentResults = None
        self._count = None

    def __iter__(self):
        self._initEntityIterator()
        return self

    def __next__(self) -> _idType:
        if not self._generatorType:
            raise NotImplementedError(
                "Iterator cannot generate items without a specified 'generatorType' field in class %a"
                % type(self).__name__
            )

        return self._getNextEntity()

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

    def _checkParameterType(self):
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

        if self._parametersInput and not isinstance(
            self._parametersInput, self._parameterType
        ):
            raise LOGSException(
                "Parameter for iterator %a must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self._parameterType.__name__,
                    type(self._parametersInput).__name__,
                )
            )

        self._parametersInput = Tools.checkAndConvert(
            self._parametersInput, self._parameterType, "parameters", initOnNone=True
        )

    def _initEntityIterator(self):
        self._checkParameterType()

        url = self.getBaseUrl()
        self._entityIterator = 0

        if not self._connection:
            raise LOGSException(
                "Entity connector %a is not connected" % type(self).__name__
            )

        tmp = False
        if hasattr(self._parameters, "includeCount"):
            tmp = self._parameters.includeCount
            self._parameters.includeCount = True

        self._currentResults, responseError = self._connection.postUrl(
            url=url + "/ids_only",
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

    def first(self):
        i = iter(self)
        try:
            return cast(_idType, next(i))
        except StopIteration:
            return None

    def toList(self, count: Optional[int] = None):
        if count:
            count = int(count)
            if count < 0:
                raise Exception("Invalid negative count %d" % count)
            result = cast(List[_idType], [])
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
