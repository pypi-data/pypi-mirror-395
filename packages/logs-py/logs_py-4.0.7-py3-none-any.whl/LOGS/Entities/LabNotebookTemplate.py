from typing import Any, Dict, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ISessionedEntity import ISessionedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.Interfaces.IVersionedEntity import IVersionedEntity


@Endpoint("lab_notebook_templates")
class LabNotebookTemplate(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    IVersionedEntity,
    IProjectBased,
    IGenericPermissionEntity,
    ISessionedEntity,
    ILockableEntity,
):
    _description: Optional[str] = None
    _content: Optional[Dict[str, Any]] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def content(self) -> Optional[Dict[str, Any]]:
        return self._content

    @content.setter
    def content(self, value: Dict[str, Any]):
        self._content = self.checkAndConvertNullable(value, dict, "content")
