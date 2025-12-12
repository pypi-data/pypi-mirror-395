from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)


class CalloutAttribute(BasicAttribute):
    _type: Optional[str] = None
    _emoji: Optional[str] = None

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, str, "type")

    @property
    def emoji(self) -> Optional[str]:
        return self._emoji

    @emoji.setter
    def emoji(self, value):
        self._emoji = self.checkAndConvertNullable(value, str, "emoji")


class EntryContentCallout(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[CalloutAttribute],
):
    _attrType = CalloutAttribute
    _type = "callout"
