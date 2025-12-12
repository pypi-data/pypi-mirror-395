from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Vendor import Vendor
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(Vendor)
class VendorMinimal(EntityMinimalWithStrId[Vendor]):
    pass
