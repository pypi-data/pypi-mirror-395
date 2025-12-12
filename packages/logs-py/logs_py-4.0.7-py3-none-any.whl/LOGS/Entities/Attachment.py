from typing import TYPE_CHECKING, List, Optional, Sequence

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint, UiEndpoint
from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Entities.DatasetBase import DatasetBase
from LOGS.Entities.DatasetModels import ViewableEntityTypes
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    pass


@Endpoint("datasets")
@UiEndpoint("#data")
class Attachment(
    DatasetBase,
    IUniqueEntity,
    IEntryRecord,
    IModificationRecord,
):
    _viewableEntityTypes: List[ViewableEntityTypes] = [ViewableEntityTypes.CustomField]
    _isViewableEntity: bool = True

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        pathPrefixToStrip: Optional[str] = None,
        pathPrefixToAdd: Optional[str] = None,
    ):
        from LOGS.Entities.DataFormatMinimal import DataFormatMinimal

        super().__init__(ref=ref, id=id, connection=connection)

        t = type(self)
        self._noSerialize += [
            t.parserLogs.fget.__name__,  # type: ignore
        ]
        self._format = DataFormatMinimal(
            id="doc_multi", name="Attachment format", connection=self._getConnection()
        )

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

            infoFields = [
                "parserLogs",
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

    def fetchFull(self):
        self.fetchInfo()
        self.fetchZipSize()
