from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.LabNotebookTemplate import LabNotebookTemplate
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(LabNotebookTemplate)
class LabNotebookTemplateMinimal(EntityMinimalWithIntId[LabNotebookTemplate]):
    pass
