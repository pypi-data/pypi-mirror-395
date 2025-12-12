import os
from typing import Any, List, Literal, Optional, cast

from LOGS.Auxiliary.Exceptions import EntityIncompleteException, LOGSException
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.LOGSConnection import LOGSConnection, ResponseTypes

_NumberTypeType = Literal["int", "float", "double"]
_DatatrackType = Literal[
    "binary", "char", "formatted_table", "image", "numeric_array", "numeric_matrix"
]
_CodecType = Literal["char", "jpeg", "points", "generator"]


class Datatrack(ConnectedEntity):
    _type: Optional[_DatatrackType] = None
    _codec: Optional[_CodecType] = None
    _id: Optional[str] = None
    _count: Optional[int] = None
    _size: Optional[List[int]] = None
    _min: Optional[List[float]] = None
    _max: Optional[List[float]] = None
    _numberType: Optional[_NumberTypeType] = None
    _data: Optional[Any] = None
    _incomplete = True

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._noSerialize += ["data"]
        super().__init__(ref=ref, connection=connection)

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a." % (type(self).__name__)
            )

        if not self.id:
            raise LOGSException("%s id is not defined." % type(self).__name__)

        return self._getConnection(), self._endpoint, self.id

    def _fetchDataFromCache(self):
        cacheFile = self._getCacheFile()
        if cacheFile is None:
            raise LOGSException("Cache directory not defined.")

        if not os.path.exists(cacheFile):
            return None

        with open(cacheFile, "rb") as f:
            return f.read()

    def _getCacheFile(self):
        if self.cacheDir is None:
            return None

        return os.path.join(self.cacheDir, self.cacheId + ".cache")

    def _storeDataInCache(self, data):
        cacheFile = self._getCacheFile()
        if cacheFile is None:
            raise LOGSException("Cache directory not defined.")
        with open(cacheFile, "wb") as f:
            f.write(data)

    def clearCache(self):
        cacheFile = self._getCacheFile()
        if cacheFile is not None:
            if os.path.exists(cacheFile):
                os.remove(cacheFile)

    def _fetchData(self):
        data = None
        if self.cacheDir:
            data = self._fetchDataFromCache()

        if data is None:
            connection, endpoint, id = self._getConnectionData()

            data, responseError = connection.getEndpoint(
                endpoint + [id], responseType=ResponseTypes.RAW
            )
            if responseError:
                raise LOGSException(
                    "Could not fetch %s: %s"
                    % (type(self).__name__, responseError.errorString()),
                    responseError=responseError,
                )

            if self.cacheDir:
                self._storeDataInCache(data)

        self._data = data

    def fetchFull(self, cacheDir: Optional[str] = None):
        self._fetchData()
        self._incomplete = False

    def __iter__(self):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is not None:
            for x in self._data:
                yield x

    @property
    def type(self) -> Optional[_DatatrackType]:
        return self._type

    @property
    def codec(self) -> Optional[_CodecType]:
        return self._codec

    @codec.setter
    def codec(self, value):
        self._codec = cast(Any, self.checkAndConvertNullable(value, str, "codec"))

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, str, "id")

    @property
    def count(self) -> Optional[int]:
        return self._count

    @count.setter
    def count(self, value):
        self._count = self.checkAndConvertNullable(value, int, "count")

    @property
    def size(self) -> Optional[List[int]]:
        return self._size

    @size.setter
    def size(self, value):
        self._size = self.checkListAndConvertNullable(value, int, "size")

    @property
    def min(self) -> Optional[List[float]]:
        return self._min

    @min.setter
    def min(self, value):
        self._min = self.checkListAndConvertNullable(value, float, "min")

    @property
    def max(self) -> Optional[List[float]]:
        return self._max

    @max.setter
    def max(self, value):
        self._max = self.checkListAndConvertNullable(value, float, "max")

    @property
    def numberType(self) -> Optional[_NumberTypeType]:
        return self._numberType

    @numberType.setter
    def numberType(self, value):
        self._numberType = cast(
            Any, self.checkAndConvertNullable(value, str, "numberType")
        )

    @property
    def data(self) -> Optional[Any]:
        raise NotImplementedError(
            "Field 'data' of %a class not implemented." % type(self).__name__
        )

    @property
    def cacheId(self) -> str:
        if self._cacheId is None:
            return f"{self.type}_{self.id}"
        else:
            return self._cacheId
