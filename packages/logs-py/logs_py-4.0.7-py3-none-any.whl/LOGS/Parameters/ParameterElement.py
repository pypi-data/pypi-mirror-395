from typing import List, Literal, Optional, Union

from LOGS.Parameters.ParameterBase import ParameterBase

VTypeType = Literal["int", "float", "int[]", "float[]", "str"]
ValueType = Union[str, int, float, List[int], List[float], None]
FormatterType = Literal[
    "duration",
    "length",
    "voltage",
    "current",
    "pressure",
    "frequency",
    "magnetic",
    "epower",
]


class ParameterElement(ParameterBase):
    _type = "parameter"

    _vtype: VTypeType = "str"
    _value: ValueType = None
    _formatter: Optional[FormatterType] = None
    _unit: Optional[str] = None
    _delimiter: Optional[str] = None
    _decimalPlaces: Optional[int] = None
    _multiline: Optional[bool] = None

    @property
    def vtype(self) -> VTypeType:
        return self._vtype

    @vtype.setter
    def vtype(self, value):
        self._vtype = value

    @property
    def value(self) -> ValueType:
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def formattedValue(self) -> str:
        if self._unit:
            return str(self._value) + " " + self._unit

        return str(self._value)

    @property
    def formatter(self) -> Optional[FormatterType]:
        return self._formatter

    @formatter.setter
    def formatter(self, value):
        self._formatter = value

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    @property
    def multiline(self) -> Optional[bool]:
        return self._multiline

    @multiline.setter
    def multiline(self, value):
        self._multiline = value

    @property
    def delimiter(self) -> Optional[str]:
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        self._delimiter = value

    @property
    def decimalPlaces(self) -> Optional[int]:
        return self._decimalPlaces

    @decimalPlaces.setter
    def decimalPlaces(self, value):
        value = self.checkAndConvert(
            value, fieldName="decimalPlaces", fieldType=int, allowNone=True
        )
        if value < 0:
            raise Exception(
                "Decimal places must be zero or a positive integer number. (Got %a)"
                % value
            )
        self._decimalPlaces = value
