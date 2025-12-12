from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Project import Project
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Project)
class ProjectMinimal(EntityMinimalWithIntId[Project]):
    pass
