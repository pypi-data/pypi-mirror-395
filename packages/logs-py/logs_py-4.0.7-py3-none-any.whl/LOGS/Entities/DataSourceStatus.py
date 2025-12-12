from datetime import datetime
from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entities.RunState import RunState
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Entity.SerializableContent import SerializableClass


class DataSourceStatusError(SerializableClass):
    message: Optional[str] = None


@Endpoint("data_sources_status")
class DataSourceStatus(IEntityWithIntId):
    _type: Optional[BridgeType] = None
    _uuid: Optional[str] = None
    _lastUpdated: Optional[datetime] = None
    _counter: Optional[int] = None
    _dataSourceId: Optional[int] = None
    _runState: Optional[RunState] = None
    _startedOn: Optional[datetime] = None
    _duration: Optional[float] = None
    _errors: Optional[List[DataSourceStatusError]] = None
    _info: Optional[dict] = None

    @property
    def type(self) -> Optional[BridgeType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, BridgeType, "type")

    @property
    def uuid(self) -> Optional[str]:
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = self.checkAndConvertNullable(value, str, "uuid")

    @property
    def lastUpdated(self) -> Optional[datetime]:
        return self._lastUpdated

    @lastUpdated.setter
    def lastUpdated(self, value):
        self._lastUpdated = self.checkAndConvertNullable(value, datetime, "lastUpdated")

    @property
    def counter(self) -> Optional[int]:
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = self.checkAndConvertNullable(value, int, "counter")

    @property
    def dataSourceId(self) -> Optional[int]:
        return self._dataSourceId

    @dataSourceId.setter
    def dataSourceId(self, value):
        self._dataSourceId = self.checkAndConvertNullable(value, int, "dataSourceId")

    @property
    def runState(self) -> Optional[RunState]:
        return self._runState

    @runState.setter
    def runState(self, value):
        self._runState = self.checkAndConvertNullable(value, RunState, "runState")

    @property
    def startedOn(self) -> Optional[datetime]:
        return self._startedOn

    @startedOn.setter
    def startedOn(self, value):
        self._startedOn = self.checkAndConvertNullable(value, datetime, "startedOn")

    @property
    def duration(self) -> Optional[float]:
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = self.checkAndConvertNullable(value, float, "duration")

    @property
    def errors(self) -> Optional[List[DataSourceStatusError]]:
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = self.checkListAndConvertNullable(
            value, DataSourceStatusError, "errors"
        )

    @property
    def info(self) -> Optional[dict]:
        return self._info

    @info.setter
    def info(self, value):
        self._info = self.checkAndConvertNullable(value, dict, "info")
