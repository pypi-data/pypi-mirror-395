from typing import Optional

from LOGS.Entities.Track import Track
from LOGS.Entities.TrackImageData import TrackImageData


class TrackImage(Track):
    _datatracks: Optional[TrackImageData] = None

    def _fetchData(self):
        if self.datatracks:
            if self.datatracks.image:
                self.datatracks.image.fetchFull()

    @property
    def datatracks(self) -> Optional[TrackImageData]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkAndConvertNullable(value, TrackImageData, "data")
