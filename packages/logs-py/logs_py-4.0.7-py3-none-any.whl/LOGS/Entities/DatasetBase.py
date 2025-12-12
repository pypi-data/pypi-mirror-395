import os
from typing import Any, Dict, List, Optional, cast

from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    EntityIncompleteException,
    LOGSException,
)
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.DataFormatMinimal import DataFormatMinimal
from LOGS.Entities.DatasetInfo import DatasetInfo
from LOGS.Entities.DatasetRequestParameter import ParsingStates
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entities.Track import Track
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import ResponseTypes


class DatasetBase(
    IEntityWithIntId,
    INamedEntity,
):
    # private attributes
    _files: Optional[List[FileEntry]] = None

    # state of additionally fetched data
    _noInfo = True

    # fields
    _path: Optional[str] = None

    # special fetched fields
    ## Getter and setter implemented in inherited classes
    _formatVersion: Optional[int] = None
    _tracks: Optional[List[Track]] = None
    _datatracks: Optional[List[Datatrack]] = None
    _tracksHierarchy: Optional[HierarchyNode] = None

    ## Getter and setter implemented in this class
    _parsingState: Optional[ParsingStates] = None
    _parserLogs: Optional[List[ParserLog]] = None
    _zipSize: Optional[int] = None
    _format: Optional["DataFormatMinimal"] = None

    def fetchZipSize(self):
        connection, endpoint, id = self._getConnectionData()

        zip, responseError = connection.getEndpoint(
            endpoint + ["zip_size"], parameters={"ids": [self.id]}
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(zip, dict) and "size" in zip:
            self._zipSize = zip["size"]

    def _getDataDir(self):
        if self.cacheDir:
            if not os.path.isdir(self.cacheDir):
                raise LOGSException(
                    f"Specified cache directory '{self.cacheDir}' cannot be opened or is not a directory."
                )
            return self.cacheDir
        return None

    def fetchInfo(self):
        connection, endpoint, id = self._getConnectionData()

        data, responseError = connection.getEndpoint(endpoint + [id, "info"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        dataDir = self._getDataDir()
        if dataDir and not os.path.exists(dataDir):
            os.mkdir(dataDir)

        self._setInfo(cast(dict, data))
        self._noInfo = False
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack._endpoint = (
                    endpoint + [str(id), "datatrack"] if endpoint else None
                )

    def _setInfo(self, data: dict):
        info = DatasetInfo(data)
        self._formatVersion = info.formatVersion
        self._parserLogs = info.parserLogs
        self._tracks = info.tracks
        self._datatracks = info.datatracks
        self._tracksHierarchy = info.tracksHierarchy
        self._parsingState = info.parsingState

        dataDir = self._getDataDir()

        trackLookup: Dict[str, Datatrack] = {}
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack._setConnection(self._getConnection())
                datatrack.cacheDir = dataDir
                if datatrack.id:
                    trackLookup[datatrack.id] = datatrack

        if self._tracks:
            for track in self._tracks:
                track._setConnection(self._getConnection())
                track.cacheDir = dataDir
                if track._dataIds:
                    track.datatracks = cast(
                        Any,
                        {
                            k: (trackLookup[v] if v in trackLookup else None)
                            for k, v in track._dataIds.items()
                        },
                    )

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ):
        connection, endpoint, id = self._getConnectionData()

        if not directory:
            directory = os.curdir

        if not fileName:
            fileName = self.name if self.name and self.name != "" else "Dataset"
            fileName += ".zip"

        path = os.path.join(directory, Tools.sanitizeFileName(fileName=fileName))

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, responseError = connection.getEndpoint(
            endpoint + [id, "files", "zip"], responseType=ResponseTypes.RAW
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        with open(path, mode="wb") as localFile:
            localFile.write(cast(bytes, data))

        return path

    @property
    def format(self) -> Optional["DataFormatMinimal"]:
        return self._format

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, value):
        self._path = self.checkAndConvertNullable(value, str, "path")

    @property
    def parserLogs(self) -> Optional[List[ParserLog]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="parserLogs",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._parserLogs

    @property
    def parsingState(self) -> Optional[ParsingStates]:
        return self._parsingState

    @parsingState.setter
    def parsingState(self, value):
        self._parsingState = cast(
            ParsingStates, self.checkAndConvertNullable(value, str, "parsingState")
        )

    @property
    def zipSize(self) -> Optional[int]:
        if self._zipSize is None:
            raise EntityIncompleteException(
                self,
                parameterName="zipSize",
                functionName=f"{self.fetchZipSize.__name__}()",
            )
        return self._zipSize
