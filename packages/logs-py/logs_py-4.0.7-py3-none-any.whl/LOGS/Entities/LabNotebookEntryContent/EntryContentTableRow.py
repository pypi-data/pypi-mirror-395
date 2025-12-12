from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)


class EntryContentTableRow(EntryContentItem, IEntryContentWithContent):
    _type = "tableRow"
