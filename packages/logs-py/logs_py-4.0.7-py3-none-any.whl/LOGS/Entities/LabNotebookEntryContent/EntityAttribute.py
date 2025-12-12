from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.BasicAttribute import BasicAttribute
from LOGS.Entity.SerializableContent import SerializableClass


class EntityAttributeSettings(SerializableClass):
    showHeader: Optional[bool] = None
    collapsible: Optional[bool] = None
    defaultCollapsed: Optional[bool] = None


class EntityAttributeAdditionalSettings(SerializableClass):
    height: Optional[int] = None
    showViewer: Optional[bool] = None


class EntityAttribute(BasicAttribute):
    _version: Optional[int] = None
    _entityId: Optional[int] = None
    _settings: Optional[EntityAttributeSettings] = None
    _additionalSettings: Optional[EntityAttributeAdditionalSettings] = None
    _entityUuid: Optional[str] = None
    _entityTypeId: Optional[str] = None
    _style: Optional[str] = None

    @property
    def style(self) -> Optional[str]:
        return self._style

    @style.setter
    def style(self, value):
        self._style = self.checkAndConvertNullable(value, str, "style")

    @property
    def entityTypeId(self) -> Optional[str]:
        return self._entityTypeId

    @entityTypeId.setter
    def entityTypeId(self, value):
        self._entityTypeId = self.checkAndConvertNullable(value, str, "entityTypeId")

    @property
    def entityUuid(self) -> Optional[str]:
        return self._entityUuid

    @entityUuid.setter
    def entityUuid(self, value):
        self._entityUuid = self.checkAndConvertNullable(value, str, "entityUuid")

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvertNullable(value, int, "version")

    @property
    def entityId(self) -> Optional[int]:
        return self._entityId

    @entityId.setter
    def entityId(self, value):
        self._entityId = self.checkAndConvertNullable(value, int, "entityId")

    @property
    def settings(self) -> Optional[EntityAttributeSettings]:
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = self.checkAndConvertNullable(
            value, EntityAttributeSettings, "settings"
        )

    @property
    def additionalSettings(self) -> Optional[EntityAttributeAdditionalSettings]:
        return self._additionalSettings

    @additionalSettings.setter
    def additionalSettings(self, value):
        self._additionalSettings = self.checkAndConvertNullable(
            value, EntityAttributeAdditionalSettings, "additionalSettings"
        )
