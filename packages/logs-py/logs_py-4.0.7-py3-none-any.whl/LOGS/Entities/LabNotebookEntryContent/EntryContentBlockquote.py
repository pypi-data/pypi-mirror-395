from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithContent import (
    IEntryContentWithContent,
)
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithTextAttribute import (
    IEntryContentWithTextAttribute,
)


class EntryContentBlockquote(
    EntryContentItem, IEntryContentWithContent, IEntryContentWithTextAttribute
):
    _type = "blockquote"
