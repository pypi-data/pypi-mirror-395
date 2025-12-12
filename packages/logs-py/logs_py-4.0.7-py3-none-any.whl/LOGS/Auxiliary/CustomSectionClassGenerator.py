from base64 import b64encode
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, cast

from LOGS.Auxiliary.CheckClassName import CheckClassName
from LOGS.Auxiliary.CustomFieldClassGenerator import CustomFieldClassGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Interfaces.ICustomSectionValue import ICustomSectionValue

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeSection import CustomTypeSection
    from LOGS.LOGSConnection import LOGSConnection


class CustomSectionClassGenerator:

    _classCache: Dict[str, Type["ICustomSectionValue"]] = {}

    @classmethod
    def _getCacheKey(cls, customTypeSection: str, connection: "LOGSConnection") -> str:
        url = connection.getEndpointUrl(["custom_type_sections", customTypeSection])
        return b64encode(url.encode()).decode()

    @classmethod
    def generate(
        cls,
        section: "CustomTypeSection",
        customTypeId: int,
        sectionIndex: int,
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
    ) -> Type["ICustomSectionValue"]:

        if not customTypeId >= 0:
            raise ValueError(
                f"Section customTypeId is missing for section in field '{fieldName}'."
            )

        if not sectionIndex >= 0:
            raise ValueError(
                f"Section index is missing for section {sectionIndex} in field '{fieldName}'."
            )

        id = ICustomSectionValue._generateId(customTypeId, sectionIndex)
        cacheId = cls._getCacheKey(id, connection)
        if cacheId in cls._classCache:
            return cls._classCache[cacheId]

        customFields = (
            [
                CustomFieldClassGenerator.generate(
                    customFieldId=c.id, fieldName=fieldName, connection=connection
                )
                for c in section.customFields
                if c and c.id
            ]
            if section.customFields
            else []
        )

        name = (
            CheckClassName.sanitizeClassName(section.name)
            if section.name
            else f"Section_TypeID{customTypeId}_Index{sectionIndex}"
        )

        module = ".".join(
            ICustomSectionValue.__module__.split(".")[:-1]
            + ["GeneratedCustomSectionValues"],
        )

        class CustomFieldProperty:
            def __init__(self, name: str):
                self.name = name

            def __get__(self, instance: ICustomSectionValue, _):
                return instance.getField(self.name)

            def __set__(self, instance: ICustomSectionValue, value):
                instance.setField(self.name, value)

        def __init__(self, ref=None):
            cast(Any, type(self).__bases__[0]).__init__(self, ref)

        typeDict = {
            "__init__": __init__,
            "__module__": module,
            "__doc__": f"This class represents the value of the LOGS custom field '{section.name}' (TypeID: {customTypeId} Index: {sectionIndex}  )",
            "_name": section.name,
            "_customTypeId": customTypeId,
            "_sectionIndex": sectionIndex,
            "_fieldNames": [],
            "_fieldTypes": {},
            "_fieldIds": {},
            "_noSerialize": ["fieldNames"],
        }

        for f in customFields:
            attrName = Tools.resolveKeyConflictWithPrefix(f.__name__, "_", typeDict)

            typeDict["_" + attrName] = None
            typeDict[attrName] = CustomFieldProperty(attrName)
            typeDict["_fieldNames"].append(attrName)
            typeDict["_fieldTypes"][attrName] = f
            typeDict["_fieldIds"][f._id] = attrName

        typeDict["_noSerialize"] += typeDict["_fieldNames"]

        newClass: Type[ICustomSectionValue] = type(
            name,
            (ICustomSectionValue,),
            typeDict,
        )
        return newClass
