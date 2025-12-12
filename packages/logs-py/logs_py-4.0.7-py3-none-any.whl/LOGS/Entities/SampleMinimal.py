from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Sample import Sample
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Sample)
class SampleMinimal(EntityMinimalWithIntId[Sample]):
    pass
