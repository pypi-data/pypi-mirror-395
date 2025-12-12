from typing import TYPE_CHECKING, List, Optional, Union, cast

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ISignableEntity import ISignableEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.Project import Project
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


@Endpoint("samples")
class Sample(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    ITypedEntity,
    IOwnedEntity,
    IProjectBased,
    IEntryRecord,
    IModificationRecord,
    ISoftDeletable,
    ILockableEntity,
    ISignableEntity,
    IGenericPermissionEntity,
):

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: str = "",
        projects: Optional[List[Union["ProjectMinimal", "Project"]]] = None,
    ):
        self._name = name
        self._projects = cast(Optional[List["ProjectMinimal"]], projects)

        if ref != None and isinstance(ref, (str, int, float)):
            ref = {"text": str(ref)}

        super().__init__(ref=ref, id=id, connection=connection)
