from base64 import b64encode
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, cast

from LOGS.Auxiliary.CheckClassName import CheckClassName
from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import EntityFetchingException

if TYPE_CHECKING:
    from LOGS.Interfaces.ICustomFieldValue import ICustomFieldValue
    from LOGS.LOGSConnection import LOGSConnection


class CustomFieldClassGenerator:

    _classCache: Dict[str, Type["ICustomFieldValue"]] = {}

    @classmethod
    def _getCacheKey(cls, customTypeField: int, connection: "LOGSConnection") -> str:
        url = connection.getEndpointUrl(["custom_type_fields", customTypeField])
        return b64encode(url.encode()).decode()

    @classmethod
    def generate(
        cls,
        customFieldId: int,
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
    ) -> Type["ICustomFieldValue"]:
        from LOGS.Entities.CustomField import CustomField
        from LOGS.Interfaces.ICustomFieldValue import ICustomFieldValue

        cacheId = cls._getCacheKey(customFieldId, connection)
        if cacheId in cls._classCache:
            return cls._classCache[cacheId]

        customField = CustomField(id=customFieldId, connection=connection)
        try:
            customField.fetch()
        except EntityFetchingException as e:
            raise ValueError(
                f"Custom field with ID {customFieldId} specified in '{fieldName}' not found:"
                + f"\n{Constants.exceptionIndentation}{str(e)}"
            )

        if cacheId in cls._classCache:
            return cls._classCache[cacheId]

        name = (
            CheckClassName.sanitizeClassName(customField.name)
            if customField.name
            else f"CustomField_ID{customField.id}"
        )

        def __init__(self, ref=None):
            cast(Any, type(self).__bases__[0]).__init__(self, ref, customField.dataType)

        doc = (
            f"This class represents the value of the LOGS custom field '{customField.name}' (ID: {customField.id})"
            + ("\n" + customField.description if customField.description else "")
        )

        module = ".".join(
            ICustomFieldValue.__module__.split(".")[:-1]
            + ["GeneratedCustomFieldValues"],
        )

        newClass: Type[ICustomFieldValue] = type(
            name,
            (ICustomFieldValue,),
            {
                "__init__": __init__,
                "_dataType": customField.dataType,
                "__module__": module,
                "__doc__": doc,
                "_name": customField.name,
                "_id": customField.id,
                "_connection": connection,
                "_value": (
                    customField.defaultValues
                    if customField.defaultValues is not None
                    else None
                ),
            },
        )
        cls._classCache[cacheId] = newClass

        return newClass

    @classmethod
    def convert(
        cls,
        value: Any,
        customFieldId: int,
        connection: "LOGSConnection",
        fieldName: Optional[str] = None,
    ) -> Optional["ICustomFieldValue"]:
        from LOGS.Interfaces.ICustomFieldValue import ICustomFieldValue

        if isinstance(value, ICustomFieldValue):
            return value

        if not isinstance(value, dict):
            raise ValueError(
                f"Field '{fieldName}' cannot be converted from value of type '{type(value).__name__}'."
            )

        c = cls.generate(
            customFieldId=customFieldId, fieldName=fieldName, connection=connection
        )
        try:
            return c(value)
        except Exception as e:
            raise ValueError(
                f"Field '{fieldName}' cannot be converted to '{c.__name__}': {str(e)}"
            ) from e
