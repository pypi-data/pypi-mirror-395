from typing import Optional

from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.InventoryItem import InventoryItem
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(InventoryItem)
class InventoryItemMinimal(EntityMinimalWithIntId[InventoryItem]):
    _inventoryName: Optional[str] = None

    @property
    def inventoryName(self) -> Optional[str]:
        return self._inventoryName

    @inventoryName.setter
    def inventoryName(self, value):
        self._inventoryName = self.checkAndConvert(
            value, str, "inventoryName", allowNone=True
        )

    def __str__(self):
        s = f" class:'{self.inventoryName}'" if self.inventoryName else ""
        s += " name:'%s'" % (self.name if self.name else "")
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)
