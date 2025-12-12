from typing import Any, Dict, List, Optional, Union

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import EntityCreatingException, LOGSException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.Attachment import Attachment
from LOGS.Entities.Dataset import Dataset
from LOGS.Entities.DatasetModels import ViewableEntityTypes
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.EntityConnector import EntityConnector
from LOGS.LOGSConnection import LOGSConnection, MultipartEntry


class DatasetUploadRequest(ConnectedEntity):
    _typeMapper = {"files": FileEntry}
    _dataset: Optional[Union[Dataset, Attachment]] = None

    _viewableEntityTypes: Optional[List[ViewableEntityTypes]] = None
    _isViewableEntity: Optional[bool] = None
    _files: Optional[List[FileEntry]] = None
    _filePathsAreAbsolute: Optional[bool] = True

    def __init__(
        self,
        ref=None,
        dataset: Optional[Union[Dataset, Attachment]] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        super().__init__(ref=ref, connection=connection)

        if not dataset:
            return
        self._dataset = dataset

        if not isinstance(dataset, (Dataset, Attachment)):
            raise ValueError(
                f"Dataset parameter must be of type Dataset or Attachment in the {type(self).__name__} constructor."
            )
        self._files = dataset._files
        self._format = dataset._format
        if isinstance(dataset, Attachment):
            self._isViewableEntity = True
            self._viewableEntityTypes = dataset._viewableEntityTypes

    def toDict(self) -> Dict[str, Any]:
        result = self._dataset.toDict() if self._dataset else {}
        result.update(super().toDict())
        return result

    @property
    def files(self) -> Optional[List[FileEntry]]:
        return self._files

    @files.setter
    def files(self, value):
        self._files = self.checkListAndConvertNullable(value, FileEntry, "files")

    @property
    def filePathsAreAbsolute(self) -> Optional[bool]:
        return self._filePathsAreAbsolute

    @filePathsAreAbsolute.setter
    def filePathsAreAbsolute(self, value):
        self._filePathsAreAbsolute = self.checkAndConvertNullable(
            value, bool, "filePathsAreAbsolute"
        )

    @property
    def isViewableEntity(self) -> Optional[bool]:
        return self._isViewableEntity

    @isViewableEntity.setter
    def isViewableEntity(self, value):
        self._isViewableEntity = self.checkAndConvertNullable(
            value, bool, "isViewableEntity"
        )

    @property
    def viewableEntityTypes(self) -> Optional[List[ViewableEntityTypes]]:
        return self._viewableEntityTypes

    @viewableEntityTypes.setter
    def viewableEntityTypes(self, value):
        self._viewableEntityTypes = self.checkListAndConvertNullable(
            value, ViewableEntityTypes, "viewableEntityTypes"
        )


@Endpoint("datasets")
class DatasetCreator(EntityConnector):
    _request: DatasetUploadRequest = DatasetUploadRequest()
    _formatId: str
    _files: List[FileEntry]

    def __init__(self, connection: LOGSConnection, dataset: Union[Dataset, Attachment]):
        self._connection = connection

        if not dataset:
            raise LOGSException("Cannot not create empty dataset")
        if not dataset._files:
            raise LOGSException("Cannot not create dataset without files")
        if not dataset.format or not dataset.format.id:
            raise LOGSException("Cannot not create dataset without a format field")

        self._formatId = dataset.format.id
        self._files = dataset._files
        dataset._setConnection(self._connection)
        self._request = self._getDatasetUploadRequest(dataset=dataset)

    def create(self):
        connection, endpoint = self._getConnectionData()

        multipart = [
            MultipartEntry(
                name="Dataset", fileName=None, content=self._request.toDict()
            )
        ]
        multipart.extend(
            [
                MultipartEntry(name="files", fileName=file.id, content=file)
                for file in self._files
            ]
        )

        data, responseError = connection.postMultipartEndpoint(
            endpoint=endpoint + ["create"], data=multipart
        )
        if responseError:
            raise EntityCreatingException(responseError=responseError)

        return Tools.checkAndConvert(data, dict, "dataset creation result")

    def _getDatasetUploadRequest(self, dataset: Union[Dataset, Attachment]):
        # print("\n".join([f.fullPath for f in fileList]))
        if not self._files:
            raise LOGSException("Cannot not create dataset without files")
        if not self._formatId:
            raise LOGSException("Cannot not create dataset without a formatId")

        for file in self._files:
            file.addMtime()

        request = DatasetUploadRequest(
            dataset=dataset, connection=self._getConnection()
        )

        return request
