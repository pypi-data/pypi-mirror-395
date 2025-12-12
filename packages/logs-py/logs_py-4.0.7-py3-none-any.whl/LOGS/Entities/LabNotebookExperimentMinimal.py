from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.LabNotebookExperiment import LabNotebookExperiment
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(LabNotebookExperiment)
class LabNotebookExperimentMinimal(EntityMinimalWithIntId[LabNotebookExperiment]):
    pass
