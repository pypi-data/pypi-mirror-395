from typing import Generic, Optional, Type, TypeVar

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entity.SerializableContent import SerializableContent

_T = TypeVar("_T", bound=BasicAttribute)


class IEntryContentWithAttribute(Generic[_T], SerializableContent):
    _attrType: Optional[Type] = None
    _attrs: Optional[_T] = None

    @property
    def attrs(self) -> Optional[_T]:
        return self._attrs

    @attrs.setter
    def attrs(self, value):
        if not self._attrType:
            raise Exception(
                f"Field attrType must be defined for class '{type(self).__name__}'"
            )
        self._attrs = self.checkAndConvertNullable(value, self._attrType, "attrs")
