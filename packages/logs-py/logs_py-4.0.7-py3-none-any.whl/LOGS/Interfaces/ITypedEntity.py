from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type

from typing_extensions import Self

from LOGS.Auxiliary.Exceptions import EntityNotConnectedException
from LOGS.Entities.CustomType import CustomType
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entity.Entity import Entity
    from LOGS.Interfaces.ICustomTypeValue import ICustomTypeValue


@dataclass
class ITypedEntityRequest:
    customTypeIds: Optional[List[int]] = None
    customFieldIds: Optional[List[int]] = None


class ITypedEntity(IEntityInterface):
    _customType: Optional["CustomType"] = (
        None  # this diverges from the LOGS model (CustomTypeMinimal) because here the full custom type is retrieved
    )
    _customValues: Optional["ICustomTypeValue"] = None

    _untypedValues: Optional[List[Dict[str, Any]]] = None
    _untypedCustomType: Optional[Dict[str, Any]] = None
    _initCustomValues: bool = True
    _baseType: Optional[Type["Entity"]] = None

    def _contentToString(self) -> str:
        s = f"{type(self).__name__}"
        if self.customType:
            s += f" <{self.customType.name}>\n"
            s += self.customValues._contentToString(1) if self.customValues else ""
        else:
            s += " <no type>\n"
        return s

    def _createCustomValuesInstance(self) -> None:
        from LOGS.Auxiliary.CustomTypeClassGenerator import CustomTypeClassGenerator

        if self.customType is None:
            return

        connection = self._getEntityConnection()
        if not connection:
            raise EntityNotConnectedException()

        self._customValues = CustomTypeClassGenerator.convert(
            [],
            customTypeOrId=self.customType,
            fieldName="customValues",
            connection=connection,
        )

    def getUntypedInstance(self) -> Self:
        from LOGS.Auxiliary.CustomEntityClassGenerator import CustomEntityClassGenerator

        return CustomEntityClassGenerator.convertToUntyped(self)

    def _getTypedInstance(self) -> "ITypedEntity":
        from LOGS.Auxiliary.CustomEntityClassGenerator import CustomEntityClassGenerator
        from LOGS.Interfaces.INamedEntity import INamedEntity

        return CustomEntityClassGenerator.convertFromUntyped(
            self,
            fieldName=self.name if isinstance(self, INamedEntity) else None,
            limitToEntityType=type(self),
        )

    @property
    def baseType(self) -> Optional[Type["Entity"]]:
        return self._baseType

    @property
    def customType(self) -> Optional["CustomType"]:
        return self._customType

    @customType.setter
    def customType(self, value):
        if not self._customType and isinstance(value, dict) and "id" in value:
            self._untypedCustomType = value
            return

        if self._customType == value or value == None:
            return

        newId = (
            value.id
            if isinstance(value, CustomType)
            else value["id"] if isinstance(value, dict) and "id" in value else None
        )
        if newId and self._customType and self._customType.id == newId:
            return

        raise ValueError(f"Custom type {self._customType} cannot be changed.")

    @property
    def customValues(
        self,
    ) -> Optional["ICustomTypeValue"]:
        if self._customType and self._customValues is None:
            self._createCustomValuesInstance()
        return self._customValues

    @customValues.setter
    def customValues(self, value):
        from LOGS.Auxiliary.CustomTypeClassGenerator import CustomTypeClassGenerator

        if (
            self.customType is None
            or self._getEntityConnection() is None
            or value is None
        ):
            self._untypedValues = value
            return

        connection = self._getEntityConnection()
        if not connection:
            raise EntityNotConnectedException()

        self._customValues = CustomTypeClassGenerator.convert(
            value,
            customTypeOrId=self.customType,
            fieldName="customValues",
            connection=connection,
        )
