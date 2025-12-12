from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class IHierarchyTypeRequest:
    childrenOfParentIds: Optional[List[int]] = None
    descendantsOfIds: Optional[List[int]] = None
    isRoot: Optional[List[bool]] = None


class IHierarchyType(IEntityInterface):
    _inventoryName: Optional[str]
    _isHierarchyRoot: Optional[bool]
    _rootHierarchy: Optional[EntityMinimalWithIntId]
    _parentTypes: Optional[List[EntityMinimalWithIntId]]

    @property
    def inventoryName(self) -> Optional[str]:
        return self._inventoryName

    @inventoryName.setter
    def inventoryName(self, value):
        self._inventoryName = Tools.checkAndConvert(
            value, str, "inventoryName", allowNone=True
        )

    @property
    def isHierarchyRoot(self) -> Optional[bool]:
        return self._isHierarchyRoot

    @isHierarchyRoot.setter
    def isHierarchyRoot(self, value):
        self._isHierarchyRoot = Tools.checkAndConvert(
            value, bool, "isHierarchyRoot", allowNone=True
        )

    @property
    def rootHierarchy(self) -> Optional[EntityMinimalWithIntId]:
        return self._rootHierarchy

    @rootHierarchy.setter
    def rootHierarchy(self, value):
        self._rootHierarchy = Tools.checkAndConvert(
            value, EntityMinimalWithIntId, "rootHierarchy", allowNone=True
        )

    @property
    def parentTypes(self) -> Optional[List[EntityMinimalWithIntId]]:
        return self._parentTypes

    @parentTypes.setter
    def parentTypes(self, value):
        self._parentTypes = Tools.checkListAndConvert(
            value, EntityMinimalWithIntId, "parentTypes", allowNone=True
        )
