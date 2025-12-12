from dataclasses import dataclass, field
from typing import Type

from LOGS.Entity.EntityRequestParameter import (
    DefaultSortingOptions,
    EntityRequestParameter,
)
from LOGS.Interfaces.INamedEntity import INamedEntityRequest


@dataclass
class DataFormatInstrumentRequestParameter(
    EntityRequestParameter[DefaultSortingOptions], INamedEntityRequest
):
    _orderByType: Type[DefaultSortingOptions] = field(
        default=DefaultSortingOptions, init=False
    )
