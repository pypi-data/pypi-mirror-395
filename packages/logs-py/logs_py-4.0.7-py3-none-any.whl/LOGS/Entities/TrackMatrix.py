from typing import Optional

from LOGS.Entities.Track import Track
from LOGS.Entities.TrackMatrixData import TrackMatrixData


class TrackMatrix(Track):
    _datatracks: Optional[TrackMatrixData] = None

    def _fetchData(self):
        if self.datatracks:
            if self.datatracks.matrix:
                self.datatracks.matrix.fetchFull()

    def __iter__(self):
        if self.datatracks is not None and self.datatracks.matrix is not None:
            for i in self.datatracks.matrix:
                yield i[0], i[1], self.datatracks.matrix.getValueFromIndex(i)

    @property
    def datatracks(self) -> Optional[TrackMatrixData]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkAndConvertNullable(
            value, TrackMatrixData, "datatracks"
        )
