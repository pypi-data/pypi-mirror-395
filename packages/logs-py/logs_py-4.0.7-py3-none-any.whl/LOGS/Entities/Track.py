from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union, cast

from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.TrackData import TrackData
from LOGS.Entities.TrackSettings import TrackSettings
from LOGS.Entity.EntityWithStrId import EntityWithStrId

TrackTypes = Literal[
    "nucleotide_sequence",
    "image",
    "matrix_real",
    "pdf",
    "table",
    "XY_complex",
    "XY_real",
]

_T = TypeVar("_T", bound=Union[Datatrack, Dict[str, Datatrack]])


class Track(Generic[_T], EntityWithStrId):
    _name: Optional[str] = None
    _type: Optional[TrackTypes] = None
    _tags: Optional[List[str]] = None
    _settings: TrackSettings = TrackSettings()
    _dataIds: Optional[dict] = None
    _datatracks: Optional[_T] = None

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "data" in ref:
                self._dataIds = self.checkAndConvertNullable(ref["data"], dict)
                ref["data"] = None

        super().fromDict(ref)

    def toDict(self) -> Dict[str, Any]:
        d = super().toDict()
        if isinstance(self.datatracks, TrackData):
            d["data"] = self.datatracks.toData()
        return d

    def __str__(self):
        s = (" name:'%s'" % getattr(self, "name")) if hasattr(self, "name") else ""
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)

    def _fetchData(self):
        if isinstance(self.datatracks, dict):
            for t in self.datatracks.values():
                t.fetchFull()

    def fetchFull(self):
        self._fetchData()

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def type(self) -> Optional[TrackTypes]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = cast(TrackTypes, self.checkAndConvertNullable(value, str, "type"))

    @property
    def tags(self) -> Optional[List[str]]:
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = self.checkListAndConvertNullable(value, str, "tags")

    @property
    def settings(self) -> TrackSettings:
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = self.checkAndConvert(value, TrackSettings, "settings")

    @property
    def datatracks(self) -> Optional[_T]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = cast(Any, self.checkAndConvertNullable(value, dict, "data"))
