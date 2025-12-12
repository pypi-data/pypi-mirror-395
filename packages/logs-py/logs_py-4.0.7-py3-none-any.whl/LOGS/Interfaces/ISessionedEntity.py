from datetime import datetime
from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


class ISessionedEntity(IEntityInterface):
    _currentlyEditedBy: Optional["PersonMinimal"] = None
    _currentlyEditedSince: Optional[datetime] = None
    _publicSessionId: Optional[str] = None
    _isCurrentlyEdited: Optional[bool] = None

    @property
    def currentlyEditedBy(self) -> Optional["PersonMinimal"]:
        return self._currentlyEditedBy

    @currentlyEditedBy.setter
    def currentlyEditedBy(self, value):
        self._currentlyEditedBy = MinimalModelGenerator.MinimalFromSingle(
            value,
            "PersonMinimal",
            "currentlyEditedBy",
            connection=self._getEntityConnection(),
        )

    @property
    def currentlyEditedSince(self) -> Optional[datetime]:
        return self._currentlyEditedSince

    @currentlyEditedSince.setter
    def currentlyEditedSince(self, value):
        self._currentlyEditedSince = Tools.checkAndConvert(
            value, datetime, "currentlyEditedSince", allowNone=True
        )

    @property
    def publicSessionId(self) -> Optional[str]:
        return self._publicSessionId

    @publicSessionId.setter
    def publicSessionId(self, value):
        self._publicSessionId = Tools.checkAndConvert(
            value, str, "publicSessionId", allowNone=True
        )

    @property
    def isCurrentlyEdited(self) -> Optional[bool]:
        return self._isCurrentlyEdited

    @isCurrentlyEdited.setter
    def isCurrentlyEdited(self, value):
        self._isCurrentlyEdited = Tools.checkAndConvert(
            value, bool, "isCurrentlyEdited", allowNone=True
        )
