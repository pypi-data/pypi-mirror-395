from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Type, Union
from uuid import UUID

from LOGS.Entity.EntityRequestParameter import (
    DefaultSortingOptions,
    EntityRequestParameter,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


@dataclass
class OriginRequestParameter(
    EntityRequestParameter[DefaultSortingOptions],
    INamedEntityRequest,
    IModificationRecordRequest,
    IEntryRecordRequest,
    IPermissionedEntityRequest,
):
    _orderByType: Type[DefaultSortingOptions] = field(
        default=DefaultSortingOptions, init=False
    )

    urls: Optional[List[str]] = None
    uids: Optional[Sequence[Union[UUID, str]]] = None
