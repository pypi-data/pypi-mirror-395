from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.LabNotebookTemplate import LabNotebookTemplate
from LOGS.Entities.LabNotebookTemplateRequestParameter import (
    LabNotebookTemplateRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("lab_notebook_templates")
class LabNotebookTemplates(
    EntityIterator[LabNotebookTemplate, LabNotebookTemplateRequestParameter]
):
    """LOGS connected LabNotebookTemplate iterator"""

    _generatorType = LabNotebookTemplate
    _parameterType = LabNotebookTemplateRequestParameter
