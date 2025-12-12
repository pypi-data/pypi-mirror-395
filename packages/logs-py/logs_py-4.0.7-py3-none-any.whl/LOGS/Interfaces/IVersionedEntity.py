from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, Union

from LOGS.Auxiliary import Tools
from LOGS.Interfaces.IEntryRecord import IEntryRecord, IEntryRecordRequest
from LOGS.Interfaces.IModificationRecord import (
    IModificationRecord,
    IModificationRecordRequest,
)
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable, ISoftDeletableRequest

if TYPE_CHECKING:
    pass

_idType = TypeVar("_idType", bound=Union[int, str])


@dataclass
class IVersionedEntityRequest(
    Generic[_idType],
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
):
    originalIds: Optional[List[_idType]] = None
    versionIds: Optional[List[int]] = None
    versions: Optional[List[int]] = None


class IVersionedEntity(IEntryRecord, IModificationRecord, ISoftDeletable):
    _version: Optional[int] = None

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = Tools.checkAndConvert(value, int, "version", allowNone=True)
