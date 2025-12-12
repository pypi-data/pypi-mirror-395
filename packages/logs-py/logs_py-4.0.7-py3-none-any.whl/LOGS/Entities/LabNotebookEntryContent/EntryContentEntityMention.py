from typing import List, Optional

from LOGS.Entities.LabNotebookEntryContent.EntityAttribute import EntityAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.TextMarkConverter import TextMarkConverter


class EntryContentEntityMention(
    EntryContentItem,
    IEntryContentWithAttribute[EntityAttribute],
):
    _attrType = EntityAttribute
    _type = "entityMention"

    _marks: Optional[List[IEntryContentWithAttribute]] = None

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
