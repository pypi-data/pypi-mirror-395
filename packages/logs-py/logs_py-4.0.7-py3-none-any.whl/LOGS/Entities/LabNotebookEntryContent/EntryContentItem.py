from typing import Optional

from LOGS.Entity.SerializableContent import SerializableContent


class EntryContentItem(SerializableContent):
    __type: str = "Unknown"
    _type: Optional[str] = None

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "type" not in ref or not ref["type"]:
                raise ValueError(
                    f"EntryContentItem must contain a 'type' field. (Got '{self.truncString(str(ref))}')"
                )

        super().fromDict(ref)

    @property
    def type(self) -> str:
        if type(self) == EntryContentItem:
            return self.__type

        if self._type:
            return self._type
        else:
            raise ValueError(f"Field 'type' in class {type(self).__name__} is not set.")

    @type.setter
    def type(self, value):
        if type(self) != EntryContentItem:
            if self._type != value:
                raise ValueError(
                    f"Field 'type' in class {type(self).__name__} is not mutable. (Got '{self.truncString(str(value))}' expected '{self._type}')"
                )
            return
        self.__type = self.checkAndConvertNullable(value, str, "type")
