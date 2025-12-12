from typing import Any, Dict, List, Optional, cast

from typing_extensions import Self

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableClass


class IBaseEntityOrderBy(SerializableClass):
    _value: Optional[str] = None
    _fieldNames: List[str] = []

    def fromString(self, ref: str):
        fieldNames = self._getAttrList()
        if ref not in fieldNames:
            raise ValueError(
                f"Invalid value '{ref}' for {self.__class__.__name__}. (Expected one of {Tools.eclipsesJoin(', ', fieldNames, 5)})"
            )
        self._value = ref

    def listOptions(self) -> List[str]:
        return self._getAttrList()

    def toDict(self) -> Dict[str, Any]:
        if self._value is None:
            return cast(Dict[str, None], None)
        return cast(Dict[str, None], self._value)

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        return str(self.toDict())

    CUSTOM_FIELD: Self = cast(Self, "CUSTOM_FIELD")


class IGenericEntitySortingOptions(IBaseEntityOrderBy):
    ID: Self = cast(Self, "ID")


class INamedEntitySortingOptions(IBaseEntityOrderBy):
    NAME: Self = cast(Self, "NAME")


class IEntryRecordSortingOptions(IBaseEntityOrderBy):
    ENTERED_BY: Self = cast(Self, "ENTERED_BY")
    ENTERED_ON: Self = cast(Self, "ENTERED_ON")


class IModificationRecordSortingOptions(IBaseEntityOrderBy):
    MODIFIED_BY: Self = cast(Self, "MODIFIED_BY")
    MODIFIED_ON: Self = cast(Self, "MODIFIED_ON")


class ITypedEntitySortingOptions(IBaseEntityOrderBy):
    CUSTOM_TYPE: Self = cast(Self, "CUSTOM_TYPE")
    CUSTOM_FIELD: Self = cast(Self, "CUSTOM_FIELD")
