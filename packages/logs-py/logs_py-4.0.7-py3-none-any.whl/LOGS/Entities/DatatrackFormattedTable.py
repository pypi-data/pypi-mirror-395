import json
from typing import Optional, cast

from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FormattedTable.DatatypeFormattedTable import DatatypeFormattedTable


class DatatrackFormattedTable(Datatrack):
    _type = "formatted_table"
    _data: Optional[DatatypeFormattedTable] = None

    def _fetchData(self):
        super()._fetchData()

        if self._data is not None:
            # s = cast(bytes, self._data).decode("utf-8")
            b = cast(bytes, self._data).split(b"\x00")[0]
            self._data = DatatypeFormattedTable(json.loads(b.decode("utf-8")))

    @property
    def data(self) -> Optional[DatatypeFormattedTable]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
