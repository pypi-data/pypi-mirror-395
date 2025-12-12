from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.TextAttribute import TextAttribute


class HeadingAttribute(TextAttribute):
    _level: Optional[int] = None

    @property
    def level(self) -> Optional[int]:
        return self._level

    @level.setter
    def level(self, value):
        self._level = self.checkAndConvertNullable(value, int, "level")


class EntryContentHeading(EntryContentItem, IEntryContentWithContent):
    _type = "heading"

    _attrs: Optional[HeadingAttribute] = None

    @property
    def attrs(self) -> Optional[HeadingAttribute]:
        return self._attrs

    @attrs.setter
    def attrs(self, value):
        self._attrs = self.checkAndConvertNullable(value, HeadingAttribute, "attrs")
