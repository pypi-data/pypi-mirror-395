from typing import Optional

from LOGS.Entity.SerializableContent import SerializableContent


class AxisNaming(SerializableContent):
    _x: Optional[str] = None
    _y: Optional[str] = None
    _z: Optional[str] = None

    @property
    def x(self) -> Optional[str]:
        return self._x

    @x.setter
    def x(self, value):
        self._x = self.checkAndConvertNullable(value, str, "x")

    @property
    def y(self) -> Optional[str]:
        return self._y

    @y.setter
    def y(self, value):
        self._y = self.checkAndConvertNullable(value, str, "y")

    @property
    def z(self) -> Optional[str]:
        return self._z

    @z.setter
    def z(self, value):
        self._z = self.checkAndConvertNullable(value, str, "z")
