from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Origin import Origin
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Origin)
class OriginMinimal(EntityMinimalWithIntId[Origin]):
    pass
