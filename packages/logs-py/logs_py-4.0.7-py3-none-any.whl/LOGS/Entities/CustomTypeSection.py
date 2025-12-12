from typing import List, Optional

from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.ILiteraryTypedEntity import ILiteraryTypedEntity
from LOGS.Entity.ConnectedEntity import ConnectedEntity


class CustomTypeSection(ConnectedEntity, ILiteraryTypedEntity):
    _name: Optional[str] = None
    _isFolded: Optional[bool] = None
    _isHeadless: Optional[bool] = None
    _customFields: Optional[List[CustomField]] = None

    _type = "CustomTypeSection"

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        bak = self._noSerialize
        self._noSerialize = [*bak, "customFields"]
        tab = self._indentationString * indentation
        tabContent = self._indentationString * (indentation + 1)
        s = super().contentToString(indentation, hideNone)
        s += f"{tab}customFields=\n"
        self._noSerialize = bak
        for field in self.customFields or []:
            if not field and hideNone:
                continue
            s += f"{tabContent}{str(field)}\n"

        return s

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def isFolded(self) -> Optional[bool]:
        return self._isFolded

    @isFolded.setter
    def isFolded(self, value):
        self._isFolded = self.checkAndConvertNullable(value, bool, "isFolded")

    @property
    def isHeadless(self) -> Optional[bool]:
        return self._isHeadless

    @isHeadless.setter
    def isHeadless(self, value):
        self._isHeadless = self.checkAndConvertNullable(value, bool, "isHeadless")

    @property
    def customFields(self) -> Optional[List[CustomField]]:
        return self._customFields

    @customFields.setter
    def customFields(self, value):
        self._customFields = self.checkListAndConvertNullable(
            value, CustomField, "customFields"
        )
