from enum import Enum
from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.ProjectPersonPermission import ProjectPersonPermission
from LOGS.Entities.Role import Role
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.ILockableEntity import ILockableEntity
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity


class PersonAccountState(Enum):
    NoAccount = "NoAccount"
    Enabled = "Enabled"
    Disabled = "Disabled"


@Endpoint("persons")
class Person(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    ITypedEntity,
    IEntryRecord,
    IModificationRecord,
    ISoftDeletable,
    ILockableEntity,
    IGenericPermissionEntity,
):

    _personProjectPermissions: Optional[List[ProjectPersonPermission]] = None

    _isSystemUser: Optional[bool] = None
    _has2FA: Optional[bool] = None
    _isLocalUser: Optional[bool] = None

    _firstName: Optional[str] = None
    _lastName: Optional[str] = None
    _login: Optional[str] = None
    _accountState: Optional[PersonAccountState] = None

    _email: Optional[str] = None
    _roles: Optional[List[Role]] = None
    _password: Optional[str] = None

    @property
    def personProjectPermissions(self) -> Optional[List[ProjectPersonPermission]]:
        return self._personProjectPermissions

    @personProjectPermissions.setter
    def personProjectPermissions(self, value):
        self._personProjectPermissions = self.checkListAndConvertNullable(
            value, ProjectPersonPermission, "personProjectPermissions"
        )

    @property
    def isSystemUser(self) -> Optional[bool]:
        return self._isSystemUser

    @isSystemUser.setter
    def isSystemUser(self, value):
        self._isSystemUser = self.checkAndConvertNullable(value, bool, "isSystemUser")

    @property
    def has2FA(self) -> Optional[bool]:
        return self._has2FA

    @has2FA.setter
    def has2FA(self, value):
        self._has2FA = self.checkAndConvertNullable(value, bool, "has2FA")

    @property
    def isLocalUser(self) -> Optional[bool]:
        return self._isLocalUser

    @isLocalUser.setter
    def isLocalUser(self, value):
        self._isLocalUser = self.checkAndConvertNullable(value, bool, "isLocalUser")

    @property
    def login(self) -> Optional[str]:
        return self._login

    @login.setter
    def login(self, value):
        self._login = self.checkAndConvertNullable(value, str, "login")

    @property
    def accountState(self) -> Optional[PersonAccountState]:
        return self._accountState

    @accountState.setter
    def accountState(self, value):
        self._accountState = self.checkAndConvertNullable(
            value, PersonAccountState, "accountState"
        )

    @property
    def firstName(self) -> Optional[str]:
        return self._firstName

    @firstName.setter
    def firstName(self, value):
        self._firstName = self.checkAndConvertNullable(value, str, "firstName")

    @property
    def lastName(self) -> Optional[str]:
        return self._lastName

    @lastName.setter
    def lastName(self, value):
        self._lastName = self.checkAndConvertNullable(value, str, "lastName")

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.checkAndConvertNullable(value, str, "email")

    @property
    def roles(self) -> Optional[List[Role]]:
        return self._roles

    @roles.setter
    def roles(self, value):
        if value is None:
            self._roles = None
        else:
            self._roles = self.checkListAndConvertNullable(value, Role, "roles")

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.checkAndConvertNullable(value, str, "password")
