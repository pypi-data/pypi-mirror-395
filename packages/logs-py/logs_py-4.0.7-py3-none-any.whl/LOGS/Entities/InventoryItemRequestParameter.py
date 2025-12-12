from dataclasses import dataclass, field
from typing import List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    INamedEntitySortingOptions,
    ITypedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.IHierarchicalEntity import IHierarchicalEntityRequest
from LOGS.Interfaces.ILockableEntity import ILockableEntityRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISignableEntity import ISignableEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest


class InventoryItemsSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
    ITypedEntitySortingOptions,
):
    INVENTORY_NAME: Self = cast(Self, "INVENTORY_NAME")
    NUMBER_OF_ITEMS: Self = cast(Self, "NUMBER_OF_ITEMS")
    LAYOUT: Self = cast(Self, "LAYOUT")


@dataclass
class InventoryItemRequestParameter(
    EntityRequestParameter[InventoryItemsSortingOptions],
    IPaginationRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    IHierarchicalEntityRequest,
    IProjectBasedRequest,
    ITypedEntityRequest,
    ILockableEntityRequest,
    ISignableEntityRequest,
):
    _orderByType: Type[InventoryItemsSortingOptions] = field(
        default=InventoryItemsSortingOptions, init=False
    )

    childrenOfParentIds: Optional[List[int]] = None
    descendantsOfIds: Optional[List[int]] = None
    excludeHierarchyChildren: Optional[bool] = None
    isHierarchyRoot: Optional[bool] = None
    inventoryItemIds: Optional[List[int]] = None
