from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@dataclass
class IModificationRecordRequest:
    pass


class IModifiedOnRequest:
    modifiedFrom: Optional[datetime] = None
    modifiedTo: Optional[datetime] = None


class IModifiedByRequest:
    modifiedByIds: Optional[List[int]]


class IModifiedOn(IEntityInterface):
    _modifiedOn: Optional[datetime] = None

    @property
    def modifiedOn(self) -> Optional[datetime]:
        return self._modifiedOn

    @modifiedOn.setter
    def modifiedOn(self, value):
        self._modifiedOn = Tools.checkAndConvert(
            value, datetime, "modifiedOn", allowNone=True
        )


class IModifiedBy(IEntityInterface):
    _modifiedBy: Optional["PersonMinimal"] = None

    @property
    def modifiedBy(self) -> Optional["PersonMinimal"]:
        return self._modifiedBy

    @modifiedBy.setter
    def modifiedBy(self, value):
        self._modifiedBy = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "modifiedBy", connection=self._getEntityConnection()
        )


class IModificationRecord(IModifiedOn, IModifiedBy):
    pass
