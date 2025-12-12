from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.ProjectPersonPermission import ProjectPersonPermission
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("projects")
class Project(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    ITypedEntity,
    IOwnedEntity,
    IEntryRecord,
    IModificationRecord,
    ILockableEntity,
    IGenericPermissionEntity,
):

    _projectPersonPermissions: Optional[List[ProjectPersonPermission]] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._name = name
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def projectPersonPermissions(self) -> Optional[List[ProjectPersonPermission]]:
        return self._projectPersonPermissions

    @projectPersonPermissions.setter
    def projectPersonPermissions(self, value):
        self._projectPersonPermissions = self.checkListAndConvertNullable(
            value, ProjectPersonPermission, "projectPersonPermissions"
        )
