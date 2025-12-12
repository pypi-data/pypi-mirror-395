from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.LabNotebook import LabNotebook
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(LabNotebook)
class LabNotebookMinimal(EntityMinimalWithIntId[LabNotebook]):
    pass
