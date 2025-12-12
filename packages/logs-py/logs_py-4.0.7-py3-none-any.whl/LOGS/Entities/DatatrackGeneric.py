from typing import Optional, cast

from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Entities.Datatrack import Datatrack


class DatatrackGeneric(Datatrack):
    _type = "formatted_table"
    _data: Optional[str] = None

    def _fetchData(self):
        super()._fetchData()

        if self._data is not None:
            s = cast(bytes, self._data)
            try:
                self._data = s.decode()
                return
            except:
                pass

            try:
                self._data = s.decode("latin-1")
                return
            except:
                pass

            self._data = None

    @property
    def data(self) -> Optional[str]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
