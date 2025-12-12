from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)


class OrderedListAttribute(BasicAttribute):
    _order: Optional[int] = None

    @property
    def order(self) -> Optional[int]:
        return self._order

    @order.setter
    def order(self, value):
        self._order = self.checkAndConvertNullable(value, int, "order")


class EntryContentOrderedList(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[OrderedListAttribute],
):
    _attrType = OrderedListAttribute
    _type = "orderedList"
