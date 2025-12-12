from dataclasses import dataclass
from typing import List, Optional, Union
from uuid import UUID

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.Origin import Origin
from LOGS.Entities.OriginMinimal import OriginMinimal
from LOGS.Interfaces.IEntityInterface import IEntityInterface


@dataclass
class IUniqueEntityRequest:
    originIds: Optional[List[int]] = None


class IUniqueEntity(IEntityInterface):
    _uid: Optional[str] = None
    _origin: Optional[OriginMinimal] = None

    _foreignUid: Optional[UUID] = None
    _foreignOrigin: Optional[OriginMinimal] = None

    def setOrigin(
        self,
        uid: Optional[Union[str, UUID]] = None,
        origin: Optional[Union[Origin, OriginMinimal]] = None,
    ):
        self._foreignUid = Tools.checkAndConvert(
            uid, UUID, "setOrigin(uid)", allowNone=True
        )
        self._foreignOrigin = Tools.checkAndConvert(
            origin, OriginMinimal, "setOrigin(origin)", allowNone=True
        )

    def _originConverter(self, origin: Union[Origin, OriginMinimal]) -> OriginMinimal:
        if isinstance(origin, OriginMinimal):
            return origin
        if isinstance(origin, Origin):
            return OriginMinimal(name=origin.name, id=origin.id)
        return Tools.checkAndConvert(origin, OriginMinimal, allowNone=True)

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = Tools.checkAndConvert(
            value=value, fieldType=str, fieldName="uid", allowNone=True
        )

    @property
    def origin(self) -> Optional[OriginMinimal]:
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "origin", connection=self._getEntityConnection()
        )
