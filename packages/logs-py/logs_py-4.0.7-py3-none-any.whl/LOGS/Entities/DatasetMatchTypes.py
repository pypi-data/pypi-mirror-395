import uuid
from typing import Any, List, Optional

from deprecation import deprecated  # type: ignore

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.FileEntry import FileEntry, FileFragment
from LOGS.Entity.SerializableContent import SerializableClass


class MatchRequest(SerializableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.files: List[FileEntry] = []
        self.formatIds: Optional[List[str]] = None
        super().__init__(ref)


class DatasetForSearch(SerializableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.formatId: str = ""
        self.checkUpdatable: bool = True
        self.files: List[FileEntry] = []
        super().__init__(ref)
        self.id = uuid.uuid4().hex

    @property
    @deprecated(details="Please use property 'formatId'")
    def parserId(self):
        return self.formatId

    @parserId.setter
    @deprecated(details="Please use property 'formatId'")
    def paserId(self, value):
        self.formatId = value


class DatasetsUpdatableFiles(SerializableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(
        self,
        ref: Any = None,
        datasetId: Optional[int] = None,
        files: Optional[List[FileEntry]] = None,
    ):
        self.datasetId: int = 0
        self.files: List[FileEntry] = []
        super().__init__(ref)
        if datasetId is not None:
            self.datasetId = datasetId
        if files is not None:
            self.files = files


class DatasetSearchResult(SerializableClass):
    _typeMapper: dict = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.errors: List[str] = []
        self.logsId: Optional[int] = None
        self.isUpdateable: Optional[bool] = None
        self.files: List[FileEntry] = []
        super().__init__(ref)


class DatasetSearchRequest(SerializableClass):
    _typeMapper = {"datasets": DatasetForSearch}

    def __init__(self, ref: Any = None):
        self.datasets: List[DatasetForSearch] = []
        super().__init__(ref)


class MatchedDataset(SerializableClass):
    _typeMapper = {"files": FileEntry}

    def __init__(self, ref: Any = None):
        self.id: str = ""
        self.formatId: str = ""
        self.name: str = ""
        self.parentMissing: bool = False
        self.parentPath: str = ""
        self.files: List[FileEntry] = []
        super().__init__(ref)

    def __iter__(self):
        for file in self.files:
            yield file

    def __str__(self):
        if len(self.files):
            return "<%s %a %s>" % (
                type(self).__name__,
                self.formatId,
                Tools.numberPlural("file", len(self.files)),
            )
        else:
            return "<%s>" % (type(self).__name__)

    @property
    @deprecated(details="Please use property 'formatId'")
    def parserId(self):
        return self.formatId

    @parserId.setter
    @deprecated(details="Please use property 'formatId'")
    def paserId(self, value):
        self.formatId = value


class DatasetMatch(SerializableClass):
    _typeMapper = {"datasets": MatchedDataset}

    def __init__(self, ref: Any = None):
        self.fromatId: str = ""
        self.parserName: str = ""
        self.datasets: List[MatchedDataset] = []
        super().__init__(ref)

    def __iter__(self):
        for dataset in self.datasets:
            yield dataset

    def __str__(self):
        if self.fromatId and len(self.datasets):
            return "<%s %a(%d)>" % (
                type(self).__name__,
                self.fromatId,
                len(self.datasets),
            )
        else:
            return "<%s>" % (type(self).__name__)

    @property
    @deprecated(details="Please use property 'formatId'")
    def parserId(self):
        return self.formatId

    @parserId.setter
    @deprecated(details="Please use property 'formatId'")
    def parserId(self, value):
        self.formatId = value


class MatchResult(SerializableClass):
    _typeMapper = {"matches": DatasetMatch, "missingFragments": FileFragment}

    def __init__(self, ref: Any = None):
        self.matches: List[DatasetMatch] = []
        self.missingFragments: List[FileFragment] = []
        super().__init__(ref)
