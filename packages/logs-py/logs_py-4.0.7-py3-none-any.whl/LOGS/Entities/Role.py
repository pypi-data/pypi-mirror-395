from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import MinimalModelGenerator
from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Permission import Permission
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@Endpoint("roles")
class Role(
    IEntityWithIntId,
    INamedEntity,
    IGenericPermissionEntity,
    IEntryRecord,
    IModificationRecord,
):

    _rolePermissions: Optional[List["Permission"]] = None
    _users: Optional[List["PersonMinimal"]] = None
    _isInternal: Optional[bool] = None
    _roleId: Optional[str] = None
    _description: Optional[str] = None
    _isDefault: Optional[bool] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional["LOGSConnection"] = None,
    ):
        if isinstance(ref, str):
            ref = {"roleId": ref}

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def rolePermissions(self) -> Optional[List["Permission"]]:
        return self._rolePermissions

    @rolePermissions.setter
    def rolePermissions(self, value):
        self._rolePermissions = self.checkListAndConvertNullable(
            value, Permission, "rolePermissions"
        )

    @property
    def users(self) -> Optional[List["PersonMinimal"]]:
        return self._users

    @users.setter
    def users(self, value):
        self._users = MinimalModelGenerator.MinimalFromList(
            value, "PersonMinimal", "users", self._getConnection()
        )

    @property
    def isInternal(self) -> Optional[bool]:
        return self._isInternal

    @isInternal.setter
    def isInternal(self, value):
        self._isInternal = self.checkAndConvertNullable(value, bool, "isInternal")

    @property
    def roleId(self) -> Optional[str]:
        return self._roleId

    @roleId.setter
    def roleId(self, value):
        self._roleId = self.checkAndConvertNullable(value, str, "roleId")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def isDefault(self) -> Optional[bool]:
        return self._isDefault

    @isDefault.setter
    def isDefault(self, value):
        self._isDefault = self.checkAndConvertNullable(value, bool, "isDefault")
