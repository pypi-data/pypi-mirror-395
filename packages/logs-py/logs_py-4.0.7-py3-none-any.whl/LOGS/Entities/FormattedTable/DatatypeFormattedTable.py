import sys
from typing import Dict, List, Literal, Optional, Union

from LOGS.Entities.FormattedTable.DatatypeFormattedTableCell import (
    DatatypeFormattedTableCell,
)
from LOGS.Entity.SerializableContent import SerializableContent

_VTypeType = Literal["int", "float", "str", "bool"]


class DatatypeFormattedTable(SerializableContent):
    _type: str = "formatted_table"
    _name: Optional[str] = None
    _id = ""

    _cells: List[DatatypeFormattedTableCell] = []

    _rowRange: List[int] = [sys.maxsize, -1]
    _columnRange: List[int] = [sys.maxsize, -1]

    _cellIds: Dict[str, int] = {}

    _fixedRow: Optional[int] = None
    _fixedColumn: Optional[int] = None

    def appendCell(
        self,
        cell: Union[_VTypeType, DatatypeFormattedTableCell],
        row: int = -1,
        column: int = -1,
    ) -> DatatypeFormattedTableCell:
        c = self.checkAndConvert(
            cell, fieldName="cell", fieldType=DatatypeFormattedTableCell
        )
        if row >= 0:
            c.row = row
        if column >= 0:
            c.column = column

        id = c.id
        index = self.getCell(id)
        if index >= 0:
            self.cells[index] = c
        else:
            self._cellIds[id] = len(self.cells)
            self.cells.append(c)

        # self.reorganizeCells()

        return c

    def getCell(self, id: str) -> int:
        if id in self._cellIds:
            return self._cellIds[id]
        return -1

    # def addCellId(self, cell: DatatypeFormattedTableCell):
    #     self.cells.sort(key=lambda c: (c.row, c.column))
    #     self._cellIds = {c.id: i for i, c in enumerate(self.cells)}
    #     self._cellIds[cell.id] = cell

    def reorganizeCells(self):
        self.cells.sort(key=lambda c: c.column)
        self._columnRange = [self.cells[0].column, self.cells[-1].column]
        self.cells.sort(key=lambda c: (c.row, c.column))
        self._rowRange = [self.cells[0].row, self.cells[-1].row]
        self._cellIds = {c.id: i for i, c in enumerate(self.cells)}

    def toDict(self, validate=False):
        self.reorganizeCells()
        return super().toDict()

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cells(self) -> List[DatatypeFormattedTableCell]:
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = self.checkListAndConvert(
            value, fieldName="cells", fieldType=DatatypeFormattedTableCell
        )
        self.reorganizeCells()

    @property
    def rowRange(self) -> List[int]:
        return self._rowRange

    @property
    def columnRange(self) -> List[int]:
        return self._columnRange

    @property
    def fixedRow(self) -> Optional[int]:
        return self._fixedRow

    @fixedRow.setter
    def fixedRow(self, value):
        self._fixedRow = self.checkAndConvert(
            value, fieldName="fixedRow", fieldType=int, allowNone=True
        )

    @property
    def fixedColumn(self) -> Optional[int]:
        return self._fixedColumn

    @fixedColumn.setter
    def fixedColumn(self, value):
        self._fixedColumn = self.checkAndConvert(
            value, fieldName="fixedColumn", fieldType=int, allowNone=True
        )
