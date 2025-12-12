from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Type, Union
from uuid import UUID

from LOGS.Entity.EntityRequestParameter import (
    DefaultSortingOptions,
    EntityRequestParameter,
)


@dataclass
class EntitiesRequestParameter(EntityRequestParameter[DefaultSortingOptions]):
    _orderByType: Type[DefaultSortingOptions] = field(
        default=DefaultSortingOptions, init=False
    )

    uids: Optional[Sequence[Union[str, UUID]]] = None
    names: Optional[List[str]] = None
