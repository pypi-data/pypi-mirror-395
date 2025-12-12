from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import EntityAPIException
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entities.Bridge import Bridge
from LOGS.Entities.DataFormat import DataFormat
from LOGS.Entities.DatasetTemplate import DatasetTemplate
from LOGS.Entities.DataSourceConnectionStatus import DataSourceConnectionStatus
from LOGS.Entities.DataSourceStatusIterator import DataSourceStatusIterator
from LOGS.Entities.DataSourceStatusRequestParameter import (
    DataSourceStatusRequestParameter,
    DataSourceStatusSortingOptions,
)
from LOGS.Entities.FileExcludePattern import FileExcludePattern
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.DataFormatMinimal import DataFormatMinimal


class DataSourceType(Enum):
    Crawler = "Crawler"
    IconNMR = "IconNMR"


class DataSourceUpdateMode(Enum):
    Deactivated = "Deactivated"
    UseHash = "UseHash"
    UsePath = "UsePath"


@Endpoint("data_sources")
class DataSource(
    IEntityWithIntId,
    INamedEntity,
    IUniqueEntity,
    IEntryRecord,
    IModificationRecord,
    IGenericPermissionEntity,
):
    _type: Optional[DataSourceType] = None
    _enabled: Optional[bool] = None
    _bridge: Optional["Bridge"] = None
    _format: Optional["DataFormatMinimal"] = None
    _customImport: Optional[EntityMinimalWithStrId] = None
    _datasetUpdateMode: Optional[DataSourceUpdateMode] = None
    _parser: Optional[DataFormat] = None
    _directories: Optional[List[str]] = None
    _intervalInSeconds: Optional[int] = None
    _cutoffDate: Optional[datetime] = None
    _fileExcludePatterns: Optional[List[FileExcludePattern]] = None
    _status: Optional[DataSourceConnectionStatus] = None
    _datasetTemplate: Optional[DatasetTemplate] = None

    def triggerAutoload(self):
        connection, endpoint, id = self._getConnectionData()

        _, responseError = connection.getEndpoint(endpoint + [id, "trigger_autoload"])
        if responseError:
            raise EntityAPIException(entity=self, responseError=responseError)

    @property
    def history(self) -> Optional[DataSourceStatusIterator]:
        return DataSourceStatusIterator(
            self._getConnection(),
            DataSourceStatusRequestParameter(
                dataSourceIds=[self.id],
                sortBy=DataSourceStatusSortingOptions.STARTED_ON,
            ),
        )

    @property
    def enabled(self) -> Optional[bool]:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = self.checkAndConvertNullable(value, bool, "enabled")

    @property
    def formats(self) -> Optional[List["DataFormatMinimal"]]:
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = MinimalModelGenerator.MinimalFromList(
            value, "DataFormatMinimal", "formats", connection=self._getConnection()
        )

    @property
    def directories(self) -> Optional[List[str]]:
        return self._directories

    @directories.setter
    def directories(self, value):
        self._directories = self.checkListAndConvertNullable(value, str, "directories")

    @property
    def intervalInSeconds(self) -> Optional[int]:
        return self._intervalInSeconds

    @intervalInSeconds.setter
    def intervalInSeconds(self, value):
        self._intervalInSeconds = self.checkAndConvertNullable(
            value, int, "intervalInSeconds"
        )

    @property
    def cutoffDate(self) -> Optional[datetime]:
        return self._cutoffDate

    @cutoffDate.setter
    def cutoffDate(self, value):
        self._cutoffDate = self.checkAndConvertNullable(value, datetime, "cutoffDate")

    @property
    def fileExcludePatterns(self) -> Optional[List[FileExcludePattern]]:
        return self._fileExcludePatterns

    @fileExcludePatterns.setter
    def fileExcludePatterns(self, value):
        self._fileExcludePatterns = self.checkListAndConvertNullable(
            value, FileExcludePattern, "fileExcludePatterns"
        )

    @property
    def customImportId(self) -> Optional[str]:
        return self._customImportId

    @customImportId.setter
    def customImportId(self, value):
        print("customImportId", value)
        self._customImportId = self.checkAndConvertNullable(
            value, str, "customImportId"
        )

    @property
    def status(self) -> Optional[DataSourceConnectionStatus]:
        return self._status

    @status.setter
    def status(self, value):
        self._status = self.checkAndConvertNullable(
            value, DataSourceConnectionStatus, "status"
        )

    @property
    def type(self) -> Optional[DataSourceType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, DataSourceType, "type")

    @property
    def bridge(self) -> Optional["Bridge"]:
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = self.checkAndConvertNullable(value, Bridge, "bridge")

    @property
    def format(self) -> Optional["DataFormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = MinimalModelGenerator.MinimalFromSingle(
            value, "DataFormatMinimal", "format", connection=self._getConnection()
        )

    @property
    def customImport(self) -> Optional[EntityMinimalWithStrId]:
        return self._customImport

    @customImport.setter
    def customImport(self, value):
        self._customImport = self.checkAndConvertNullable(
            value, EntityMinimalWithStrId, "customImport"
        )

    @property
    def datasetUpdateMode(self) -> Optional[DataSourceUpdateMode]:
        return self._datasetUpdateMode

    @datasetUpdateMode.setter
    def datasetUpdateMode(self, value):
        self._datasetUpdateMode = self.checkAndConvertNullable(
            value, DataSourceUpdateMode, "datasetUpdateMode"
        )

    @property
    def parser(self) -> Optional[DataFormat]:
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = self.checkAndConvertNullable(value, DataFormat, "parser")

    @property
    def datasetTemplate(self) -> Optional[DatasetTemplate]:
        return self._datasetTemplate

    @datasetTemplate.setter
    def datasetTemplate(self, value):
        self._datasetTemplate = self.checkAndConvertNullable(
            value, DatasetTemplate, "datasetTemplate"
        )
