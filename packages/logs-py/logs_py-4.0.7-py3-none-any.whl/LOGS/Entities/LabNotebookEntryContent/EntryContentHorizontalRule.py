from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)


class EntryContentHorizontalRule(
    EntryContentItem, IEntryContentWithAttribute[BasicAttribute]
):
    _attrType = BasicAttribute
    _type = "horizontalRule"
