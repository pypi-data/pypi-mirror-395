from enum import Enum
from typing import Optional, Union

from LOGS.Entity.SerializableContent import SerializableClass


class ParameterType(Enum):
    Integer = "Integer"
    String = "String"
    Boolean = "Boolean"
    Float = "Float"


class IConverterParameter(SerializableClass):
    name: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    hasDefault: Optional[bool] = None
    identifier: Optional[str] = None

    @classmethod
    def TypeMapper(cls, t: Union[ParameterType, str]):
        if t == ParameterType.Integer:
            return int
        if t == ParameterType.String:
            return str
        if t == ParameterType.Boolean:
            return bool
        if t == ParameterType.Float:
            return float
        raise Exception("Unknown parameter type '%s'" % t)

    @classmethod
    def GetParameterFromDict(cls, data: dict):
        if not isinstance(data, dict) or "type" not in data:
            raise Exception(f"Export parameter type not specified.")

        type = data["type"]
        if type not in ParameterType.__members__:
            raise Exception(
                f"Unknown export parameter type '{type}' not found in parameter data"
            )

        type = ParameterType.__members__[type]

        if type == ParameterType.Integer:
            return ConverterIntegerParameter(data)
        if type == ParameterType.String:
            return ConverterStringParameter(data)
        if type == ParameterType.Boolean:
            return ConverterBooleanParameter(data)
        if type == ParameterType.Float:
            return ConverterFloatParameter(data)

        raise Exception(
            f"Unknown export parameter type '{type}' not found in parameter data"
        )

    @property
    def type(self) -> ParameterType:
        raise NotImplementedError(
            f"{type(self).__name__} is an abstract class. Please implement the 'type' property."
        )


class ConverterIntegerParameter(IConverterParameter):
    @property
    def type(self) -> ParameterType:
        return ParameterType.Integer


class ConverterStringParameter(IConverterParameter):
    @property
    def type(self) -> ParameterType:
        return ParameterType.String


class ConverterBooleanParameter(IConverterParameter):
    @property
    def type(self) -> ParameterType:
        return ParameterType.Boolean


class ConverterFloatParameter(IConverterParameter):
    @property
    def type(self) -> ParameterType:
        return ParameterType.Float
