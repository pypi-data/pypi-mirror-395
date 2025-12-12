from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union

from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.Signature import Signature, SignatureType


@dataclass
class ISignableEntityRequest:
    signedByIds: Optional[List[int]] = None
    notSignedByIds: Optional[List[int]] = None
    signedFrom: Optional[datetime] = None
    signedTo: Optional[datetime] = None
    isSigned: Optional[bool] = None
    signatureTypes: Optional[List["SignatureType"]] = None


class ISignableEntity(IEntityInterface):
    _signatures: Optional[List["Signature"]] = None
    _isSigned: Optional[bool] = None

    @property
    def signatures(self) -> Optional[List["Signature"]]:
        return self._signatures

    @signatures.setter
    def signatures(self, value: Optional[Union[List["Signature"], List[dict]]]):
        from LOGS.Entities.Signature import Signature
        from LOGS.Entity.ConnectedEntity import ConnectedEntity

        self._signatures = ConnectedEntity.checkListAndConvertWithConnection(
            value,
            Signature,
            "signatures",
            allowNone=True,
            connection=self._getEntityConnection(),
        )

    @property
    def isSigned(self) -> Optional[bool]:
        return self._isSigned

    @isSigned.setter
    def isSigned(self, value: Optional[bool]):
        self._isSigned = Tools.checkAndConvert(value, bool, "isSigned", allowNone=True)
