from base64 import b64encode
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, TypeVar, Union, cast

from LOGS.Auxiliary.CheckClassName import CheckClassName
from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.CustomSectionClassGenerator import CustomSectionClassGenerator
from LOGS.Auxiliary.Exceptions import EntityFetchingException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.ICustomSectionValue import ICustomSectionValue
from LOGS.Interfaces.ICustomTypeValue import ICustomTypeValue

if TYPE_CHECKING:
    from LOGS.Entities.CustomType import CustomType
    from LOGS.LOGSConnection import LOGSConnection


_T = TypeVar("_T")


class CustomTypeClassGenerator:

    _classCache: Dict[str, Type["ICustomTypeValue"]] = {}

    @classmethod
    def _getCacheKey(cls, customTypeOrId: int, connection: "LOGSConnection") -> str:
        url = connection.getEndpointUrl(
            ["custom_types", str(customTypeOrId)],
        )
        return b64encode(url.encode()).decode()

    @classmethod
    def generate(
        cls,
        customType: "CustomType",
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
    ):

        if not customType or not customType.id:
            raise ValueError(f"Custom type is missing for field '{fieldName}'.")

        cacheId = cls._getCacheKey(customType.id, connection)
        if cacheId in cls._classCache:
            return cls._classCache[cacheId]

        sections = (
            [
                CustomSectionClassGenerator.generate(
                    section,
                    customTypeId=customType.id,
                    sectionIndex=i,
                    connection=connection,
                )
                for i, section in enumerate(customType.sections)
            ]
            if customType.sections
            else []
        )

        name = (
            CheckClassName.sanitizeClassName(customType.name)
            if customType.name
            else f"CustomType_ID{customType.id}"
        )

        module = ".".join(
            ICustomTypeValue.__module__.split(".")[:-1] + ["GeneratedCustomTypeValues"],
        )

        class SectionProperty:
            def __init__(self, name: str):
                self.name = name

            def __get__(self, instance: ICustomSectionValue, _):
                return instance.getField(self.name)

        def __init__(self, ref=None):
            cast(Any, type(self).__bases__[0]).__init__(self, ref)

        typeDict = {
            "__init__": __init__,
            "__module__": module,
            "__doc__": f"This class represents the value of the LOGS custom type '{customType.name}' (TypeID: {customType.id})",
            "_name": customType.name,
            "_id": customType.id,
            "_fieldNames": [],
            "_fieldTypes": {},
            "_fieldIds": {},
            "_noSerialize": ["fieldNames"],
        }

        for s in sections:
            attrName = Tools.resolveKeyConflictWithPrefix(s.__name__, "_", typeDict)

            typeDict["_" + attrName] = None
            typeDict[attrName] = SectionProperty(attrName)
            typeDict["_fieldNames"].append(attrName)
            typeDict["_fieldTypes"][attrName] = s
            typeDict["_fieldIds"][s.getId()] = attrName

        typeDict["_noSerialize"] += typeDict["_fieldNames"]

        newClass: Type[ICustomTypeValue] = type(
            name,
            (ICustomTypeValue,),
            typeDict,
        )

        return newClass

    @classmethod
    def convert(
        cls,
        value: Any,
        customTypeOrId: Union["CustomType", int],
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
    ) -> Optional["ICustomTypeValue"]:
        from LOGS.Entities.CustomType import CustomType

        if isinstance(value, ICustomTypeValue):
            return value

        if not isinstance(value, list):
            raise ValueError(
                f"Field '{fieldName}' cannot be converted from value of type '{type(value).__name__}'."
            )

        if isinstance(customTypeOrId, int):
            customType = CustomType(id=customTypeOrId, connection=connection)
            try:
                customType.fetch()
            except EntityFetchingException as e:
                raise ValueError(
                    f"Field '{fieldName}' cannot be converted:"
                    + f"\n{Constants.exceptionIndentation}{str(e)}"
                )
        else:
            customType = customTypeOrId

        c = cls.generate(customType, connection, fieldName)
        try:
            return c(value)
        except Exception as e:
            raise ValueError(
                f"Field '{fieldName}' cannot be converted to '{c.__name__}': {str(e)}"
            ) from e
