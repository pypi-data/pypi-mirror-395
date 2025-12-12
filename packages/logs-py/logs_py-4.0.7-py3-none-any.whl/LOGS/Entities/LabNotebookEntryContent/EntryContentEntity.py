from LOGS.Entities.LabNotebookEntryContent.EntityAttribute import EntityAttribute
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)


class EntryContentEntity(
    EntryContentItem,
    IEntryContentWithAttribute[EntityAttribute],
):
    _attrType = EntityAttribute
    _type = "entity"
