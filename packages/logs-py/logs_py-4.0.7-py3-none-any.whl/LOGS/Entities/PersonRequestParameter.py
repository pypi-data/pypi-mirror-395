from dataclasses import dataclass, field
from typing import List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    ITypedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.ILockableEntity import ILockableEntityRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest


class PersonSortingOptions(
    IGenericEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
    ITypedEntitySortingOptions,
):
    NAME: Self = cast(Self, "NAME")
    LOGIN: Self = cast(Self, "LOGIN")
    IS_SYSTEM_USER: Self = cast(Self, "IS_SYSTEM_USER")
    LAST_NAME: Self = cast(Self, "LAST_NAME")
    FIRST_NAME: Self = cast(Self, "FIRST_NAME")


@dataclass
class PersonRequestParameter(
    EntityRequestParameter[PersonSortingOptions],
    IPermissionedEntityRequest,
    IUniqueEntityRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    ILockableEntityRequest,
    ITypedEntityRequest,
):
    _orderByType: Type[PersonSortingOptions] = field(
        default=PersonSortingOptions, init=False
    )

    isLocalUser: Optional[List[bool]] = None
    roleIds: Optional[List[int]] = None
    hasAccount: Optional[bool] = None
    isAccountEnabled: Optional[bool] = None
    includeSystemUsers: Optional[bool] = None
    logins: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    firstNames: Optional[List[str]] = None
    lastNames: Optional[List[str]] = None
