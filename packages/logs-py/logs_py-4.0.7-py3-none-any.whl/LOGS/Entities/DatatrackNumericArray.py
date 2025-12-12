from typing import Optional, cast

import numpy as np

from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Entities.Datatrack import Datatrack


class DatatrackNumericArray(Datatrack):
    _type = "numeric_array"
    _data: Optional[np.ndarray] = None

    def __iter__(self):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is not None:
            for x in self._data:
                yield x

    def _fetchData(self):
        super()._fetchData()

        if self._data:
            self._data = np.frombuffer(cast(bytes, self._data), dtype=np.double)

    @property
    def data(self) -> Optional[np.ndarray]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
