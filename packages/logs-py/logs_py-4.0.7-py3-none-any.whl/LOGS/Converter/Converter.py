from typing import Any, Dict, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Converter.ConverterParameter import IConverterParameter
from LOGS.Converter.ExportParameters import ExportParameters
from LOGS.Entity.SerializableContent import SerializableContent


class Converter(SerializableContent):
    _formatId: Optional[str] = None
    _exportId: Optional[str] = None
    _version: Optional[str] = None
    _name: Optional[str] = None
    _id: Optional[str] = None
    _parameters: Optional[List[IConverterParameter]] = None

    def __init__(self, ref=None):
        t = type(self)

        self._noSerialize += [
            t.parameters.fget.__name__,  # type: ignore
        ]

        super().__init__(ref)

    def __str__(self):
        return Tools.ObjectToString(self)

    @property
    def formatId(self) -> Optional[str]:
        return self._formatId

    @formatId.setter
    def formatId(self, value):
        self._formatId = self.checkAndConvertNullable(value, str, "formatId")

    @property
    def exportId(self) -> Optional[str]:
        return self._exportId

    @exportId.setter
    def exportId(self, value):
        self._exportId = self.checkAndConvertNullable(value, str, "exportId")

    @property
    def version(self) -> Optional[str]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvertNullable(value, str, "version")

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, str, "id")

    @property
    def requestParameter(self) -> Optional[ExportParameters]:
        if self.parameters is None:
            return None

        p: Dict[str, Any] = {p.id: None for p in self.parameters if p.id}
        p["_parentId"] = self.id
        return ExportParameters(
            ref=p,
            types={
                p.id: IConverterParameter.TypeMapper(p.type)
                for p in self.parameters
                if p.id
            },
        )

    @property
    def parameters(self) -> Optional[List[IConverterParameter]]:
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = self.checkListAndConvertNullable(
            value,
            fieldType=IConverterParameter,
            converter=IConverterParameter.GetParameterFromDict,
            fieldName="parameters",
        )
