from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.CustomFieldModels import CustomFieldValueType
from LOGS.Interfaces.ICustomFieldValue import ICustomFieldValue
from LOGS.Interfaces.ICustomValue import ITypedCustomValue

if TYPE_CHECKING:
    pass


class ICustomSectionValue(ITypedCustomValue):
    _noSerialize: List[str] = ["fieldNames"]

    _type: CustomFieldValueType = CustomFieldValueType.CustomTypeSection
    _customTypeId: int = cast(int, None)
    _sectionIndex: int = cast(int, None)

    _fieldNames: List[str] = []
    _fieldTypes: Dict[str, Type[ICustomFieldValue]] = {}
    _fieldIds: Dict[int, str] = {}
    _name: Optional[str] = None

    def __init__(self, ref=None):
        for fieldName in self._fieldNames:
            setattr(self, "_" + fieldName, self._fieldTypes[fieldName]())
        super().__init__(ref)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict) and "content" in ref:
            content = ref["content"]
            del ref["content"]

        super().fromDict(ref)

        if content is not None:
            if not isinstance(content, list):
                raise ValueError(
                    f"Invalid content format. (Expected a 'list' got '{type(content).__name__}')"
                )
            for i, c in enumerate(content):
                if not isinstance(c, dict):
                    raise ValueError(
                        f"Invalid content item {i} format. (Expected a 'dict' got '{type(c).__name__}')"
                    )
                if "value" not in c:
                    continue
                if "id" not in c:
                    raise ValueError(f"Content item {i} is missing the 'id' field.")
                fieldId = Tools.checkAndConvert(
                    c["id"], int, f"content[{i}].id", allowNone=False
                )
                self.setField(fieldId, c["value"])

    def toDict(self) -> Dict[str, Any]:
        result = super().toDict()
        content = []
        for name in self._fieldNames:
            field = self.getCustomField(name)
            if field is not None:
                content.append(field.toDict() if hasattr(field, "toDict") else field)
        result["content"] = content
        return result

    @classmethod
    def _generateId(cls, customTypeId: int, sectionIndex: int):
        return f"{customTypeId}.{sectionIndex}"

    def _getFieldNameFromId(self, fieldId: int) -> str:
        if fieldId not in self._fieldIds:
            raise AttributeError(f"Unknown field ID '{type(self).__name__}.{fieldId}'.")
        return self._fieldIds[fieldId]

    def setField(self, fieldNameOrId: Union[str, int], value):
        fieldName = (
            self._getFieldNameFromId(fieldNameOrId)
            if isinstance(fieldNameOrId, int)
            else fieldNameOrId
        )

        if fieldName not in self._fieldNames:
            raise AttributeError(f"Unknown field '{type(self).__name__}.{fieldName}'.")
        f = self.getCustomField(fieldName)
        if f is not None:
            f.value = value

    def getField(self, fieldNameOrId: Union[str, int]):
        fieldName = (
            self._getFieldNameFromId(fieldNameOrId)
            if isinstance(fieldNameOrId, int)
            else fieldNameOrId
        )

        if fieldName not in self._fieldNames:
            raise AttributeError(f"Unknown field '{type(self).__name__}.{fieldName}'.")
        f = self.getCustomField(fieldName)
        return f.value if f is not None else None

    def _getCustomFieldByName(self, fieldName: str) -> Optional[ICustomFieldValue]:
        return getattr(self, "_" + fieldName)

    def getCustomField(self, fieldName: str) -> Optional[ICustomFieldValue]:
        if fieldName not in self._fieldNames:
            raise AttributeError(
                f"Unknown custom field '{type(self).__name__}.{fieldName}'."
            )
        return self._getCustomFieldByName(fieldName)

    def _contentToString(self, indentation: int = 0, hideNone: bool = False) -> str:
        s = ""
        for name in self._fieldNames:
            field = self.getCustomField(name)
            if field is not None:
                content = field._contentToString()
                if not content and hideNone:
                    continue
                s += f"{self._indentationString * indentation}{name} = {content}\n"
        return s

    def __str__(self):
        id1 = f"typeID:{self._customTypeId}" if self._customTypeId is not None else ""
        id2 = f"index:{self._sectionIndex}" if self._sectionIndex is not None else ""
        id = f"{id1}{' ' if id2 else ''}{id2}; " if id1 or id2 else ""
        return f"<{type(self).__name__} [{id}{Tools.numberPlural('field' , len(self._fieldNames))}]>"

    def customField(self, nameOrId) -> Optional[ICustomFieldValue]:
        for name in self._fieldNames:
            value = self._getCustomFieldByName(name)
            if isinstance(nameOrId, int):
                if value is not None and value.id == nameOrId:
                    return value
            else:
                if value is not None and value.name == str(nameOrId):
                    return value

        return None

    @classmethod
    def getId(cls) -> str:
        return cls._generateId(cls._customTypeId, cls._sectionIndex)

    @property
    def customFields(self) -> List[ICustomFieldValue]:
        result = []
        for name in self._fieldNames:
            value = self._getCustomFieldByName(name)
            if value is not None:
                result.append(value)
        return result

    @property
    def fieldNames(self) -> List[str]:
        return self._fieldNames

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")
