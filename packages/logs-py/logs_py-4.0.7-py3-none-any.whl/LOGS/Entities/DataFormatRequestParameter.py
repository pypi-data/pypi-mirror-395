from dataclasses import dataclass, field
from typing import List, Optional, Type

from LOGS.Entity.EntityRequestParameter import (
    DefaultSortingOptions,
    EntityRequestParameter,
)


@dataclass
class DataFormatRequestParameter(EntityRequestParameter[DefaultSortingOptions]):
    _orderByType: Type[DefaultSortingOptions] = field(
        default=DefaultSortingOptions, init=False
    )

    name: Optional[str] = None
    vendors: Optional[List[str]] = None
    vendors: Optional[List[str]] = None
    methods: Optional[List[str]] = None
    formats: Optional[List[str]] = None
    instruments: Optional[List[str]] = None
