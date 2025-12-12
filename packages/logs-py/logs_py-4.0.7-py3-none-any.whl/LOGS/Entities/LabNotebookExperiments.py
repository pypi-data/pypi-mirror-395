from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.LabNotebookExperiment import LabNotebookExperiment
from LOGS.Entities.LabNotebookExperimentRequestParameter import (
    LabNotebookExperimentRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("lab_notebook_experiments")
class LabNotebookExperiments(
    EntityIterator[LabNotebookExperiment, LabNotebookExperimentRequestParameter]
):
    """LOGS connected LabNotebookExperiment iterator"""

    _generatorType = LabNotebookExperiment
    _parameterType = LabNotebookExperimentRequestParameter
