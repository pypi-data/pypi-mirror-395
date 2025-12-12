from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.DataFormatInstrumentMinimal import DataFormatInstrumentMinimal
    from LOGS.Entities.MethodMinimal import MethodMinimal
    from LOGS.Entities.VendorMinimal import VendorMinimal


class FormatMetaData(ConnectedEntity):
    _vendor: List["VendorMinimal"]
    _method: List["MethodMinimal"]
    _instrument: List["DataFormatInstrumentMinimal"]

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._vendor = []
        self._method = []
        self._format = []
        self._instrument = []
        super().__init__(ref=ref, connection=connection)

    @property
    def vendor(self) -> List["VendorMinimal"]:
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = MinimalModelGenerator.MinimalFromList(
            value, "VendorMinimal", "vendor", connection=self._getConnection()
        )

    @property
    def method(self) -> List["MethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MinimalModelGenerator.MinimalFromList(
            value, "MethodMinimal", "method", connection=self._getConnection()
        )

    @property
    def instrument(self) -> List["DataFormatInstrumentMinimal"]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = MinimalModelGenerator.MinimalFromList(
            value,
            "DataFormatInstrumentMinimal",
            "instrument",
            connection=self._getConnection(),
        )
