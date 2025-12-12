from typing import Any, Optional, cast

from LOGS.Auxiliary.Exceptions import IllegalFieldValueException
from LOGS.Interfaces.IEntityInterface import IEntityInterface


class ILiteraryTypedEntity(IEntityInterface):
    _type: str = cast(Any, None)

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, value):
        if value != self._type:
            raise IllegalFieldValueException(
                self, "type", value, f"Only value '{self._type}' allowed."
            )
