from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.CustomFieldModels import CustomTypeEntityType
from LOGS.Entities.CustomTypeSection import CustomTypeSection
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IHierarchyType import IHierarchyType
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal


@Endpoint("types")
class CustomType(
    IEntityWithIntId,
    IGenericPermissionEntity,
    INamedEntity,
    IUniqueEntity,
    IEntryRecord,
    IModificationRecord,
    ISoftDeletable,
    IHierarchyType,
):
    _noSerialize = ["connection", "cachePath", "cacheId", "cacheDir", "customFields"]

    _description: Optional[str] = None
    _entityType: Optional[CustomTypeEntityType] = None
    _hasRestrictedAddPermission: Optional[bool] = None
    _hasRestrictedEditPermission: Optional[bool] = None
    _hasRestrictedReadPermission: Optional[bool] = None
    _isEnabled: Optional[bool] = None
    _inventoryName: Optional[str] = None
    _inventoryDescription: Optional[str] = None
    _isHierarchyRoot: Optional[bool] = None
    _rootHierarchy: Optional["CustomTypeMinimal"] = None
    _parentTypes: Optional[List["CustomTypeMinimal"]] = None
    _templateVersion: Optional[str] = None
    _integrationId: Optional[str] = None
    _sections: Optional[List[CustomTypeSection]] = None

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        bak = self._noSerialize
        self._noSerialize = [*bak, "sections"]
        tab = self._indentationString * indentation
        tabContent = self._indentationString * (indentation + 1)
        s = super().contentToString(indentation, hideNone)
        # s = ""
        s += f"{tab}sections=\n"
        self._noSerialize = bak
        for section in self.sections or []:
            if not section and hideNone:
                continue
            content = ""
            if section is not None:
                content = section.contentToString(indentation + 2, hideNone=hideNone)
            if not content and hideNone:
                continue
            s += f"{tabContent}{content}"
        return s

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def entityType(self) -> Optional[CustomTypeEntityType]:
        return self._entityType

    @entityType.setter
    def entityType(self, value):
        self._entityType = self.checkAndConvertNullable(
            value, CustomTypeEntityType, "entityType"
        )

    @property
    def hasRestrictedAddPermission(self) -> Optional[bool]:
        return self._hasRestrictedAddPermission

    @hasRestrictedAddPermission.setter
    def hasRestrictedAddPermission(self, value):
        self._hasRestrictedAddPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedAddPermission"
        )

    @property
    def hasRestrictedEditPermission(self) -> Optional[bool]:
        return self._hasRestrictedEditPermission

    @hasRestrictedEditPermission.setter
    def hasRestrictedEditPermission(self, value):
        self._hasRestrictedEditPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedEditPermission"
        )

    @property
    def hasRestrictedReadPermission(self) -> Optional[bool]:
        return self._hasRestrictedReadPermission

    @hasRestrictedReadPermission.setter
    def hasRestrictedReadPermission(self, value):
        self._hasRestrictedReadPermission = self.checkAndConvertNullable(
            value, bool, "hasRestrictedReadPermission"
        )

    @property
    def sections(self) -> Optional[List[CustomTypeSection]]:
        return self._sections

    @sections.setter
    def sections(self, value):
        self._sections = self.checkListAndConvertNullable(
            value, CustomTypeSection, "sections"
        )

    @property
    def isEnabled(self) -> Optional[bool]:
        return self._isEnabled

    @isEnabled.setter
    def isEnabled(self, value):
        self._isEnabled = self.checkAndConvertNullable(value, bool, "isEnabled")

    @property
    def inventoryName(self) -> Optional[str]:
        return self._inventoryName

    @inventoryName.setter
    def inventoryName(self, value):
        self._inventoryName = self.checkAndConvertNullable(value, str, "inventoryName")

    @property
    def inventoryDescription(self) -> Optional[str]:
        return self._inventoryDescription

    @inventoryDescription.setter
    def inventoryDescription(self, value):
        self._inventoryDescription = self.checkAndConvertNullable(
            value, str, "inventoryDescription"
        )

    @property
    def isHierarchyRoot(self) -> Optional[bool]:
        return self._isHierarchyRoot

    @isHierarchyRoot.setter
    def isHierarchyRoot(self, value):
        self._isHierarchyRoot = self.checkAndConvertNullable(
            value, bool, "isHierarchyRoot"
        )

    @property
    def rootHierarchy(self) -> Optional["CustomTypeMinimal"]:
        return self._rootHierarchy

    @rootHierarchy.setter
    def rootHierarchy(self, value):
        self._rootHierarchy = MinimalModelGenerator.MinimalFromSingle(
            value, "CustomTypeMinimal", "rootHierarchy", self._getConnection()
        )

    @property
    def parentTypes(self) -> Optional[List["CustomTypeMinimal"]]:
        return self._parentTypes

    @parentTypes.setter
    def parentTypes(self, value):
        self._parentTypes = MinimalModelGenerator.MinimalFromList(
            value, "CustomTypeMinimal", "parentTypes", self._getConnection()
        )

    @property
    def customFields(self) -> List[CustomField]:
        if self.sections is None:
            return []

        return [
            field
            for section in self.sections
            if section.customFields is not None
            for field in section.customFields
            if field is not None
        ]

    @property
    def templateVersion(self) -> Optional[str]:
        return self._templateVersion

    @templateVersion.setter
    def templateVersion(self, value):
        self._templateVersion = self.checkAndConvertNullable(
            value, str, "templateVersion"
        )

    @property
    def integrationId(self) -> Optional[str]:
        return self._integrationId

    @integrationId.setter
    def integrationId(self, value):
        self._integrationId = self.checkAndConvertNullable(value, str, "integrationId")
