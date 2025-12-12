from typing import Literal, Optional, Union

from LOGS.Entities.FormattedTable.DatatypeFormattedTableSettings import (
    DatatypeFormattedTableSettings,
)
from LOGS.Entity.SerializableContent import SerializableContent

_VTypeType = Literal["int", "float", "str", "bool"]
_ValueType = Union[str, int, float, bool, None]


class DatatypeFormattedTableCell(SerializableContent):
    __vtype = {"int": int, "float": float, "str": str, "bool": bool}

    _id: str = ""
    _type: str = "formatted_table_cell"
    _value: Optional[_ValueType] = None
    _vtype: _VTypeType = "str"
    _row: int = 0
    _column: int = 0
    _settings: Optional[DatatypeFormattedTableSettings] = None

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self) -> _ValueType:
        return self._value

    @value.setter
    def value(self, value):
        vtype = self.vtype if self.vtype else type(value).__name__

        converter = self.__vtype.get(vtype, None)
        if converter:
            try:
                self._value = converter(value)
                self._vtype = vtype
            except:
                raise Exception(
                    "ERROR: could not convert "
                    + "' value '"
                    + value
                    + "' to type '"
                    + value
                    + "'"
                )
        else:
            raise Exception(
                "Unknown vtype %a. (Expected one of '%s')"
                % (vtype, ", ".join(self.__vtype.keys()))
            )

    @property
    def vtype(self) -> _VTypeType:
        return self._vtype

    @vtype.setter
    def vtype(self, value):
        if value not in self.__vtype:
            raise Exception(
                "Unknown vtype %a. (Expected one of '%s')"
                % (value, ", ".join(self.__vtype.keys()))
            )
        self._vtype = value

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def column(self) -> int:
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def id(self) -> str:
        return f"{self.row}x{self.column}"

    @property
    def settings(self) -> Optional[DatatypeFormattedTableSettings]:
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = self.checkAndConvert(
            value, fieldName="settings", fieldType=DatatypeFormattedTableSettings
        )
