from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class ISoftDeletableRequest:
    includeSoftDeleted: Optional[bool] = None
    isSoftDeleted: Optional[bool] = None


class ISoftDeletable(IEntityInterface):
    _isDeleted: Optional[bool] = None

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = Tools.checkAndConvert(
            value, bool, "isDeleted", allowNone=True
        )
