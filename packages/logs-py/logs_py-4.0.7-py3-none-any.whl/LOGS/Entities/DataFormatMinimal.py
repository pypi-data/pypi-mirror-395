from typing import List, Optional

from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.DataFormat import DataFormat
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(DataFormat)
class DataFormatMinimal(EntityMinimalWithStrId[DataFormat]):
    _version: Optional[List[str]] = None

    @property
    def version(self) -> Optional[List[str]]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkListAndConvertNullable(value, str, "version")
