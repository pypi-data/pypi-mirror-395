from typing import Optional

from LOGS.Entities.DatatrackFormattedTable import DatatrackFormattedTable
from LOGS.Entities.TrackData import TrackData


class TrackTableData(TrackData):
    _table: Optional[DatatrackFormattedTable] = None

    def fetchFull(self):
        if self.table:
            self.table.fetchFull()

    @property
    def table(self) -> Optional[DatatrackFormattedTable]:
        return self._table

    @table.setter
    def table(self, value):
        self._table = self.checkAndConvertNullable(
            value, DatatrackFormattedTable, "matrix"
        )
