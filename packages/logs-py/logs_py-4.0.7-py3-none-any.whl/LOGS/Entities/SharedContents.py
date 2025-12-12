from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.SharedContent import SharedContent
from LOGS.Entities.SharedContentRequestParameter import SharedContentRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("shared_content")
class SharedContents(EntityIterator[SharedContent, SharedContentRequestParameter]):
    """LOGS connected SharedContents iterator"""

    _generatorType = SharedContent
    _parameterType = SharedContentRequestParameter
