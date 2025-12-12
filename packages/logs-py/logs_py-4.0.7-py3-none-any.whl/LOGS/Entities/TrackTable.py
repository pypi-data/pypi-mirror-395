from typing import Optional

from LOGS.Entities.Track import Track
from LOGS.Entities.TrackTableData import TrackTableData


class TrackTable(Track):
    _datatracks: Optional[TrackTableData] = None

    def _fetchData(self):
        if self.datatracks:
            if self.datatracks.table:
                self.datatracks.table.fetchFull()

    @property
    def datatracks(self) -> Optional[TrackTableData]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkAndConvertNullable(value, TrackTableData, "data")
