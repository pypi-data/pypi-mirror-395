from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
)
from LOGS.Interfaces.ILockableEntity import ILockableEntityRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISignableEntity import ISignableEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest
from LOGS.Interfaces.IVersionedEntity import IVersionedEntityRequest


class LabNotebookEntrySortingOptions(
    IGenericEntitySortingOptions, IModificationRecordSortingOptions
):
    NAME: Self = cast(Self, "NAME")
    ENTRY_DATE: Self = cast(Self, "ENTRY_DATE")
    VERSION: Self = cast(Self, "VERSION")
    LAB_NOTEBOOK_ID: Self = cast(Self, "LAB_NOTEBOOK_ID")
    LAB_NOTEBOOK_NAME: Self = cast(Self, "LAB_NOTEBOOK_NAME")
    LAB_NOTEBOOK_EXPERIMENT_ID: Self = cast(Self, "LAB_NOTEBOOK_EXPERIMENT_ID")
    LAB_NOTEBOOK_EXPERIMENT_NAME: Self = cast(Self, "LAB_NOTEBOOK_EXPERIMENT_NAME")


@dataclass
class LabNotebookEntryRequestParameter(
    EntityRequestParameter[LabNotebookEntrySortingOptions],
    IPermissionedEntityRequest,
    IUniqueEntityRequest,
    INamedEntityRequest,
    IProjectBasedRequest,
    ILockableEntityRequest,
    ISignableEntityRequest,
    IVersionedEntityRequest,
):
    _orderByType: Type[LabNotebookEntrySortingOptions] = field(
        default=LabNotebookEntrySortingOptions, init=False
    )

    entryDateFrom: Optional[date] = None
    entryDateTo: Optional[date] = None
    labNotebookExperimentReferenceIds: Optional[List[int]] = None
    datasetReferenceIds: Optional[List[int]] = None
    attachmentReferenceIds: Optional[List[int]] = None
    personReferenceIds: Optional[List[int]] = None
    projectReferenceIds: Optional[List[int]] = None
    sampleReferenceIds: Optional[List[int]] = None
    inventoryItemReferenceIds: Optional[List[int]] = None
    labNotebookReferenceIds: Optional[List[int]] = None
    useFullTextSearch: Optional[bool] = None
    includeContent: Optional[bool] = None
