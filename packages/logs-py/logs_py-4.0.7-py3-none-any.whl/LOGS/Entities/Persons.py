from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Person import Person
from LOGS.Entities.PersonRequestParameter import PersonRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("persons")
class Persons(EntityIterator[Person, PersonRequestParameter]):
    """LOGS connected Person iterator"""

    _generatorType = Person
    _parameterType = PersonRequestParameter
