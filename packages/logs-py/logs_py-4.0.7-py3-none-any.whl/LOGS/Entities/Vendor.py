from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("vendors")
class Vendor(EntityWithStrId, INamedEntity):
    _description: Optional[str]
    _icon: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._description = None
        self._icon = None
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def icon(self) -> Optional[str]:
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = self.checkAndConvertNullable(value, str, "icon")
