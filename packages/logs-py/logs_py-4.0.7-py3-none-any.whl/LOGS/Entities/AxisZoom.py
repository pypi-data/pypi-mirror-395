from typing import List, Optional

from LOGS.Entity.SerializableContent import SerializableContent


class AxisZoom(SerializableContent):
    _x: Optional[List[float]] = None
    _y: Optional[List[float]] = None
    _z: Optional[List[float]] = None

    @property
    def x(self) -> Optional[List[float]]:
        return self._x

    @x.setter
    def x(self, value):
        self._x = self.checkListAndConvertNullable(value, float, "x")

    @property
    def y(self) -> Optional[List[float]]:
        return self._y

    @y.setter
    def y(self, value):
        self._y = self.checkListAndConvertNullable(value, float, "y")

    @property
    def z(self) -> Optional[List[float]]:
        return self._z

    @z.setter
    def z(self, value):
        self._z = self.checkListAndConvertNullable(value, float, "z")
