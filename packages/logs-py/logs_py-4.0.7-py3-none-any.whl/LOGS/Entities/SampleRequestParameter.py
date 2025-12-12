from dataclasses import dataclass, field
from typing import Type, cast

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
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISignableEntity import ISignableEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest


class SampleSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IModificationRecordSortingOptions,
    IEntryRecordSortingOptions,
    ITypedEntitySortingOptions,
):
    OWNER: Self = cast(Self, "OWNER")


@dataclass
class SampleRequestParameter(
    EntityRequestParameter[SampleSortingOptions],
    IPermissionedEntityRequest,
    IUniqueEntityRequest,
    INamedEntityRequest,
    IOwnedEntityRequest,
    IProjectBasedRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    ILockableEntityRequest,
    ISignableEntityRequest,
    ITypedEntityRequest,
):
    _orderByType: Type[SampleSortingOptions] = field(
        default=SampleSortingOptions, init=False
    )
