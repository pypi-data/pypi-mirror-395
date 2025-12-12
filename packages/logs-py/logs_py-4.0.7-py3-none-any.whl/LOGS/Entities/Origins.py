from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Origin import Origin
from LOGS.Entities.OriginRequestParameter import OriginRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("origins")
class Origins(EntityIterator[Origin, OriginRequestParameter]):
    """LOGS connected Person iterator"""

    _generatorType = Origin
    _parameterType = OriginRequestParameter
