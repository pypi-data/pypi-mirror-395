from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entities.LabNotebookModels import LabNotebookExperimentStatus
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.ISignableEntity import ISignableEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.Interfaces.IVersionedEntity import IVersionedEntity

if TYPE_CHECKING:
    from LOGS.Entities import LabNotebookMinimal


@Endpoint("lab_notebook_experiments")
class LabNotebookExperiment(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    IVersionedEntity,
    IGenericPermissionEntity,
    ILockableEntity,
    ISignableEntity,
):
    _labNotebook: Optional["LabNotebookMinimal"] = None
    _status: Optional[LabNotebookExperimentStatus] = None
    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def status(self) -> Optional[LabNotebookExperimentStatus]:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = self.checkAndConvertNullable(
            value, LabNotebookExperimentStatus, "status"
        )

    @property
    def labNotebook(self) -> Optional["LabNotebookMinimal"]:
        return self._labNotebook

    @labNotebook.setter
    def labNotebook(self, value: str):
        self._labNotebook = MinimalModelGenerator.MinimalFromSingle(
            value, "LabNotebookMinimal", "labNotebook", self._getConnection()
        )
