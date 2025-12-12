from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.CustomType import CustomType
from LOGS.Entities.CustomTypeRequestParameter import CustomTypeRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("types")
class CustomTypes(EntityIterator[CustomType, CustomTypeRequestParameter]):
    """LOGS connected CustomTypes iterator"""

    _generatorType = CustomType
    _parameterType = CustomTypeRequestParameter
