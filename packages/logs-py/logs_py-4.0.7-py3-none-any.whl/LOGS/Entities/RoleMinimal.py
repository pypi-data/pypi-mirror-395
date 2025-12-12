from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Role import Role
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Role)
class RoleMinimal(EntityMinimalWithIntId[Role]):
    pass
