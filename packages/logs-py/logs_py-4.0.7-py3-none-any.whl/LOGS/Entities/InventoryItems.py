from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.InventoryItem import InventoryItem
from LOGS.Entities.InventoryItemRequestParameter import InventoryItemRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("inventory_items")
class InventoryItems(EntityIterator[InventoryItem, InventoryItemRequestParameter]):
    """LOGS connected InventoryItems iterator"""

    _generatorType = InventoryItem
    _parameterType = InventoryItemRequestParameter
