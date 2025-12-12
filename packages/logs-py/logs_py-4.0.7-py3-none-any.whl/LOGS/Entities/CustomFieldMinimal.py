from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.CustomField import CustomField
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(CustomField)
class CustomFieldMinimal(EntityMinimalWithIntId[CustomField]):
    pass
