from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.DataFormatInstrument import DataFormatInstrument
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(DataFormatInstrument)
class DataFormatInstrumentMinimal(EntityMinimalWithStrId[DataFormatInstrument]):
    pass
