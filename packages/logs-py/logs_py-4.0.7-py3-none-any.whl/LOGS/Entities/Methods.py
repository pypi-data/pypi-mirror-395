from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Method import Method
from LOGS.Entities.MethodRequestParameter import MethodRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("methods")
class Methods(EntityIterator[Method, MethodRequestParameter]):
    """LOGS connected class FormatMethod iterator"""

    _generatorType = Method
    _parameterType = MethodRequestParameter
