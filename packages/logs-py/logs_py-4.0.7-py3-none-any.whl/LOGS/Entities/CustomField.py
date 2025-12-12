from typing import TYPE_CHECKING, Any, List, Optional, cast

from LOGS.Auxiliary.CustomFieldValueTypeChecker import CustomFieldValueTypeChecker
from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entities.CustomFieldModels import CustomFieldDataType
from LOGS.Entities.ILiteraryTypedEntity import ILiteraryTypedEntity
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal


@Endpoint("custom_fields")
class CustomField(
    IEntityWithIntId,
    IOwnedEntity,
    INamedEntity,
    IUniqueEntity,
    IEntryRecord,
    IModificationRecord,
    ILiteraryTypedEntity,
    IGenericPermissionEntity,
):
    _type = "CustomField"
    _valueTypeChecker: CustomFieldValueTypeChecker = cast(
        CustomFieldValueTypeChecker, None
    )
    _description: Optional[str] = None
    _placeholder: Optional[str] = None
    _dataType: Optional[CustomFieldDataType] = None
    _required: Optional[bool] = None
    _readOnly: Optional[bool] = None
    _validationRegexp: Optional[str] = None
    _validationMessage: Optional[str] = None
    _showAsTextArea: Optional[bool] = None
    _predefinedOptions: Optional[List[Any]] = None
    _predefinedOptionsFromValues: bool = False
    _defaultValues: Optional[Any] = None
    _customTypeConstraint: Optional[List["CustomTypeMinimal"]] = None
    _templateVersion: Optional[str] = None
    _integrationId: Optional[str] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        if ref != None and isinstance(ref, (str, int, float)):
            ref = {"text": str(ref)}

        super().__init__(id=id, ref=ref, connection=connection)

    def fromDict(self, ref) -> None:
        if (
            isinstance(ref, dict)
            and "dataType" in ref
            and isinstance(ref["dataType"], str)
        ):
            self.dataType = CustomFieldDataType(ref["dataType"])

        super().fromDict(ref=ref)

    def __str__(self) -> str:
        i = " id:'%s'" % self.id if self.id is not None else ""
        t = " type:'%s'" % self._dataType.name if self._dataType else ""
        n = " name:'%s'" % self.name if self.name is not None else ""
        return "<%s%s%s%s>" % (type(self).__name__, i, t, n)

    @staticmethod
    def isValidClassName(name: str) -> bool:
        if not isinstance(name, str) or not name:
            return False
        if not name.isidentifier():
            return False
        if not name[0].isupper():
            return False
        return True

    @property
    def className(self) -> Optional[str]:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def defaultValues(self) -> Optional[Any]:
        return self._defaultValues

    @defaultValues.setter
    def defaultValues(self, value):
        if not self._dataType:
            raise Exception("Data type is not set")

        self._defaultValues = self._valueTypeChecker.checkAndConvert(
            value, "defaultValues"
        )

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @readOnly.setter
    def readOnly(self, value):
        self._readOnly = self.checkAndConvertNullable(value, bool, "readOnly")

    @property
    def required(self) -> Optional[bool]:
        return self._required

    @required.setter
    def required(self, value):
        self._required = self.checkAndConvertNullable(value, bool, "required")

    @property
    def validationRegexp(self) -> Optional[str]:
        return self._validationRegexp

    @validationRegexp.setter
    def validationRegexp(self, value):
        self._validationRegexp = self.checkAndConvertNullable(
            value, str, "validationRegexp"
        )

    @property
    def validationMessage(self) -> Optional[str]:
        return self._validationMessage

    @validationMessage.setter
    def validationMessage(self, value):
        self._validationMessage = self.checkAndConvertNullable(
            value, str, "validationMessage"
        )

    @property
    def predefinedOptions(self) -> Optional[List[Any]]:
        return self._predefinedOptions

    @predefinedOptions.setter
    def predefinedOptions(self, value):
        if not self._dataType:
            raise Exception("Data type is not set")

        if not value:
            self._predefinedOptions = None
            return

        self._predefinedOptions = (
            self._valueTypeChecker.checkAndConvertIgnoreEnumOptions(
                value, "predefinedOptions"
            )
        )
        if not self._predefinedOptionsFromValues and self._predefinedOptions:
            self._valueTypeChecker.enumOptions = self._predefinedOptions

    @property
    def customTypeConstraint(self) -> Optional[List["CustomTypeMinimal"]]:
        return self._customTypeConstraint

    @customTypeConstraint.setter
    def customTypeConstraint(self, value):
        self._customTypeConstraint = MinimalModelGenerator.MinimalFromList(
            value, "CustomTypeMinimal", "customTypeConstraint", self._getConnection()
        )

    @property
    def dataType(self) -> Optional[CustomFieldDataType]:
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = self.checkAndConvertNullable(
            value, CustomFieldDataType, "dataType"
        )
        if (
            not self._valueTypeChecker
            or self._valueTypeChecker.dataType != self._dataType
        ):
            self._valueTypeChecker = CustomFieldValueTypeChecker(
                self._dataType,
                self._getConnection(),
                self._valueTypeChecker.enumOptions if self._valueTypeChecker else None,
            )

    @property
    def predefinedOptionsFromValues(self) -> bool:
        return self._predefinedOptionsFromValues

    @predefinedOptionsFromValues.setter
    def predefinedOptionsFromValues(self, value):
        self._predefinedOptionsFromValues = self.checkAndConvert(
            value, bool, "predefinedOptionsFromValues"
        )

    @property
    def placeholder(self) -> Optional[str]:
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = self.checkAndConvertNullable(value, str, "placeholder")

    @property
    def showAsTextArea(self) -> Optional[bool]:
        return self._showAsTextArea

    @showAsTextArea.setter
    def showAsTextArea(self, value):
        self._showAsTextArea = self.checkAndConvertNullable(
            value, bool, "showAsTextArea"
        )

    @property
    def templateVersion(self) -> Optional[str]:
        return self._templateVersion

    @templateVersion.setter
    def templateVersion(self, value):
        self._templateVersion = self.checkAndConvertNullable(
            value, str, "templateVersion"
        )

    @property
    def integrationId(self) -> Optional[str]:
        return self._integrationId

    @integrationId.setter
    def integrationId(self, value):
        self._integrationId = self.checkAndConvertNullable(value, str, "integrationId")
