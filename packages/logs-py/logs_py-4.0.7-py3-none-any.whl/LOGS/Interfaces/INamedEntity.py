from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class INamedEntityRequest:
    names: Optional[List[str]] = None


class INamedEntity(IEntityInterface):
    _name: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = Tools.checkAndConvert(value, str, "name", allowNone=True)
