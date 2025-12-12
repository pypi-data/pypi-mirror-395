from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Dataset import Dataset
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Dataset)
class DatasetMinimal(EntityMinimalWithIntId[Dataset]):
    pass
