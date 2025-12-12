from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@dataclass
class IEnteredOnRequest:
    enteredFrom: Optional[datetime] = None
    enteredTo: Optional[datetime] = None


class IEnteredByRequest:
    createdByIds: Optional[List[int]]


@dataclass
class IEntryRecordRequest(IEnteredOnRequest, IEnteredByRequest):
    pass


class IEnteredOn(IEntityInterface):
    _enteredOn: Optional[datetime] = None

    @property
    def enteredOn(self) -> Optional[datetime]:
        return self._enteredOn

    @enteredOn.setter
    def enteredOn(self, value):
        self._enteredOn = Tools.checkAndConvert(
            value, datetime, "enteredOn", allowNone=True
        )


class IEnteredBy(IEntityInterface):
    _enteredBy: Optional["PersonMinimal"] = None

    @property
    def enteredBy(self) -> Optional["PersonMinimal"]:
        return self._enteredBy

    @enteredBy.setter
    def enteredBy(self, value):
        self._enteredBy = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "enteredBy", connection=self._getEntityConnection()
        )


class IEntryRecord(IEnteredOn, IEnteredBy):
    pass
