from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Method import Method
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(Method)
class MethodMinimal(EntityMinimalWithStrId[Method]):
    pass
