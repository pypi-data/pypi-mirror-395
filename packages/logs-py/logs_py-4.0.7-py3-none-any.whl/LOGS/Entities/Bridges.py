from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Bridge import Bridge
from LOGS.Entities.BridgeRequestParameter import BridgeRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("bridges")
class Bridges(EntityIterator[Bridge, BridgeRequestParameter]):
    """LOGS connected class Bridges iterator"""

    _generatorType = Bridge
    _parameterType = BridgeRequestParameter
