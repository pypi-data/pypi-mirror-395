from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("data_format_instruments")
class DataFormatInstrument(EntityWithStrId, INamedEntity):
    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")
