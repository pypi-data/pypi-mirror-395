from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

from LOGS.Interfaces.ICustomFieldValue import ICustomFieldValue
from LOGS.Interfaces.ICustomSectionValue import ICustomSectionValue
from LOGS.Interfaces.ICustomValue import ICustomValue

if TYPE_CHECKING:
    pass


class ICustomTypeValue(ICustomValue):
    _id: Optional[int] = None
    _name: Optional[str] = None

    _fieldNames: List[str] = []
    _fieldTypes: Dict[str, Type[ICustomFieldValue]] = {}
    _fieldIds: Dict[int, str] = {}

    def __init__(
        self,
        ref=None,
    ):
        for fieldName in self._fieldNames:
            setattr(self, "_" + fieldName, self._fieldTypes[fieldName]())
        if not isinstance(ref, dict):
            ref = {"content": ref}
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
                if "type" not in c:
                    raise ValueError(f"Content item {i} is missing the 'type' field.")
                if c["type"] != "CustomTypeSection" or "content" not in c:
                    continue

                s = self.getSection(i)
                if s is not None:
                    s.override(c)

    def toDict(self) -> Dict[str, Any]:
        result = super().toDict()
        content = []
        for name in self._fieldNames:
            field = self.getSection(name)
            if field is not None:
                content.append(field.toDict() if hasattr(field, "toDict") else field)
        # print("content:", content)
        return cast(Any, content)

    def __str__(self):
        id = f" [ID: {self.id}]" if self.id else ""
        return f"<{type(self).__name__}{id}>"

    def _contentToString(self, indentation: int = 0, hideNone: bool = False) -> str:
        tab = self._indentationString * indentation
        s = ""
        for name in self._fieldNames:
            section = self.getSection(name)
            if not section and hideNone:
                continue
            content = ""
            if section is not None:
                content = section._contentToString(indentation + 1, hideNone=hideNone)
            if not content and hideNone:
                continue
            s += f"{tab}{name}:\n{content}"
        return s

    def _getFieldNameFromId(self, fieldId: str) -> str:
        if fieldId in self._fieldIds:
            return self._fieldIds[fieldId]
        return fieldId

    def getField(self, fieldNameOrId: str):
        fieldName = self._getFieldNameFromId(fieldNameOrId)

        if fieldName not in self._fieldNames:
            raise AttributeError(f"Unknown field '{type(self).__name__}.{fieldName}'.")
        return self.getSection(fieldName)

    def _getSectionByName(self, sectionName: str) -> Optional[ICustomSectionValue]:
        return getattr(self, "_" + sectionName)

    def getSection(
        self, sectionIndexOrFieldId: Union[str, int]
    ) -> Optional[ICustomSectionValue]:

        if isinstance(sectionIndexOrFieldId, int):
            if self.id is None:
                raise ValueError(f"Section with index {sectionIndexOrFieldId} unknown")
            fieldId = ICustomSectionValue._generateId(self.id, sectionIndexOrFieldId)
        else:
            fieldId = sectionIndexOrFieldId

        fieldName = self._getFieldNameFromId(fieldId)
        if fieldName not in self._fieldNames:
            raise AttributeError(
                f"Section with index or name '{sectionIndexOrFieldId}' unknown."
            )
        return self._getSectionByName(fieldName)

    def printFieldValues(self, hideNone: bool = False):

        s = f"{type(self).__name__}"

        customFields = self.customFields
        for field in customFields:
            if hideNone and (field.value is None or field.value == ""):
                continue
            s += f"\n{self._indentationString}{field.name} [{field.id}] = {field.value}"
        print(s)

    def customField(self, nameOrId) -> Optional[ICustomFieldValue]:
        for name in self._fieldNames:
            section = self._getSectionByName(name)
            if section is not None:
                field = section.customField(nameOrId)
                if field is not None:
                    return field
        return None

    @property
    def customFields(self) -> List[ICustomFieldValue]:
        result = []
        for name in self._fieldNames:
            section = self._getSectionByName(name)
            if section is not None:
                result.extend(section.customFields)
        return result

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def name(self) -> Optional[str]:
        return self._name
