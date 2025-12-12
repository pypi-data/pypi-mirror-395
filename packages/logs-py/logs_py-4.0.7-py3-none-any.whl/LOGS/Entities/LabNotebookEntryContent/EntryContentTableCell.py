from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.TextMarkAtributes import BasicAttribute


class TableCellAttribute(BasicAttribute):
    _colspan: Optional[int] = None
    _rowspan: Optional[int] = None

    @property
    def colspan(self) -> Optional[int]:
        return self._colspan

    @colspan.setter
    def colspan(self, value):
        self._colspan = self.checkAndConvertNullable(value, int, "colspan")

    @property
    def rowspan(self) -> Optional[int]:
        return self._rowspan

    @rowspan.setter
    def rowspan(self, value):
        self._rowspan = self.checkAndConvertNullable(value, int, "rowspan")


class EntryContentTableCell(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[TableCellAttribute],
):
    _attrType = TableCellAttribute
    _type = "tableCell"
