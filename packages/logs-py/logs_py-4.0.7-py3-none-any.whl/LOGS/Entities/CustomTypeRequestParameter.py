from dataclasses import dataclass, field
from typing import List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entities.CustomFieldModels import CustomTypeEntityType
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    INamedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest


class CustomTypeSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
):
    NUMBER_OF_ITEMS: Self = cast(Self, "NUMBER_OF_ITEMS")
    INVENTORY_NAME: Self = cast(Self, "INVENTORY_NAME")
    LAYOUT: Self = cast(Self, "LAYOUT")


@dataclass
class CustomTypeRequestParameter(
    EntityRequestParameter[CustomTypeSortingOptions],
    IPaginationRequest,
    IPermissionedEntityRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    INamedEntityRequest,
):
    _orderByType: Type[CustomTypeSortingOptions] = field(
        default=CustomTypeSortingOptions, init=False
    )

    excludeDisabled: Optional[bool] = None
    isEnabled: Optional[bool] = None
    customFieldIds: Optional[List[int]] = None
    entityTypes: Optional[List[CustomTypeEntityType]] = None
    extendSearchToInventoryItems: Optional[bool] = None
    parentTypeIds: Optional[List[int]] = None
    hasRestrictedAddPermission: Optional[bool] = None
    hasRestrictedEditPermission: Optional[bool] = None
    hasRestrictedReadPermission: Optional[bool] = None
    rootHierarchyIds: Optional[List[int]] = None
    isInventory: Optional[bool] = None
    isHierarchyRoot: Optional[bool] = None
    inventoryNames: Optional[List[str]] = None
    excludeNonInventories: Optional[bool] = None
