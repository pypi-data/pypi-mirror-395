from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.CustomType import CustomType
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(CustomType)
class CustomTypeMinimal(EntityMinimalWithIntId[CustomType]):
    pass
