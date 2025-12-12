from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@dataclass
class ILockableEntityRequest:
    lockedByIds: Optional[List[int]] = None
    lockedFrom: Optional[datetime] = None
    lockedTo: Optional[datetime] = None
    isLocked: Optional[bool] = None


class ILockableEntity(IEntityInterface):
    _lockedBy: Optional["PersonMinimal"] = None
    _lockedOn: Optional[datetime] = None
    _isLocked: Optional[bool] = None

    @property
    def lockedBy(self) -> Optional["PersonMinimal"]:
        return self._lockedBy

    @lockedBy.setter
    def lockedBy(self, value):
        self._lockedBy = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "lockedBy", self._getEntityConnection()
        )

    @property
    def lockedOn(self) -> Optional[datetime]:
        return self._lockedOn

    @lockedOn.setter
    def lockedOn(self, value: Optional[Union[datetime, dict]]):
        self._lockedOn = Tools.checkAndConvert(
            value, datetime, "lockedOn", allowNone=True
        )

    @property
    def isLocked(self) -> Optional[bool]:
        return self._isLocked

    @isLocked.setter
    def isLocked(self, value: Optional[bool]):
        self._isLocked = Tools.checkAndConvert(value, bool, "isLocked", allowNone=True)
