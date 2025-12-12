from typing import List, Literal, Optional, Union

from LOGS.Parameters.ParameterBase import ParameterBase

ColumnTypesType = Literal["int", "float", "str", "bool"]
TableType = Union[str, int, float, None]


class ParameterTable(ParameterBase):
    _type = "table"

    _columnNumber: int = 0
    _columnTypes: List[ColumnTypesType] = []
    _columnDecimals: List[Optional[int]] = []
    _columnNames: List[str] = []
    _table: List[List[TableType]] = []

    @property
    def columnNumber(self) -> int:
        return self._columnNumber

    @columnNumber.setter
    def columnNumber(self, value):
        if not isinstance(value, int) or value < 0:
            value = 0
        self._columnNumber = value

    @property
    def columnTypes(self) -> List[ColumnTypesType]:
        return self._columnTypes

    @columnTypes.setter
    def columnTypes(self, value):
        self._columnTypes = self.checkListAndConvert(
            value, str, fieldName="columnTypes"  # type: ignore
        )

    @property
    def columnDecimals(self) -> List[Optional[int]]:
        return self._columnDecimals

    @columnDecimals.setter
    def columnDecimals(self, value):
        self._columnDecimals = self.checkListAndConvert(
            value, fieldType=int, fieldName="columnDecimals", allowNone=True
        )

    @property
    def columnNames(self) -> List[str]:
        return self._columnNames

    @columnNames.setter
    def columnNames(self, value):
        self._columnNames = self.checkListAndConvert(
            value, fieldType=str, fieldName="columnNames", allowNone=True
        )

    @property
    def table(self) -> List[List[TableType]]:
        return self._table

    @table.setter
    def table(self, value):
        self._table = value
