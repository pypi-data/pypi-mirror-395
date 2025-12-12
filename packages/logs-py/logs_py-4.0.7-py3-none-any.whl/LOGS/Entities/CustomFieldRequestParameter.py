from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entities.CustomFieldModels import (
    CustomFieldDataType,
    CustomFieldValuesSearchPredicate,
)
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
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class CustomFieldSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
):
    DATATYPE: Self = cast(Self, "DATATYPE")


@dataclass
class CustomFieldValuesSearchParameters:
    values: Optional[List[Any]] = None
    dataType: Optional[CustomFieldDataType] = None
    customFieldIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    personIds: Optional[List[int]] = None
    inventoryIds: Optional[List[int]] = None
    facilityIds: Optional[List[int]] = None
    predicate: Optional[CustomFieldValuesSearchPredicate] = None


@dataclass
class ICustomFieldValuesSearchRequest:
    customFieldValues: Optional[List[CustomFieldValuesSearchParameters]] = None


@dataclass
class CustomFieldRequestParameter(
    EntityRequestParameter[CustomFieldSortingOptions],
    IPaginationRequest,
    IPermissionedEntityRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ICustomFieldValuesSearchRequest,
    IOwnedEntityRequest,
    INamedEntityRequest,
):
    _orderByType: Type[CustomFieldSortingOptions] = field(
        default=CustomFieldSortingOptions, init=False
    )

    dataTypes: Optional[List[CustomFieldDataType]] = None
    customFieldValues: Optional[List[CustomFieldValuesSearchParameters]] = None
