from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
from LOGS.Entities.LabNotebookEntryRequestParameter import (
    LabNotebookEntryRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("lab_notebook_entries")
class LabNotebookEntries(
    EntityIterator[LabNotebookEntry, LabNotebookEntryRequestParameter]
):
    """LOGS connected LabNotebookEntry iterator"""

    _generatorType = LabNotebookEntry
    _parameterType = LabNotebookEntryRequestParameter
