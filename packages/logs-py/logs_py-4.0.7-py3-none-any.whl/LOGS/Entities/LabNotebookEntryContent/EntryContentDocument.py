from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)


class EntryContentDocument(EntryContentItem, IEntryContentWithContent):
    _type = "doc"
