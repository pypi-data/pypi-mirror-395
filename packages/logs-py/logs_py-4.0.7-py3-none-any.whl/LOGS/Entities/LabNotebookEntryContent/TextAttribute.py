from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute


class TextAttribute(BasicAttribute):
    _style: Optional[str] = None
    _nodeIndent: Optional[int] = None
    _nodeLineHeight: Optional[int] = None
    _nodeTextAlignment: Optional[str] = None

    @property
    def style(self) -> Optional[str]:
        return self._style

    @style.setter
    def style(self, value):
        self._style = self.checkAndConvertNullable(value, str, "style")

    @property
    def nodeIndent(self) -> Optional[int]:
        return self._nodeIndent

    @nodeIndent.setter
    def nodeIndent(self, value):
        self._nodeIndent = self.checkAndConvertNullable(value, int, "nodeIndent")

    @property
    def nodeLineHeight(self) -> Optional[int]:
        return self._nodeLineHeight

    @nodeLineHeight.setter
    def nodeLineHeight(self, value):
        self._nodeLineHeight = self.checkAndConvertNullable(
            value, int, "nodeLineHeight"
        )

    @property
    def nodeTextAlignment(self) -> Optional[str]:
        return self._nodeTextAlignment

    @nodeTextAlignment.setter
    def nodeTextAlignment(self, value):
        self._nodeTextAlignment = self.checkAndConvertNullable(
            value, str, "nodeTextAlignment"
        )
