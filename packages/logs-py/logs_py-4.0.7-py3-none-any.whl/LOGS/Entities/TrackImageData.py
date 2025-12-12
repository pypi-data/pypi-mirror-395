from typing import Optional

from LOGS.Entities.DatatrackImage import DatatrackImage
from LOGS.Entities.TrackData import TrackData


class TrackImageData(TrackData):
    _image: Optional[DatatrackImage] = None

    def fetchFull(self):
        if self.image:
            self.image.fetchFull()

    @property
    def image(self) -> Optional[DatatrackImage]:
        return self._image

    @image.setter
    def image(self, value):
        self._image = self.checkAndConvertNullable(value, DatatrackImage, "image")
