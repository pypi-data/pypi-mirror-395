from dataclasses import dataclass, field
from typing import Optional, Type, cast

from typing_extensions import Self

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    INamedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class RoleSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
):
    IS_INTERNAL: Self = cast(Self, "IS_INTERNAL")


@dataclass
class RoleRequestParameter(
    EntityRequestParameter[RoleSortingOptions],
    IEntryRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):
    _orderByType: Type[RoleSortingOptions] = field(
        default=RoleSortingOptions, init=False
    )

    name: Optional[str] = None
    roleId: Optional[str] = None
    includeInternals: Optional[bool] = None
