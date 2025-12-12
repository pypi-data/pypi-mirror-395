from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.TextMarkAtributes import BasicAttribute


class TaskListItemAttribute(BasicAttribute):
    _checked: Optional[bool] = False

    @property
    def checked(self) -> Optional[bool]:
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = self.checkAndConvertNullable(value, bool, "checked")


class EntryContentTaskListItem(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[TaskListItemAttribute],
):
    _attrType = TaskListItemAttribute
    _type = "taskListItem"
