from typing import Optional

from LOGS.Entities.Track import Track
from LOGS.Entities.TrackXYComplexData import TrackXYComplexData


class TrackXYComplex(Track):
    _datatracks: Optional[TrackXYComplexData] = None

    def _fetchData(self):
        if self.datatracks:
            if self.datatracks.x:
                self.datatracks.x.fetchFull()
            if self.datatracks.re:
                self.datatracks.re.fetchFull()
            if self.datatracks.im:
                self.datatracks.im.fetchFull()

    def __iter__(self):
        if (
            self.datatracks is not None
            and self.datatracks.x is not None
            and self.datatracks.x.count is not None
            and self.datatracks.x.data is not None
            and self.datatracks.re is not None
            and self.datatracks.re.count is not None
            and self.datatracks.re.data is not None
            and self.datatracks.im is not None
            and self.datatracks.im.count is not None
            and self.datatracks.im.data is not None
        ):
            for i in range(
                min(
                    self.datatracks.x.count,
                    self.datatracks.re.count,
                    self.datatracks.im.count,
                )
            ):
                yield self.datatracks.x.data[i], self.datatracks.re.data[
                    i
                ], self.datatracks.im.data[i]

    @property
    def datatracks(self) -> Optional[TrackXYComplexData]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkAndConvertNullable(
            value, TrackXYComplexData, "datatracks"
        )
