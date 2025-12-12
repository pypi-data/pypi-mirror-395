from typing import TYPE_CHECKING, cast

from LOGS.Auxiliary.Exceptions import IllegalFieldValueException
from LOGS.Entities.CustomFieldModels import CustomFieldValueType
from LOGS.Entity.SerializableContent import SerializableContent

if TYPE_CHECKING:
    pass


class ICustomValue(SerializableContent):
    _indentationString: str = "  "


class ITypedCustomValue(ICustomValue):
    _type: CustomFieldValueType = cast(CustomFieldValueType, None)

    @property
    def type(self) -> CustomFieldValueType:
        return self._type

    @type.setter
    def type(self, value):
        value = self.checkAndConvert(value, CustomFieldValueType, "type")
        if value != self._type:
            raise IllegalFieldValueException(
                self, "type", value, f"Only value '{self._type}' allowed."
            )
