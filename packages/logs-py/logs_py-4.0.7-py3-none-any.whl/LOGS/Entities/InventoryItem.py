from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IHierarchicalEntity import IHierarchicalEntity
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ISignableEntity import ISignableEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.InventoryItemMinimal import InventoryItemMinimal


@Endpoint("inventory_items")
class InventoryItem(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    IEntryRecord,
    IModificationRecord,
    ISoftDeletable,
    ILockableEntity,
    IGenericPermissionEntity,
    ITypedEntity,
    IProjectBased,
    IHierarchicalEntity,
    ISignableEntity,
):

    _rootCustomType: Optional["InventoryItemMinimal"] = None
    _isRootItem: Optional[bool] = None
    _isHierarchyItem: Optional[bool] = None

    _isDeletedViaHierarchy: Optional[bool] = None
    _isLockedViaHierarchy: Optional[bool] = None
    _isSignedViaHierarchy: Optional[bool] = None

    @property
    def rootCustomType(self) -> Optional["InventoryItemMinimal"]:
        return self._rootCustomType

    @rootCustomType.setter
    def rootCustomType(self, value):
        self._rootCustomType = MinimalModelGenerator.MinimalFromSingle(
            value, "InventoryItemMinimal", "rootCustomType", self._getConnection()
        )

    @property
    def isRootItem(self) -> Optional[bool]:
        return self._isRootItem

    @isRootItem.setter
    def isRootItem(self, value):
        self._isRootItem = self.checkAndConvertNullable(value, bool, "isRootItem")

    @property
    def isHierarchyItem(self) -> Optional[bool]:
        return self._isHierarchyItem

    @isHierarchyItem.setter
    def isHierarchyItem(self, value):
        self._isHierarchyItem = self.checkAndConvertNullable(
            value, bool, "isHierarchyItem"
        )

    @property
    def isDeletedViaHierarchy(self) -> Optional[bool]:
        return self._isDeletedViaHierarchy

    @isDeletedViaHierarchy.setter
    def isDeletedViaHierarchy(self, value):
        self._isDeletedViaHierarchy = self.checkAndConvertNullable(
            value, bool, "isDeletedViaHierarchy"
        )

    @property
    def isLockedViaHierarchy(self) -> Optional[bool]:
        return self._isLockedViaHierarchy

    @isLockedViaHierarchy.setter
    def isLockedViaHierarchy(self, value):
        self._isLockedViaHierarchy = self.checkAndConvertNullable(
            value, bool, "isLockedViaHierarchy"
        )

    @property
    def isSignedViaHierarchy(self) -> Optional[bool]:
        return self._isSignedViaHierarchy

    @isSignedViaHierarchy.setter
    def isSignedViaHierarchy(self, value):
        self._isSignedViaHierarchy = self.checkAndConvertNullable(
            value, bool, "isSignedViaHierarchy"
        )
