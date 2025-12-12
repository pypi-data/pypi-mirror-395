from typing import List, Optional

from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.TextMarkConverter import TextMarkConverter
from LOGS.Entities.LabNotebookEntryContent.TextMarks import IEntryContentWithAttribute


class EntryContentText(EntryContentItem):
    _type = "text"

    _text: Optional[str] = None
    _marks: Optional[List[IEntryContentWithAttribute]] = None

    @property
    def text(self) -> Optional[str]:
        return self._text

    @text.setter
    def text(self, value):
        self._text = self.checkAndConvertNullable(value, str, "text")

    @property
    def marks(self) -> Optional[List[IEntryContentWithAttribute]]:
        return self._marks

    @marks.setter
    def marks(self, value):
        self._marks = self.checkListAndConvertNullable(
            value,
            IEntryContentWithAttribute,
            "marks",
            converter=TextMarkConverter.convert,
        )
