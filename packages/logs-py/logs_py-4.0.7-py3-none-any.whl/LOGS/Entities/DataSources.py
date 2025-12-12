from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.DataSource import DataSource
from LOGS.Entities.DataSourceRequestParameter import DataSourceRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("data_sources")
class DataSources(EntityIterator[DataSource, DataSourceRequestParameter]):
    """LOGS connected class DataSource iterator"""

    _generatorType = DataSource
    _parameterType = DataSourceRequestParameter
