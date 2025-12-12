from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.SharedContent import SharedContent
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(SharedContent)
class SharedContentMinimal(EntityMinimalWithIntId[SharedContent]):
    pass
