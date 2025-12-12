from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ISignableEntity import ISignableEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.Interfaces.IVersionedEntity import IVersionedEntity


@Endpoint("lab_notebooks")
class LabNotebook(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    IVersionedEntity,
    IProjectBased,
    IGenericPermissionEntity,
    ILockableEntity,
    ISignableEntity,
):
    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = self.checkAndConvertNullable(value, str, "description")
