from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities import DataFormat
from LOGS.Entities.DataFormatRequestParameter import DataFormatRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("data_formats")
class DataFormats(EntityIterator[DataFormat, DataFormatRequestParameter]):
    """LOGS connected Formats iterator"""

    _generatorType = DataFormat
    _parameterType = DataFormatRequestParameter
