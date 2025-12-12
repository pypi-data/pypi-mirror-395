from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from LOGS.Entity.EntitySortBy import EntitySortBy, SortDirection
from LOGS.Entity.IGenericEntityOrderBy import (
    IBaseEntityOrderBy,
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
)
from LOGS.Entity.SerializableContent import SerializableClass
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest


class DefaultSortingOptions(IGenericEntitySortingOptions, INamedEntitySortingOptions):
    pass


_Sorting = TypeVar("_Sorting", bound=IBaseEntityOrderBy)


@dataclass
class EntityRequestParameter(Generic[_Sorting], SerializableClass, IPaginationRequest):
    _orderByType: Type[_Sorting] = field(default=cast(Type[_Sorting], None), init=False)

    _getOrderbyType: Callable[[], Type[_Sorting]] = field(
        default=lambda: cast(Type[_Sorting], None), init=False
    )

    excludeIds: Optional[Union[List[int], List[str]]] = None
    searchTerm: Optional[str] = None
    ids: Optional[Union[List[int], List[str]]] = None
    includeCount: Optional[bool] = None
    sortBy: Optional[
        Union[
            List[
                Union[
                    Tuple[_Sorting, SortDirection],
                    Tuple[int, SortDirection],
                    _Sorting,
                    int,
                ]
            ],
            _Sorting,
            int,
        ]
    ] = None

    def __post_init__(self):
        orderByType = self.__class__._orderByType
        if type(self) is not EntityRequestParameter and not orderByType:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not define an order type."
            )

        if self.sortBy:
            if not isinstance(self.sortBy, list):
                self.sortBy = [self.sortBy]

            convertedSortBy: List[EntitySortBy[_Sorting]] = []
            for i, t in enumerate(self.sortBy):
                if not isinstance(t, tuple):
                    t = (t, SortDirection.ASC)

                if isinstance(t[0], int):
                    customFieldId = t[0]
                    property = orderByType.CUSTOM_FIELD
                elif isinstance(t[0], (orderByType, str)):
                    customFieldId = None
                    property = self.checkAndConvert(
                        t[0], orderByType, f"sortBy[{i}][0]"
                    )
                else:
                    raise TypeError(
                        f"Invalid type '{type(t[0]).__name__}' for sortBy[{i}][0]. (Expected int or {orderByType.__name__})"
                    )

                if len(t) > 1:
                    direction = self.checkAndConvert(
                        t[1], SortDirection, f"sortBy[{i}][1]"
                    )
                else:
                    direction = SortDirection.ASC

                convertedSortBy.append(
                    EntitySortBy[_Sorting](
                        orderByType=orderByType,
                        property=property,
                        sortDirection=direction,
                        customFieldId=customFieldId,
                    )
                )

            self.sortBy = cast(Any, convertedSortBy)
