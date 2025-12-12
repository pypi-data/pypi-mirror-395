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
from LOGS.Interfaces.ILockableEntity import ILockableEntityRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest


class ProjectSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
    ITypedEntitySortingOptions,
):
    DATASET_COUNT: Self = cast(Self, "DATASET_COUNT")
    INVENTORY_ITEM_COUNT: Self = cast(Self, "INVENTORY_ITEM_COUNT")
    LAB_NOTEBOOK_COUNT: Self = cast(Self, "LAB_NOTEBOOK_COUNT")
    SAMPLE_COUNT: Self = cast(Self, "SAMPLE_COUNT")


@dataclass
class ProjectRequestParameter(
    EntityRequestParameter[ProjectSortingOptions],
    IPermissionedEntityRequest,
    IUniqueEntityRequest,
    INamedEntityRequest,
    IOwnedEntityRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ILockableEntityRequest,
    ITypedEntityRequest,
):
    _orderByType: Type[ProjectSortingOptions] = field(
        default=ProjectSortingOptions, init=False
    )

    inventoryItemIds: Optional[List[int]] = None
    labNotebookIds: Optional[List[int]] = None
    personIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    currentUserHasAddPermission: Optional[bool] = None
