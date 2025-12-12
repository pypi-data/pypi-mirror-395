from io import BytesIO
from typing import Optional, cast

import PIL.Image
from PIL.Image import Image

from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Entities.Datatrack import Datatrack


class DatatrackImage(Datatrack):
    _type = "image"
    _data: Optional[Image] = None

    def _fetchData(self):
        super()._fetchData()

        if self._data:
            self._data = PIL.Image.open(BytesIO(cast(bytes, self._data)))

    @property
    def data(self) -> Optional[Image]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
