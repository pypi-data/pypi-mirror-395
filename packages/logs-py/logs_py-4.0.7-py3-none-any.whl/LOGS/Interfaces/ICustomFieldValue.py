import re
from typing import TYPE_CHECKING, Any, Optional, cast

from LOGS.Auxiliary.CustomFieldValueTypeChecker import CustomFieldValueTypeChecker
from LOGS.Auxiliary.Exceptions import EntityNotConnectedException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.CustomFieldModels import CustomFieldDataType, CustomFieldValueType
from LOGS.Interfaces.ICustomValue import ITypedCustomValue
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity


class ICustomFieldValue(ITypedCustomValue):
    _type: CustomFieldValueType = CustomFieldValueType.CustomField
    _valueTypeChecker: CustomFieldValueTypeChecker = cast(
        CustomFieldValueTypeChecker, None
    )
    _newLineRe = re.compile(r"[\n\r\t\b\f]+")
    _connection: Optional[LOGSConnection] = None

    _id: Optional[int] = None
    _dataType: CustomFieldDataType
    _value: Optional[Any] = None
    _name: Optional[str] = None

    def __init__(self, ref=None, dataType: Optional[CustomFieldDataType] = None):
        if not dataType:
            raise Exception("Data type is not set")
        self._dataType = dataType
        self._setTypeChecker()
        super().__init__(ref)

    def _getConnection(self):
        if not self._connection:
            raise EntityNotConnectedException(cast("ConnectedEntity", self))
        return self._connection

    def _setTypeChecker(self):
        self._valueTypeChecker = CustomFieldValueTypeChecker(
            self._dataType, self._getConnection()
        )

    def _contentToString(self) -> str:
        if self._valueTypeChecker._isArrayType:
            v = [str(f) for f in self.value] if self.value is not None else []
            t = ", ".join(v)
        else:
            t = str(self.value) if self.value is not None else ""
        t = self._newLineRe.sub(" ", t)
        return Tools.truncString(t, 100)

    def __str__(self):
        id = f" [{'' + self._dataType.name + ']' if self._dataType else ''}{' ID:' + str(self.id) if self.id else ''}"
        return f"<{type(self).__name__}{id}>"

    @property
    def identifier(self):
        name = (
            f" '{getattr(self, 'name')}'"
            if hasattr(self, "name") and getattr(self, "name")
            else ""
        )
        return "%s(id:%s)%s" % (
            type(self).__name__,
            str(self.id),
            name,
        )

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def dataType(self) -> Optional[CustomFieldDataType]:
        return self._dataType

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, value):
        if not self._dataType:
            raise Exception("Data type is not set")

        self._value = self._valueTypeChecker.checkAndConvert(value, type(self).__name__)

    @property
    def name(self) -> Optional[str]:
        return self._name
