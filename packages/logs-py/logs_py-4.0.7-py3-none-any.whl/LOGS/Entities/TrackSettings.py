from typing import Optional

from LOGS.Entities.AxisNaming import AxisNaming
from LOGS.Entities.AxisZoom import AxisZoom
from LOGS.Entity.SerializableContent import SerializableContent


class TrackSettings(SerializableContent):
    """LOGS general Track settings"""

    _color: Optional[str] = None
    _axisUnits: Optional[AxisNaming] = None
    _axisLabels: Optional[AxisNaming] = None
    _visible: Optional[bool] = None
    _zoom: Optional[AxisZoom] = None

    @property
    def color(self) -> Optional[str]:
        return self._color

    @color.setter
    def color(self, value):
        self._color = self.checkAndConvertNullable(value, str, "color")

    @property
    def axisUnits(self) -> Optional[AxisNaming]:
        return self._axisUnits

    @axisUnits.setter
    def axisUnits(self, value):
        self._axisUnits = self.checkAndConvertNullable(value, AxisNaming, "axisUnits")

    @property
    def axisLabels(self) -> Optional[AxisNaming]:
        return self._axisLabels

    @axisLabels.setter
    def axisLabels(self, value):
        self._axisLabels = self.checkAndConvertNullable(value, AxisNaming, "axisLabels")

    @property
    def visible(self) -> Optional[bool]:
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = self.checkAndConvertNullable(value, bool, "visible")

    @property
    def zoom(self) -> Optional[AxisZoom]:
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = self.checkAndConvertNullable(value, AxisZoom, "zoom")
