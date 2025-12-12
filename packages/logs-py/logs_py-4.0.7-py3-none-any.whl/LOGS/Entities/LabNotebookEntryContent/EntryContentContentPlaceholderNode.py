from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.TextAttribute import TextAttribute


class PlaceholderNodeAttribute(TextAttribute):
    _label: Optional[str] = None

    @property
    def label(self) -> Optional[str]:
        return self._label

    @label.setter
    def label(self, value):
        self._label = self.checkAndConvertNullable(value, str, "label")


class EntryContentContentPlaceholderNode(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[PlaceholderNodeAttribute],
):
    _attrType = PlaceholderNodeAttribute
    _type = "contentPlaceholderNode"
