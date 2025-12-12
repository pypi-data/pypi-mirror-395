from typing import List, Optional

from LOGS.Entity.SerializableContent import SerializableContent


class SingleColor(SerializableContent):
    _color: str
    _offset: Optional[float]
    _value: Optional[float]

    @classmethod
    def bgrIntSigned32bit_to_hexcolor(cls, bgrInt: int):
        b = bgrInt & 2**8 - 1
        g = (bgrInt >> 8) & 2**8 - 1
        r = (bgrInt >> 16) & 2**8 - 1
        return "#%02x%02x%02x" % (r, g, b)

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def offset(self) -> Optional[float]:
        return self._offset

    @offset.setter
    def offset(self, value):
        value = self.checkAndConvert(
            value, fieldName="offset", fieldType=float, allowNone=True
        )
        if value < 0:
            raise Exception("Color offset value must be >= 0. (Got %f)" % value)
        if value > 1:
            raise Exception("Color offset value must be <= 1. (Got %f)" % value)
        self._offset = value

    @property
    def value(self) -> Optional[float]:
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Color(SerializableContent):
    _colors: List[SingleColor]
    _discrete: Optional[bool]
    _reverse: Optional[bool]

    def __init__(self, ref=None):
        if ref != None:
            if isinstance(ref, str):
                ref = {"colors": [ref]}
            elif isinstance(ref, list):
                ref = {"colors": ref}

        super().__init__(ref)

    @classmethod
    def bgrIntSigned32bit_to_hexcolor(cls, bgrInt: int):
        return SingleColor.bgrIntSigned32bit_to_hexcolor(bgrInt=bgrInt)

    @property
    def colors(self) -> List[SingleColor]:
        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = self.checkListAndConvert(
            value, fieldType=SingleColor, fieldName="colors"
        )

    @property
    def discrete(self) -> Optional[bool]:
        return self._discrete

    @discrete.setter
    def discrete(self, value):
        self._discrete = bool(value)

    @property
    def reverse(self) -> Optional[bool]:
        return self._reverse

    @reverse.setter
    def reverse(self, value):
        self._reverse = bool(value)
