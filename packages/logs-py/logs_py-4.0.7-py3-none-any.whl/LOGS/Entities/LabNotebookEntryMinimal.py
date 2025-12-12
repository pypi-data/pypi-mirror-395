from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(LabNotebookEntry)
class LabNotebookEntryMinimal(EntityMinimalWithIntId[LabNotebookEntry]):
    pass
