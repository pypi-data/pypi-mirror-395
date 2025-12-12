from typing import Optional, Tuple, cast

import numpy as np

from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Entities.Datatrack import Datatrack


class DatatrackNumericMatrix(Datatrack):
    _type = "numeric_matrix"
    _data: Optional[np.ndarray] = None

    def __iter__(self):
        if self._incomplete:
            raise EntityIncompleteException(self)

        if self.size is None:
            raise ValueError("Datatrack has no size defined.")

        if self._data is not None:
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    yield x, y

    def _fetchData(self):
        super()._fetchData()

        if self._data and self.size and len(self.size) > 1:
            self._data = np.frombuffer(cast(bytes, self._data), dtype=np.double)
            self._data = self._data.reshape((self.size[1], self.size[0]))
            self._data = self._data.T

    def getCoordinate(self, index: Tuple[int, int]):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self.min is None or self.max is None or self.size is None:
            return None

        return (
            self.min[0] + index[0] * (self.max[0] - self.min[0]) / self.size[0],
            self.min[1] + index[1] * (self.max[1] - self.min[1]) / self.size[1],
        )

    def getIndex(
        self, coord: Tuple[float, float], keepInBounds: bool = False
    ) -> Tuple[int, int]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self.min is None or self.max is None or self.size is None:
            raise ValueError("Datatrack has no min, max or size defined.")

        index = (
            int((coord[0] - self.min[0]) * self.size[0] / (self.max[0] - self.min[0])),
            int((coord[1] - self.min[1]) * self.size[1] / (self.max[1] - self.min[1])),
        )

        if keepInBounds:
            index = (
                max(0, min(index[0], self.size[0] - 1)),
                max(0, min(index[1], self.size[1] - 1)),
            )

        return index

    def getValueFromCoordinate(
        self, coord: Tuple[float, float], keepInBounds: bool = True
    ):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is None:
            return None

        return self.getValueFromIndex(self.getIndex(coord, keepInBounds=keepInBounds))

    def getValueFromIndex(self, index: Tuple[int, int]):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is None:
            return None

        if self.size is None:
            raise ValueError("Datatrack has no size defined.")

        if (
            index[0] < 0
            or index[0] >= self.size[0]
            or index[1] < 0
            or index[1] >= self.size[1]
        ):
            raise ValueError("Index out of bounds.")

        return self._data[index]

    @property
    def data(self) -> Optional[np.ndarray]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
