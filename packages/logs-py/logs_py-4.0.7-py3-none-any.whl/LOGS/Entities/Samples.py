from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Sample import Sample
from LOGS.Entities.SampleRequestParameter import SampleRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("samples")
class Samples(EntityIterator[Sample, SampleRequestParameter]):
    """LOGS connected Samples iterator"""

    _generatorType = Sample
    _parameterType = SampleRequestParameter
