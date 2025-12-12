from typing import List, Optional

from LOGS.Entity.SerializableContent import SerializableContent


class ParserLog(SerializableContent):
    _type: Optional[str] = None
    _message: Optional[str] = None
    _description: Optional[List[str]] = None
    _code: Optional[int] = None

    def __init__(self, ref=None):
        super().__init__(ref=ref)

    def __str__(self):
        error = f" ({self.code})" if self.code else ""
        return f"{type(self).__name__}.{self.type}{error}: {self.message}"

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, str, "type")

    @property
    def message(self) -> Optional[str]:
        return self._message

    @message.setter
    def message(self, value):
        self._message = self.checkAndConvertNullable(value, str, "message")

    @property
    def description(self) -> Optional[List[str]]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkListAndConvertNullable(value, str, "description")

    @property
    def code(self) -> Optional[int]:
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.checkAndConvertNullable(value, int, "code")
