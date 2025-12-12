from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Person import Person
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Person)
class PersonMinimal(EntityMinimalWithIntId[Person]):
    pass
