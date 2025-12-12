from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, Type, TypeVar, cast

from LOGS.Auxiliary import Tools
from LOGS.Entity.SerializableContent import SerializableClass
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class IPermissionedEntityRequest:
    includePermissions: Optional[bool] = None


class IPermissionModel:
    edit: Optional[bool] = None


class GenericPermission(IPermissionModel, SerializableClass):
    canDownload: Optional[bool] = None
    canEdit: Optional[bool] = None
    canTrash: Optional[bool] = None
    canRestore: Optional[bool] = None
    canDelete: Optional[bool] = None
    canLock: Optional[bool] = None
    canUnlock: Optional[bool] = None
    canSign: Optional[bool] = None
    canRemoveSignatures: Optional[bool] = None

    def __str__(self):
        attrList = self._getAttrList()

        s = ",".join(
            k
            for k in attrList
            if k.startswith("can") and getattr(self, k, None) is True
        )
        return f"<{type(self).__name__} access:{s}>"

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        return str(self)


_PERMISSION = TypeVar("_PERMISSION", bound=IPermissionModel)


class IPermissionedEntity(Generic[_PERMISSION], IEntityInterface):
    _permissionType: Optional[Type[_PERMISSION]] = None

    _permissions: Optional[_PERMISSION] = None

    @property
    def permissions(self) -> Optional[_PERMISSION]:
        return self._permissions

    @permissions.setter
    def permissions(self, value):
        if not self._permissionType:
            raise NotImplementedError("Permission type must be set")

        self._permissions = Tools.checkAndConvert(
            value,
            cast(Type[_PERMISSION], self._permissionType),
            "permissions",
            allowNone=True,
        )


class IGenericPermissionEntity(IPermissionedEntity[GenericPermission]):
    _permissionType: Type[GenericPermission] = GenericPermission
