from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.DataSourceStatus import DataSourceStatus
from LOGS.Entities.DataSourceStatusRequestParameter import (
    DataSourceStatusRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("data_sources_status")
class DataSourceStatusIterator(
    EntityIterator[DataSourceStatus, DataSourceStatusRequestParameter]
):
    """LOGS connected class DataSourceStatus iterator"""

    _generatorType = DataSourceStatus
    _parameterType = DataSourceStatusRequestParameter
