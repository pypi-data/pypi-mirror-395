from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Role import Role
from LOGS.Entities.RoleRequestParameter import RoleRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("Roles")
class Roles(EntityIterator[Role, RoleRequestParameter]):
    """LOGS connected Person iterator"""

    _generatorType = Role
    _parameterType = RoleRequestParameter
