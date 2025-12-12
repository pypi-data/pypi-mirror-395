from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)


class ListItemAttribute(BasicAttribute):
    _order: Optional[int] = None
    _closed: Optional[bool] = False
    _nested: Optional[bool] = False

    @property
    def closed(self) -> Optional[bool]:
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = self.checkAndConvertNullable(value, bool, "closed")

    @property
    def nested(self) -> Optional[bool]:
        return self._nested

    @nested.setter
    def nested(self, value):
        self._nested = self.checkAndConvertNullable(value, bool, "nested")

    @property
    def order(self) -> Optional[int]:
        return self._order

    @order.setter
    def order(self, value):
        self._order = self.checkAndConvertNullable(value, int, "order")


class EntryContentListItem(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[ListItemAttribute],
):
    _attrType = ListItemAttribute
    _type = "listItem"
