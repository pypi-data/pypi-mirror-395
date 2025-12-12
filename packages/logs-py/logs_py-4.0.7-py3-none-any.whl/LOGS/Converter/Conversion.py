import os
from enum import Enum
from time import sleep, time
from typing import Any, Callable, Dict, List, Optional, cast

from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    LOGSException,
    UnfinishedConversionException,
)
from LOGS.Auxiliary.Tools import Tools
from LOGS.Converter.ConverterParameter import ParameterType
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entity import Entity
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.SerializableContent import SerializableClass
from LOGS.LOGSConnection import ResponseTypes


class ConversionState(Enum):
    Successful = "Successful"
    Failed = "Failed"
    Waiting = "Waiting"


class ConversionFile(SerializableClass):
    path: Optional[str] = None
    size: Optional[int] = None


class DatasetConversionZipReadModel(SerializableClass):
    size: Optional[int] = None
    id: Optional[str] = None
    url: Optional[str] = None


class ConverterParameterEntry(SerializableClass):
    id: Optional[str] = None
    value: Optional[Any] = None
    type: Optional[ParameterType] = None


class ConversionLogModel(ParserLog):
    pass


class Conversion(ConnectedEntity):
    _datasetId: Optional[int] = None
    _datasetFormat: Optional[str] = None
    _exportFormat: Optional[str] = None
    _files: Optional[List[ConversionFile]] = None
    _logs: Optional[List[ConversionLogModel]] = None
    _output: Optional[str] = None
    _state: Optional[ConversionState] = None
    _zip: Optional[DatasetConversionZipReadModel] = None
    _inputParameters: Optional[List[ConverterParameterEntry]] = None

    _payload: Dict[str, Any] = {}
    _parentEntity: Optional[Entity] = None

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ):
        connection, _ = self._getConnectionData()

        if self.state == ConversionState.Waiting:
            raise UnfinishedConversionException(self)

        if self.state == ConversionState.Failed:
            raise LOGSException(
                f"Conversion for dataset {self.datasetId} from format '{self.datasetFormat}' to format '{self.exportFormat}' failed. Check logs for more information."
            )

        if (
            self.zip is None
            or self.zip.size is None
            or self.zip.id is None
            or self.zip.url is None
        ):
            raise LOGSException(
                f"Conversion for dataset {self.datasetId} from format '{self.datasetFormat}' to format '{self.exportFormat}' did not result in any data."
            )

        if not directory:
            directory = os.curdir

        if not fileName:
            fileName = f"dataset_{self.datasetId}_{self.zip.id}.zip"

        path = os.path.join(directory, Tools.sanitizeFileName(fileName=fileName))

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, responseError = connection.getUrl(
            self.zip.url, responseType=ResponseTypes.RAW
        )

        if responseError:
            raise LOGSException(
                f"Could not fetch conversion result for dataset {self.datasetId} from format '{self.datasetFormat}' to format '{self.exportFormat}'.",
                responseError=responseError,
            )

        with open(path, mode="wb") as localFile:
            localFile.write(cast(bytes, data))

        return path

    def _reloadOnWaiting(self, connection, endpoint):
        if self.state != ConversionState.Waiting:
            return
        data, responseError = connection.postEndpoint(endpoint, data=self._payload)
        if responseError:
            raise EntityFetchingException(
                entity=self._parentEntity, responseError=responseError
            )
        self.fromDict(data)

    def awaitResult(self):
        connection, endpoint = self._getConnectionData()
        if self.state != ConversionState.Waiting:
            return

        while self.state == ConversionState.Waiting:
            sleep(0.5)
            # print("request...")

            self._reloadOnWaiting(connection, endpoint)

            # print("... done", self.state)

    @classmethod
    def awaitAllResults(
        cls,
        conversions: List["Conversion"],
        timeout=600,
        stateChangeHook: Optional[Callable[[int], None]] = None,
    ):
        l = [c for c in conversions if c is not None]

        connectionList = []
        for i, c in enumerate(l):
            connection, endpoint = c._getConnectionData()
            connectionList.append((c, connection, endpoint))

        count = sum(
            [1 for c in connectionList if c[0].state != ConversionState.Waiting]
        )
        if stateChangeHook:
            stateChangeHook(len(connectionList) - count)

        start = time()
        while count < len(connectionList) and time() - start < timeout:
            oldCount = count
            count = 0
            for c in connectionList:
                if c[0].state != ConversionState.Waiting:
                    count += 1
                    continue
                c[0]._reloadOnWaiting(c[1], c[2])
            if stateChangeHook and oldCount != count:
                stateChangeHook(len(connectionList) - count)
            # print(f"waiting for {len(connectionList) -count} jobs")
            sleep(0.5)

    @property
    def datasetId(self) -> Optional[int]:
        return self._datasetId

    @datasetId.setter
    def datasetId(self, value):
        self._datasetId = self.checkAndConvertNullable(value, int, "datasetId")

    @property
    def datasetFormat(self) -> Optional[str]:
        return self._datasetFormat

    @datasetFormat.setter
    def datasetFormat(self, value):
        self._datasetFormat = self.checkAndConvertNullable(value, str, "datasetFormat")

    @property
    def exportFormat(self) -> Optional[str]:
        return self._exportFormat

    @exportFormat.setter
    def exportFormat(self, value):
        self._exportFormat = self.checkAndConvertNullable(value, str, "exportFormat")

    @property
    def files(self) -> Optional[List[ConversionFile]]:
        return self._files

    @files.setter
    def files(self, value):
        self._files = self.checkListAndConvertNullable(value, ConversionFile, "files")

    @property
    def logs(self) -> Optional[List[ConversionLogModel]]:
        return self._logs

    @logs.setter
    def logs(self, value):
        self._logs = self.checkListAndConvertNullable(value, ConversionLogModel, "logs")

    @property
    def output(self) -> Optional[str]:
        return self._output

    @output.setter
    def output(self, value):
        self._output = self.checkAndConvertNullable(value, str, "output")

    @property
    def state(self) -> Optional[ConversionState]:
        return self._state

    @state.setter
    def state(self, value):
        self._state = self.checkAndConvertNullable(value, ConversionState, "state")

    @property
    def zip(self) -> Optional[DatasetConversionZipReadModel]:
        return self._zip

    @zip.setter
    def zip(self, value):
        self._zip = self.checkAndConvertNullable(
            value, DatasetConversionZipReadModel, "zip"
        )

    @property
    def inputParameters(self) -> Optional[List[ConverterParameterEntry]]:
        return self._inputParameters

    @inputParameters.setter
    def inputParameters(self, value):
        self._inputParameters = self.checkListAndConvertNullable(
            value, ConverterParameterEntry, "inputParameters"
        )
