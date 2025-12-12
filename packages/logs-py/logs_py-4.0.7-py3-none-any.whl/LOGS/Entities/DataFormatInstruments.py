from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.DataFormatInstrument import DataFormatInstrument
from LOGS.Entities.DataFormatInstrumentRequestParameter import (
    DataFormatInstrumentRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("data_format_instruments")
class DataFormatInstruments(
    EntityIterator[DataFormatInstrument, DataFormatInstrumentRequestParameter]
):
    """LOGS connected class DataFormatInstrument iterator"""

    _generatorType = DataFormatInstrument
    _parameterType = DataFormatInstrumentRequestParameter
