from typing import Optional

from LOGS.Entities.DatatrackNumericMatrix import DatatrackNumericMatrix
from LOGS.Entities.TrackData import TrackData


class TrackMatrixData(TrackData):
    _matrix: Optional[DatatrackNumericMatrix] = None

    def fetchFull(self):
        if self.matrix:
            self.matrix.fetchFull()

    @property
    def matrix(self) -> Optional[DatatrackNumericMatrix]:
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = self.checkAndConvertNullable(
            value, DatatrackNumericMatrix, "matrix"
        )
