from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.LabNotebook import LabNotebook
from LOGS.Entities.LabNotebookRequestParameter import LabNotebookRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("lab_notebooks")
class LabNotebooks(EntityIterator[LabNotebook, LabNotebookRequestParameter]):
    """LOGS connected LabNotebook iterator"""

    _generatorType = LabNotebook
    _parameterType = LabNotebookRequestParameter
