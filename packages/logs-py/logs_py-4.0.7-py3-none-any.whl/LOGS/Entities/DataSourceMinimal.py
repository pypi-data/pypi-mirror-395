from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.DataSource import DataSource
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(DataSource)
class DataSourceMinimal(EntityMinimalWithIntId[DataSource]):
    pass
