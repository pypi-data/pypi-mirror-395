from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from LOGS.Entity.SerializableContent import SerializableClass

if TYPE_CHECKING:
    pass


class CustomFieldValuesSearchPredicate(Enum):
    AND = "AND"
    OR = "OR"


class CustomFieldSearchOperator(Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    STRING_CONTAINS = "STRING_CONTAINS"
    STRING_NOT_CONTAINS = "STRING_NOT_CONTAINS"
    IN_ = "IN_"
    NOT_IN = "NOT_IN"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    IS_NULL = "IS_NULL"
    IS_NOT_NULL = "IS_NOT_NULL"


@dataclass
class CustomFieldSearchQuery(SerializableClass):
    predicate: Optional[CustomFieldValuesSearchPredicate] = None
    left: Optional["CustomFieldSearchQuery"] = None
    right: Optional["CustomFieldSearchQuery"] = None
    customFieldId: Optional[int] = None
    operator: Optional[CustomFieldSearchOperator] = None
    value: Optional[Any] = None
