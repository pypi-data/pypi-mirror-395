from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Bridge import Bridge
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Bridge)
class BridgeMinimal(EntityMinimalWithIntId[Bridge]):
    pass
