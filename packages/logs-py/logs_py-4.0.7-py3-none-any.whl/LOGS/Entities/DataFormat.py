from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity


@Endpoint("data_formats")
class DataFormat(EntityWithStrId, INamedEntity, IGenericPermissionEntity):

    _description: Optional[str] = None
    _formatVersion: Optional[List[str]] = []
    _isCustom: Optional[bool] = None
    _version: Optional[str] = None
    _hasVisualization: Optional[bool] = None

    _vendors: List[str] = []
    _methods: List[str] = []
    _formats: List[str] = []
    _instruments: List[str] = []

    @property
    def formatVersion(self) -> Optional[List[str]]:
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, value):
        self._formatVersion = self.checkListAndConvertNullable(
            value, str, "formatVersion"
        )

    @property
    def vendors(self) -> List[str]:
        return self._vendors

    @vendors.setter
    def vendors(self, value):
        self._vendors = self.checkListAndConvert(value, str, "vendors")

    @property
    def methods(self) -> List[str]:
        return self._methods

    @methods.setter
    def methods(self, value):
        self._methods = self.checkListAndConvert(value, str, "methods")

    @property
    def formats(self) -> List[str]:
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = self.checkListAndConvert(value, str, "formats")

    @property
    def instruments(self) -> List[str]:
        return self._instruments

    @instruments.setter
    def instruments(self, value):
        self._instruments = self.checkListAndConvert(value, str, "instruments")

    @property
    def hasVisualization(self) -> Optional[bool]:
        return self._hasVisualization

    @hasVisualization.setter
    def hasVisualization(self, value: Optional[bool]):
        self._hasVisualization = self.checkAndConvertNullable(
            value, bool, "hasVisualization"
        )

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def isCustom(self) -> Optional[bool]:
        return self._isCustom

    @isCustom.setter
    def isCustom(self, value: Optional[bool]):
        self._isCustom = self.checkAndConvertNullable(value, bool, "isCustom")

    @property
    def version(self) -> Optional[str]:
        return self._version

    @version.setter
    def version(self, value: Optional[str]):
        self._version = self.checkAndConvertNullable(value, str, "version")
