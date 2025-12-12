import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from deprecation import deprecated  # type: ignore

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint, UiEndpoint
from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    EntityIncompleteException,
    LOGSException,
)
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.ParameterHelper import ParameterHelper
from LOGS.Converter import Converter
from LOGS.Converter.Conversion import Conversion
from LOGS.Converter.ExportParameters import ExportParameters
from LOGS.Entities.DatasetBase import DatasetBase
from LOGS.Entities.DatasetModels import DatasetSource, ParsedMetadata
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.Track import Track
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ISignableEntity import ISignableEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection
from LOGS.Parameters.ParameterList import ParameterList

if TYPE_CHECKING:
    from LOGS.Entities.BridgeMinimal import BridgeMinimal
    from LOGS.Entities.DataFormatMinimal import DataFormatMinimal


@Endpoint("datasets")
@UiEndpoint("#data")
class Dataset(
    DatasetBase,
    IUniqueEntity,
    ITypedEntity,
    IOwnedEntity,
    IProjectBased,
    IEntryRecord,
    IModificationRecord,
    ISoftDeletable,
    ILockableEntity,
    IGenericPermissionEntity,
    ISignableEntity,
):

    # state of additionally fetched data
    _noParameters = True
    _noExports = True
    _noParameterTree = True

    # private attributes
    _parameterHelper: Optional[ParameterHelper] = None

    # fields
    _automaticName: Optional[str] = None
    _isManuallyNamed: Optional[bool] = None
    _creationDate: Optional[datetime] = None
    _claimed: Optional[bool] = None
    _bridge: Optional["BridgeMinimal"] = None
    _parsedMetadata: Optional[ParsedMetadata] = None
    _source: Optional[DatasetSource] = None

    # special fetched fields
    _parameters: Optional[Dict[str, Any]] = None
    _parameterTree: Optional[ParameterList] = None
    _exports: Optional[List[Converter]] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        formatOrFormatId: Optional[Union[str, "DataFormatMinimal"]] = None,
        pathPrefixToStrip: Optional[str] = None,
        pathPrefixToAdd: Optional[str] = None,
    ):
        super().__init__(ref=ref, id=id, connection=connection)

        t = type(self)
        self._noSerialize += [
            t.parameters.fget.__name__,  # type: ignore
            t.parameterTree.fget.__name__,  # type: ignore
            t.formatVersion.fget.__name__,  # type: ignore
            t.parserLogs.fget.__name__,  # type: ignore
            t.tracks.fget.__name__,  # type: ignore
            t.datatracks.fget.__name__,  # type: ignore
            t.tracksHierarchy.fget.__name__,  # type: ignore
            t.exports.fget.__name__,  # type: ignore
        ]

        if isinstance(ref, Dataset):
            self._format = ref._format

        if formatOrFormatId:
            self.format = formatOrFormatId

        if files:
            if not self._format or not self._format.id:
                raise LOGSException(
                    "Cannot create %s object from files parameter without a format"
                    % type(self).__name__
                )

            self._files = FileEntry.entriesFromFiles(files)
            if self._files is not None:
                for file in self._files:
                    if pathPrefixToStrip and file.path:
                        file.modifyPathPrefix(pathPrefixToStrip, pathPrefixToAdd)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "parameters" in ref:
                self._parameters = self.checkAndConvertNullable(
                    ref["parameters"], dict, "parameters"
                )
                self._noParameters = False
            if "parameterTree" in ref:
                self._parameterTree = self.checkAndConvertNullable(
                    ref["parameterTree"], ParameterList, "parameters"
                )
                self._noParameterTree = False

            infoFields = [
                "formatVersion",
                "parserLogs",
                "tracks",
                "datatracks",
                "tracksHierarchy",
                "parsingState",
            ]

            self._noInfo = not all(f in ref for f in infoFields)

            info = {}
            for field in infoFields:
                if field in ref:
                    info[field] = ref[field]
                    del ref[field]

        super().fromDict(ref=ref)
        self._setInfo(info)

    def fetchParameters(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, responseError = connection.getEndpoint(
            endpoint + [id, "parameters"]
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(parameters, dict):
            if "url" in parameters:
                del parameters["url"]
            self._parameters = parameters
        else:
            self._parameters = {}

        self._parameterHelper = ParameterHelper(self._parameters)
        self._noParameters = False

    def fetchParameterTree(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, responseError = connection.getEndpoint(
            endpoint + [id, "parameter_tree"]
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if parameters == "":
            parameters = None

        self._parameterTree = self.checkAndConvertNullable(
            parameters, ParameterList, "parameterTree"
        )

        self._noParameterTree = False

    def fetchExports(self):
        connection, endpoint, id = self._getConnectionData()

        exports, responseError = connection.getEndpoint(endpoint + [id, "exports"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        self.exports = exports
        self._noExports = False

    def clearCache(self):
        dataDir = self._getDataDir()
        if dataDir and os.path.exists(dataDir) and self.datatracks:
            for datatrack in self.datatracks:
                datatrack.clearCache()
            os.rmdir(dataDir)

    def fetchFull(self):
        self.fetchParameters()
        self.fetchInfo()
        self.fetchZipSize()
        self.fetchExports()

    def getParameter(self, key, removeUnit=False):
        if not self._parameterHelper:
            self._parameterHelper = ParameterHelper(self.parameters)
        return self._parameterHelper.get(key, removeUnit)

    def _requestReport(self, exportId: str, parameters: Optional[ExportParameters]):
        connection, endpoint, id = self._getConnectionData()
        converterEndpoint: Any = endpoint + [id, "exports", exportId]
        payload = parameters.toDict() if parameters else {}
        data, responseError = connection.postEndpoint(converterEndpoint, data=payload)
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        # TODO: create a report type to wait for the report to be generated
        # TODO: maybe a class "Conversion" can be created that has a state and also and automatic awaiter function or so
        conversion = self.checkAndConvert(data, Conversion, f"Conversion_to_{exportId}")
        conversion._endpoint = converterEndpoint
        conversion._payload = payload
        conversion._parentEntity = self
        return conversion

    def exportTo(
        self, exportId: str, parameters: Optional[Union[ExportParameters, dict]] = None
    ):

        if self._noExports:
            self.fetchExports()

        if self.exports is None:
            raise LOGSException(f"Export id '{exportId}' not found in exports")

        exports = {e.exportId: e for e in self.exports}
        exports.update({e.id: e for e in self.exports})
        if exportId not in exports:
            raise LOGSException(f"Export id '{exportId}' not found in exports")

        export = exports[exportId]
        p = export.requestParameter
        if parameters is not None and p is not None:
            if isinstance(parameters, dict):
                p.fromDict(parameters)
            elif isinstance(parameters, ExportParameters):
                if parameters._parentId is None or parameters._parentId != p._parentId:
                    raise LOGSException(
                        f"The passed export parameters is not generated by and valid export format. (Expected class '{p.identifier}')"
                    )
            else:
                raise LOGSException(
                    f"Invalid parameter type '{type(parameters).__name__}'. (Expected 'dict' or '{ExportParameters.__name__}')"
                )

        return self._requestReport(exportId, p)

    def getTrackById(self, trackId: str) -> Optional[Track]:
        if not self._tracks:
            return None
        for track in self._tracks:
            if track.id == trackId:
                return track
        return None

    @property
    def format(self) -> Optional["DataFormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        if isinstance(value, str):
            value = {"id": value}
        self._format = MinimalModelGenerator.MinimalFromSingle(
            value, "DataFormatMinimal", "format", connection=self._getConnection()
        )

    @property
    def creationDate(self) -> Optional[datetime]:
        return self._creationDate

    @creationDate.setter
    def creationDate(self, value):
        self._creationDate = self.checkAndConvertNullable(
            value, datetime, "creationDate"
        )

    @property
    def claimed(self) -> Optional[bool]:
        return self._claimed

    @claimed.setter
    def claimed(self, value):
        self._claimed = self.checkAndConvertNullable(value, bool, "claimed")

    @property
    def parsedMetadata(self) -> Optional[ParsedMetadata]:
        return self._parsedMetadata

    @parsedMetadata.setter
    def parsedMetadata(self, value):
        self._parsedMetadata = self.checkAndConvertNullable(
            value, ParsedMetadata, "parsedMetadata"
        )

    @property
    def parameters(self) -> Optional[Dict[str, Any]]:
        if self._noParameters:
            raise EntityIncompleteException(
                self,
                parameterName="parameters",
                functionName=f"{self.fetchParameters.__name__}()",
            )
        return self._parameters

    @property
    def parameterTree(self) -> Optional[ParameterList]:
        if self._noParameterTree:
            raise EntityIncompleteException(
                self,
                parameterName="parameterTree",
                functionName=f"{self.fetchParameterTree.__name__}()",
                hasFetchFull=False,
            )
        return self._parameterTree

    @property
    def formatVersion(self) -> Optional[int]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="formatVersion",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._formatVersion

    @property
    def tracks(self) -> Optional[List[Track]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracks

    @property
    def datatracks(self) -> Optional[List[Datatrack]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="datatracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._datatracks

    @property
    def tracksHierarchy(self) -> Optional[HierarchyNode]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracksHierarchy",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracksHierarchy

    @property
    def bridge(self) -> Optional["BridgeMinimal"]:
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = MinimalModelGenerator.MinimalFromSingle(
            value, "BridgeMinimal", "bridge", connection=self._getConnection()
        )

    @property
    def bridgeId(self) -> Optional[int]:
        return self._bridge.id if self._bridge else None

    @bridgeId.setter
    def bridgeId(self, value):
        self._bridge = MinimalModelGenerator.MinimalFromSingle(
            value, "BridgeMinimal", "bridge", connection=self._getConnection()
        )

    @property
    def exports(self) -> Optional[List[Converter]]:
        if self._noExports:
            raise EntityIncompleteException(
                self,
                parameterName="exports",
                functionName=f"{self.fetchExports.__name__}()",
                hasFetchFull=True,
            )

        return self._exports

    @exports.setter
    def exports(self, value):
        self._exports = self.checkListAndConvertNullable(value, Converter, "exports")

    @property
    def source(self) -> Optional[DatasetSource]:
        return self._source

    @source.setter
    def source(self, value):
        self._source = self.checkAndConvertNullable(value, DatasetSource, "source")

    @property
    def isManuallyNamed(self) -> Optional[bool]:
        return self._isManuallyNamed

    @isManuallyNamed.setter
    def isManuallyNamed(self, value):
        self._isManuallyNamed = self.checkAndConvertNullable(
            value, bool, "isManuallyNamed"
        )

    @property
    def automaticName(self) -> Optional[str]:
        return self._automaticName

    @automaticName.setter
    def automaticName(self, value):
        self._automaticName = self.checkAndConvertNullable(value, str, "automaticName")
