from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Converter.DateTimeRange import DateTimeRange
from LOGS.Entities.CustomFieldModels import CustomFieldDataType

if TYPE_CHECKING:
    from LOGS.LOGSConnection import LOGSConnection


class CustomFieldValueTypeChecker:

    _customFieldTypeMap: Dict[CustomFieldDataType, Union[type, str, Callable]] = {
        CustomFieldDataType.String: str,
        CustomFieldDataType.StringArray: str,
        CustomFieldDataType.Integer: int,
        CustomFieldDataType.IntegerArray: int,
        CustomFieldDataType.Float: float,
        CustomFieldDataType.FloatArray: float,
        CustomFieldDataType.Boolean: bool,
        CustomFieldDataType.Date: date,
        CustomFieldDataType.DateArray: date,
        CustomFieldDataType.DateTime: datetime,
        CustomFieldDataType.DateTimeArray: datetime,
        CustomFieldDataType.Time: time,
        CustomFieldDataType.TimeArray: time,
        CustomFieldDataType.DateTimeRange: DateTimeRange,
        CustomFieldDataType.TimeRange: lambda value: (
            timedelta(seconds=value) if isinstance(value, (int, float)) else value
        ),
        CustomFieldDataType.Dataset: "DatasetMinimal",
        CustomFieldDataType.DatasetArray: "DatasetMinimal",
        CustomFieldDataType.Sample: "SampleMinimal",
        CustomFieldDataType.SampleArray: "SampleMinimal",
        CustomFieldDataType.Project: "ProjectMinimal",
        CustomFieldDataType.ProjectArray: "ProjectMinimal",
        CustomFieldDataType.Person: "PersonMinimal",
        CustomFieldDataType.PersonArray: "PersonMinimal",
        CustomFieldDataType.Method: "MethodMinimal",
        CustomFieldDataType.MethodArray: "MethodMinimal",
        CustomFieldDataType.SharedContent: "SharedContentMinimal",
        CustomFieldDataType.SharedContentArray: "SharedContentMinimal",
        CustomFieldDataType.LabNotebook: "LabNotebookMinimal",
        CustomFieldDataType.LabNotebookArray: "LabNotebookMinimal",
        CustomFieldDataType.LabNotebookExperiment: "LabNotebookExperimentMinimal",
        CustomFieldDataType.LabNotebookExperimentArray: "LabNotebookExperimentMinimal",
        CustomFieldDataType.LabNotebookEntry: "LabNotebookEntryMinimal",
        CustomFieldDataType.LabNotebookEntryArray: "LabNotebookEntryMinimal",
        CustomFieldDataType.Attachment: "AttachmentMinimal",
        CustomFieldDataType.InventoryItem: "InventoryItemMinimal",
        CustomFieldDataType.InventoryItemArray: "InventoryItemMinimal",
        CustomFieldDataType.Barcode: str,
        CustomFieldDataType.Url: str,
        CustomFieldDataType.UrlArray: str,
    }

    _converter: Callable[[Any, str], Any]
    _isArrayType: bool
    _enumOptions: Any = None

    @classmethod
    def _arrayTypeCheck(cls, data_type: CustomFieldDataType) -> bool:
        return data_type.name.endswith("Array")

    @classmethod
    def _generateConverter(
        cls,
        dataType: CustomFieldDataType,
        isArrayType: bool,
        connection: Optional["LOGSConnection"],
    ) -> Callable[[Any, str], Any]:
        dataClass = cls._customFieldTypeMap.get(dataType, None)

        if dataClass is None:
            raise ValueError(f"Unknown custom field type: '{dataType}'")

        if isinstance(dataClass, str):
            if isArrayType:
                return lambda value, fieldName: MinimalModelGenerator.MinimalFromList(
                    value, dataClass, fieldName, connection
                )
            else:
                return lambda value, fieldName: MinimalModelGenerator.MinimalFromSingle(
                    value, dataClass, fieldName, connection
                )
        elif isinstance(dataClass, type):
            if isArrayType:
                return lambda value, fieldName: Tools.checkListAndConvert(
                    value, dataClass, fieldName, allowNone=True
                )
            else:
                return lambda value, fieldName: Tools.checkAndConvert(
                    value, dataClass, f"{fieldName} <{dataType.name}>", allowNone=True
                )
        elif callable(dataClass):
            if isArrayType:
                return lambda value, fieldName: Tools.checkListAndConvert(
                    value, dataType.name, fieldName, dataClass, allowNone=True
                )
            else:
                return lambda value, fieldName: Tools.checkAndConvert(
                    value, dataType.name, fieldName, dataClass, allowNone=True
                )
        else:
            raise ValueError(f"Cannot create converter for type '{dataType}'")

    def __str__(self):
        s = " array" if self._isArrayType else ""
        return f"<{type(self).__name__} [{self.dataType.name}]{s}>"

    def __init__(
        self,
        dataType: CustomFieldDataType,
        connection: Optional["LOGSConnection"],
        enumOptions: Any = None,
    ):
        Tools.checkAndConvert(
            dataType, CustomFieldDataType, "dataType", allowNone=False
        )

        self.dataType = dataType
        self._isArrayType = self._arrayTypeCheck(dataType)
        self._converter = self._generateConverter(
            dataType, self._isArrayType, connection
        )
        self.enumOptions = enumOptions

    def checkAndConvertIgnoreEnumOptions(self, value: Any, fieldName: str = "value"):
        if not self._isArrayType and isinstance(value, list):
            return [
                self._converter(v, f"{fieldName}[{i}]") for i, v in enumerate(value)
            ]
        return self._converter(value, fieldName)

    def checkAndConvert(self, value: Any, fieldName: str = "value", allowNone=True):
        if allowNone and value is None:
            return None
        result = self._converter(value, fieldName)
        if self._isArrayType:
            if self._enumOptions:
                for i, v in enumerate(result):
                    if v not in self._enumOptions:
                        raise ValueError(
                            f"Value of field '{fieldName}[{i}]' must be out of enumOptions. (Value '{Tools.truncString(str(v))}' is not accepted)"
                        )
        else:
            if self._enumOptions and result not in self._enumOptions:
                raise ValueError(
                    f"Value of field '{fieldName}' must be out of enumOptions. (Value '{Tools.truncString(str(result))}' is not accepted)"
                )

        return result

    @property
    def enumOptions(self) -> Any:
        return self._enumOptions

    @enumOptions.setter
    def enumOptions(self, value: Any):
        if not value:
            self._enumOptions = None
            return

        self._enumOptions = Tools.checkAndConvert(
            value, list, "enumOptions", allowNone=False
        )
