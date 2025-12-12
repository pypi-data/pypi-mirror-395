from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.ITypedEntity import ITypedEntity

if TYPE_CHECKING:
    pass


class DatasetTemplate(ConnectedEntity, ITypedEntity, IOwnedEntity, IProjectBased):
    _id: int = 0
    _datasetTemplates: Optional[list] = None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        self._id = Tools.checkAndConvert(value, int, "id")
