from dataclasses import dataclass, field
from typing import Optional, Type

from LOGS.Entity.EntityRequestParameter import (
    DefaultSortingOptions,
    EntityRequestParameter,
)


@dataclass
class MethodRequestParameter(EntityRequestParameter[DefaultSortingOptions]):
    _orderByType: Type[DefaultSortingOptions] = field(
        default=DefaultSortingOptions, init=False
    )

    name: Optional[str] = None
