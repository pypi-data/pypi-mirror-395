from typing import List, Optional

from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.Parameters.Color import Color


class ParameterBase(SerializableContent):
    _name: str = ""
    _tracks: Optional[List[str]] = None
    _colors: List[Color] = []
    _active: bool = True
    _type: str = "None"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvert(value, fieldType=str, fieldName="name")

    @property
    def tracks(self) -> Optional[List[str]]:
        return self._tracks

    @tracks.setter
    def tracks(self, value):
        self._tracks = self.checkListAndConvert(
            value, fieldType=str, fieldName="tracks"
        )

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value):
        self._active = bool(value)

    @property
    def colors(self) -> Optional[List[Color]]:
        if len(self._colors) < 1:
            return None

        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = self.checkListAndConvert(
            value, fieldType=Color, fieldName="colors"
        )

    @property
    def type(self) -> str:
        return self._type
