from enum import Enum
from typing import Generic, Optional, Type, TypeVar, cast

from LOGS.Entity.IGenericEntityOrderBy import IBaseEntityOrderBy
from LOGS.Entity.SerializableContent import SerializableContent

_ORDER = TypeVar("_ORDER", bound=IBaseEntityOrderBy)


class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


_builtInProperty = property  # this avoids a name conflict between the @property decorator and field property


class EntitySortBy(Generic[_ORDER], SerializableContent):
    _orderByType: Type[_ORDER] = cast(Type[_ORDER], None)

    _property: Optional[_ORDER] = None
    _sortDirection: SortDirection = SortDirection.ASC
    _customFieldId: Optional[int] = None

    def __init__(
        self,
        orderByType: Type[_ORDER],
        property: _ORDER,
        sortDirection: SortDirection = SortDirection.ASC,
        customFieldId: Optional[int] = None,
    ):
        super().__init__()

        self._orderByType = orderByType
        if not self._orderByType:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not define an order type."
            )

        self.property = property
        self.sortDirection = sortDirection
        self.customFieldId = customFieldId

    @_builtInProperty
    def property(self) -> Optional[_ORDER]:
        return self._property

    @property.setter
    def property(self, value):

        self._property = self.checkAndConvert(value, self._orderByType, "property")

    @_builtInProperty
    def sortDirection(self) -> SortDirection:
        return self._sortDirection

    @sortDirection.setter
    def sortDirection(self, value: SortDirection):
        self._sortDirection = self.checkAndConvert(
            value, SortDirection, "sortDirection"
        )

    @_builtInProperty
    def customFieldId(self) -> Optional[int]:
        return self._customFieldId

    @customFieldId.setter
    def customFieldId(self, value: Optional[int]):
        self._customFieldId = self.checkAndConvertNullable(value, int, "customFieldId")
