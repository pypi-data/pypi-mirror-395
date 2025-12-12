from typing import Optional, TypeVar

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute


class TextMarkAttributeDefault(BasicAttribute):
    pass


_T = TypeVar("_T", bound=BasicAttribute)


class TextMarkAttributeTextColor(BasicAttribute):
    _color: Optional[str] = None

    @property
    def color(self) -> Optional[str]:
        return self._color

    @color.setter
    def color(self, value):
        self._color = self.checkAndConvertNullable(value, str, "color")


class TextMarkAttributeTextHighlight(BasicAttribute):
    _highlight: Optional[str] = None

    @property
    def highlight(self) -> Optional[str]:
        return self._highlight

    @highlight.setter
    def highlight(self, value):
        self._highlight = self.checkAndConvertNullable(value, str, "highlight")


class TextMarkAttributeLink(BasicAttribute):
    _auto: Optional[bool] = None
    _href: Optional[str] = None
    _target: Optional[str] = None

    @property
    def auto(self) -> Optional[bool]:
        return self._auto

    @auto.setter
    def auto(self, value):
        self._auto = self.checkAndConvertNullable(value, bool, "auto")

    @property
    def href(self) -> Optional[str]:
        return self._href

    @href.setter
    def href(self, value):
        self._href = self.checkAndConvertNullable(value, str, "href")

    @property
    def target(self) -> Optional[str]:
        return self._target

    @target.setter
    def target(self, value):
        self._target = self.checkAndConvertNullable(value, str, "target")
