from datetime import datetime
from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entities.PersonMinimal import PersonMinimal
from LOGS.Entity.Entity import Entity

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal

from enum import Enum


class SignatureType(Enum):
    Unknown = "Unknown"
    Contributor = "Contributor"
    Reviewer = "Reviewer"


class Signature(Entity):
    _signedBy: Optional["PersonMinimal"] = None
    _timestamp: Optional[datetime] = None
    _signatureType: Optional[SignatureType] = None
    _comment: Optional[str] = None

    @property
    def signedBy(self) -> Optional["PersonMinimal"]:
        return self._signedBy

    @signedBy.setter
    def signedBy(self, value):
        self._signedBy = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "signedBy", self._getConnection()
        )

    @property
    def timestamp(self) -> Optional[datetime]:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Optional[datetime]):
        self._timestamp = self.checkAndConvertNullable(value, datetime, "timestamp")

    @property
    def signatureType(self) -> Optional[SignatureType]:
        return self._signatureType

    @signatureType.setter
    def signatureType(self, value: Optional[SignatureType]):
        self._signatureType = self.checkAndConvertNullable(
            value, SignatureType, "signatureType"
        )

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @comment.setter
    def comment(self, value: Optional[str]):
        self._comment = self.checkAndConvertNullable(value, str, "comment")
