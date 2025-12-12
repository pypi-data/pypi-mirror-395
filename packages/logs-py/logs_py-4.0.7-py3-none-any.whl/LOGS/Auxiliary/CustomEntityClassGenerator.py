import base64
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from LOGS.Auxiliary.CheckClassName import CheckClassName
from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import TypedEntityNotConnectedException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.CustomFieldModels import CustomTypeEntityTypeMapper
from LOGS.Entity import Entity
from LOGS.Interfaces.ITypedEntity import ITypedEntity

if TYPE_CHECKING:
    from LOGS.Entities.CustomType import CustomType
    from LOGS.LOGSConnection import LOGSConnection


_T = TypeVar("_T", bound=Constants.TYPED_ENTITIES)


class CustomEntityClassGenerator(Generic[_T]):

    _customTypeCache: Dict[str, "CustomType"] = {}
    _classCache: Dict[str, Type[_T]] = {}

    @classmethod
    def generate(
        cls,
        customType: Optional["CustomType"],
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
        limitToEntityType: Optional[Type[_T]] = None,
    ) -> Type[_T]:
        if customType is None:
            if not limitToEntityType:
                raise ValueError(
                    "When 'customType' is None, 'limitToEntityType' must be provided."
                )

            if not isinstance(limitToEntityType, type) or not issubclass(
                limitToEntityType, Entity
            ):
                raise ValueError("'limitToEntityType' must be an entity class.")

            return limitToEntityType
        else:
            if not customType or not customType.id:
                raise ValueError(f"Custom type is missing for field '{fieldName}'.")

            cacheId = cls._getCacheKey(customType.id, connection)
            if cacheId in cls._classCache:
                return cls._classCache[cacheId]

            if not customType.entityType:
                raise ValueError(
                    f"Custom type '{customType.name}' (ID: {customType.id}) has no entity type defined."
                )

            entityType = CustomTypeEntityTypeMapper.getClass(customType.entityType)

            if limitToEntityType and limitToEntityType != entityType:
                raise Exception(
                    f"The custom type '{customType.name}' is not valid for entity type '{limitToEntityType.__name__}'. (Expected entity type '{entityType.__name__}')"
                )

            name = (
                entityType.__name__
                + "_"
                + (
                    CheckClassName.sanitizeClassName(customType.name)
                    if customType.name
                    else f"CustomType_ID{customType.id}"
                )
            )

            doc = f"This class represents a LOGS {entityType.__name__} of custom type '{customType.name}' (TypeID: {customType.id})"

            module = ".".join(
                entityType.__module__.split(".")[:-1]
                + [f"Custom{Tools.wordToPlural(entityType.__name__)}"],
            )

        def __init__(
            self,
            ref=None,
            id: Optional[int] = None,
            connection: Optional["LOGSConnection"] = connection,
            *args,
            **kwargs,
        ):
            cast(Any, type(self).__bases__[0]).__init__(
                self,
                ref=ref,
                id=id,
                connection=connection,
                *args,
                **kwargs,
            )

        typeDict = {
            "__init__": __init__,
            "__module__": module,
            "__doc__": doc,
            "_customType": customType,
            "_baseType": entityType,
        }

        newClass = cast(
            Type[_T],
            type(
                name,
                (entityType,),
                typeDict,
            ),
        )

        return newClass

    @classmethod
    def _getCacheKey(
        cls,
        customTypeOrId: int,
        connection: "LOGSConnection",
    ) -> str:
        url = connection.getEndpointUrl(
            ["custom_type_entities"] + [str(customTypeOrId)],
        )
        return base64.b64encode(url.encode()).decode()

    @classmethod
    def fetchCustomType(
        cls, customTypeOrId: Union["CustomType", int], connection: "LOGSConnection"
    ):
        from LOGS.Entities.CustomType import CustomType

        if isinstance(customTypeOrId, CustomType):
            return customTypeOrId

        if isinstance(customTypeOrId, int):
            cacheId = cls._getCacheKey(customTypeOrId, connection)
            if cacheId in cls._customTypeCache:
                return cls._customTypeCache[cacheId]

            customType = CustomType(id=customTypeOrId, connection=connection)
            customType.fetch()

            cls._customTypeCache[cacheId] = customType
            return customType

        raise ValueError(
            f"Parameter '{customTypeOrId}' must be either a {CustomType.__name__} instance or an integer ID."
        )

    @classmethod
    def convert(
        cls,
        value: Any,
        customTypeOrId: Union["CustomType", int],
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
        limitToEntityType: Optional[Type[_T]] = None,
    ) -> _T:

        if isinstance(value, Entity):
            return cast(_T, value)

        customType = cls.fetchCustomType(customTypeOrId, connection)

        c = cls.generate(customType, connection, fieldName, limitToEntityType)
        try:
            return c(value)
        except Exception as e:
            raise ValueError(
                f"Field '{fieldName}' cannot be converted to '{c.__name__}': {str(e)}"
            ) from e

    @classmethod
    def convertToUntyped(cls, entity: _T, fieldName: Optional[str] = None) -> _T:
        if not isinstance(entity, ITypedEntity) or not entity._baseType:
            return entity

        if not entity._connection:
            raise TypedEntityNotConnectedException(entity)

        customType = entity.customType
        customValues = entity.customValues

        entity._customType = None
        entity._customValues = None

        c = cls.generate(
            None,
            connection=entity._connection,
            fieldName=fieldName,
            limitToEntityType=cast(_T, entity._baseType),
        )(entity, connection=entity._getConnection())

        entity._customType = customType
        entity._customValues = customValues

        c._untypedCustomType = customType.toDict() if customType else None
        c._untypedValues = cast(Any, customValues.toDict()) if customValues else None
        return c

    @classmethod
    def convertFromUntyped(
        cls,
        entity: _T,
        fieldName: Optional[str] = None,
        limitToEntityType: Optional[Type[_T]] = None,
    ) -> _T:
        if not isinstance(entity, ITypedEntity) or not entity._untypedCustomType:
            return entity

        if (
            not isinstance(entity._untypedCustomType, dict)
            or "id" not in entity._untypedCustomType
        ):
            raise Exception(f"Custom type of {entity.identifier} is invalid.")

        if not entity._connection:
            raise TypedEntityNotConnectedException(entity)

        customTypeId = entity._untypedCustomType["id"]
        entity._untypedCustomType = None
        values = entity._untypedValues
        entity._untypedValues = None

        customType = cls.fetchCustomType(customTypeId, entity._connection)

        c = cls.generate(
            customType,
            connection=entity._connection,
            fieldName=fieldName,
            limitToEntityType=limitToEntityType,
        )

        try:
            e = c(entity, connection=entity._getConnection())
        except Exception as e:
            raise ValueError(
                f"Field '{fieldName}' cannot be converted to '{c.__name__}': {str(e)}"
            ) from e
        e.customValues = values
        return e
