from typing import Optional

from LOGS.Entities.DatatrackNumericArray import DatatrackNumericArray
from LOGS.Entities.TrackData import TrackData


class TrackXYData(TrackData):
    _x: Optional[DatatrackNumericArray] = None
    _y: Optional[DatatrackNumericArray] = None

    def fetchFull(self):
        if self.x:
            self.x.fetchFull()
        if self.y:
            self.y.fetchFull()

    @property
    def x(self) -> Optional[DatatrackNumericArray]:
        return self._x

    @x.setter
    def x(self, value):
        self._x = self.checkAndConvertNullable(value, DatatrackNumericArray, "x")

    @property
    def y(self) -> Optional[DatatrackNumericArray]:
        return self._y

    @y.setter
    def y(self, value):
        self._y = self.checkAndConvertNullable(value, DatatrackNumericArray, "y")
