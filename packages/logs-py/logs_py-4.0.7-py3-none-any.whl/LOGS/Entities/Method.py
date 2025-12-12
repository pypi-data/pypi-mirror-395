from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity

if TYPE_CHECKING:
    from LOGS.Entities.DataFormatMinimal import DataFormatMinimal
    from LOGS.Entities.MethodMinimal import MethodMinimal


@Endpoint("methods")
class Method(EntityWithStrId, INamedEntity, IGenericPermissionEntity):
    _fullName: Optional[str] = None
    _description: Optional[str] = None
    _dataFormats: Optional[List["DataFormatMinimal"]] = None
    _childMethods: Optional[List["MethodMinimal"]] = None
    _parentMethod: Optional["MethodMinimal"] = None

    @property
    def fullName(self) -> Optional[str]:
        return self._fullName

    @fullName.setter
    def fullName(self, value):
        self._fullName = self.checkAndConvertNullable(value, str, "fullName")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def dataFormats(self) -> Optional[List["DataFormatMinimal"]]:
        return self._dataFormats

    @dataFormats.setter
    def dataFormats(self, value):
        self._dataFormats = MinimalModelGenerator.MinimalFromList(
            value, "DataFormatMinimal", "dataFormats", connection=self._getConnection()
        )

    @property
    def childMethods(self) -> Optional[List["MethodMinimal"]]:
        return self._childMethods

    @childMethods.setter
    def childMethods(self, value):
        self._childMethods = MinimalModelGenerator.MinimalFromList(
            value, "MethodMinimal", "childMethods", self._getConnection()
        )

    @property
    def parentMethod(self) -> Optional["MethodMinimal"]:
        return self._parentMethod

    @parentMethod.setter
    def parentMethod(self, value):
        self._parentMethod = MinimalModelGenerator.MinimalFromSingle(
            value, "MethodMinimal", "parentMethod", self._getConnection()
        )
