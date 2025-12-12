import os
from typing import List, Optional, Sequence, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.Dataset import Dataset
from LOGS.Entities.DatasetMatchTypes import (
    DatasetForSearch,
    DatasetSearchRequest,
    DatasetSearchResult,
)
from LOGS.Entities.DatasetRequestParameter import DatasetRequestParameter
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entity.EntityIterator import EntityIterator
from LOGS.LOGSConnection import ResponseTypes


@Endpoint("datasets")
class Datasets(EntityIterator[Dataset, DatasetRequestParameter]):
    """LOGS connected Dataset iterator"""

    _generatorType = Dataset
    _parameterType = DatasetRequestParameter

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ) -> str:
        connection, endpoint = self._getConnectionData()

        if not directory:
            directory = os.curdir

        path = os.path.join(
            directory,
            Tools.sanitizeFileName(fileName=fileName, defaultName="Dataset.zip"),
        )

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, error = connection.postEndpoint(
            endpoint=endpoint + ["zip"],
            data=self._parameters.toDict(),
            responseType=ResponseTypes.RAW,
        )
        if error:
            raise LOGSException(
                "Could not fetch datasets zip file: %a" % error.errorString()
            )

        with open(path, mode="wb") as localFile:
            localFile.write(cast(bytes, data))

        return path

    def _getDatasetSearchRequest(
        self,
        files: Sequence[Constants.FILE_TYPE],
        formatIds: List[str],
        checkUpdatable=True,
    ):
        fileList = FileEntry.entriesFromFiles(files)
        for file in fileList:
            file.addHash()
        # print("\n".join([f.fullPath for f in fileList]))

        request = DatasetSearchRequest()

        request.datasets = []
        for formatId in formatIds:
            dataset = DatasetForSearch()
            dataset.checkUpdatable = checkUpdatable
            dataset.formatId = formatId
            dataset.files.extend(fileList)
            request.datasets.append(dataset)
        return request

    def findDatasetByFiles(
        self,
        files: Sequence[Constants.FILE_TYPE],
        formatIds: List[str],
        checkUpdatable=True,
    ):
        request = self._getDatasetSearchRequest(files, formatIds, checkUpdatable)
        connection, endpoint = self._getConnectionData()

        data, errors = connection.postEndpoint(
            endpoint=endpoint + ["find"], data=request.toDict()
        )
        if errors:
            raise LOGSException("Could not find dataset by files: %a" % errors)

        return Tools.checkListAndConvert(data, DatasetSearchResult, "files search")

    def __iter__(self):
        if self._parameters:
            parameters = cast(DatasetRequestParameter, self._parameters)

            if parameters.files:
                if not parameters.formatIds:
                    typeName = type(parameters).__name__
                    raise LOGSException(
                        "%s.formatIds must be defined when %s.files is used."
                        % (typeName, typeName)
                    )

                results = self.findDatasetByFiles(
                    parameters.files, parameters.formatIds, False
                )

                if len(results) > 0:
                    if parameters.ids is None:
                        parameters.ids = []

                    cast(List[int], parameters.ids).extend(
                        [r.logsId for r in results if r.logsId]
                    )
        self._initEntityIterator()
        return self

    def __next__(self):
        dataset = super().__next__()

        if self._parameters.includeParameters:
            dataset.fetchParameters()
        if self._parameters.includeInfo:
            dataset.fetchInfo()
        if self._parameters.includeZipSize:
            dataset.fetchZipSize()
        if self._parameters.includeExports:
            dataset.fetchExports()

        return dataset
