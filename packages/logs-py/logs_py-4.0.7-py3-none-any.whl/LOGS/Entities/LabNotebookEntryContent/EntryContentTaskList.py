from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.TextMarkAtributes import BasicAttribute


class EntryContentTaskList(
    EntryContentItem,
    IEntryContentWithContent,
    IEntryContentWithAttribute[BasicAttribute],
):
    _attrType = BasicAttribute
    _type = "taskList"
