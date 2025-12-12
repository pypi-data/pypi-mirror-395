from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Vendor import Vendor
from LOGS.Entities.VendorRequestParameter import VendorRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("vendors")
class Vendors(EntityIterator[Vendor, VendorRequestParameter]):
    """LOGS connected class Vendors iterator"""

    _generatorType = Vendor
    _parameterType = VendorRequestParameter
