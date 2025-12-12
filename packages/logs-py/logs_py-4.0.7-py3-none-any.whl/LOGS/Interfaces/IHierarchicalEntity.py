from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.InventoryItemMinimal import InventoryItemMinimal


@dataclass
class IHierarchicalEntityRequest:
    childrenOfParentIds: Optional[List[int]] = None
    descendantsOfIds: Optional[List[int]] = None
    excludeHierarchyChildren: Optional[bool] = None
    isHierarchyRoot: Optional[bool] = None


class IHierarchicalEntity(IEntityInterface):
    _ancestors: Optional[List["InventoryItemMinimal"]] = None
    _parent: Optional["InventoryItemMinimal"] = None

    @property
    def ancestors(self) -> Optional[List["InventoryItemMinimal"]]:
        return self._ancestors

    @ancestors.setter
    def ancestors(self, value):
        self._ancestors = MinimalModelGenerator.MinimalFromList(
            value, "InventoryItemMinimal", "ancestors", self._getEntityConnection()
        )

    @property
    def parent(self) -> Optional["InventoryItemMinimal"]:
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = MinimalModelGenerator.MinimalFromSingle(
            value, "InventoryItemMinimal", "parent", self._getEntityConnection()
        )
