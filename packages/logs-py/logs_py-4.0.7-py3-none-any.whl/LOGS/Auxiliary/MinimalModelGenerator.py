from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from LOGS.LOGSConnection import LOGSConnection


class MinimalModelGenerator:
    _entities = [
        "Attachment",
        "Bridge",
        "Dataset",
        "DataFormatInstrument",
        "Method",
        "DataFormat",
        "Vendor",
        "Notebook",
        "NotebookExperiment",
        "NotebookEntry",
        "NotebookTemplate",
        "LabNotebook",
        "LabNotebookExperiment",
        "LabNotebookEntry",
        "Origin",
        "Person",
        "Project",
        "Sample",
        "SharedContent",
        "InventoryItem",
        "CustomType",
        "CustomField",
    ]

    @classmethod
    def createMapper(cls):
        cls._mapper = {e: getattr(cls, f"get{e}MinimalClass")() for e in cls._entities}
        cls._mapper.update({f"{e}Minimal": cls._mapper[e] for e in cls._entities})

    @classmethod
    def _typeByTypename(cls, typeName: str, fieldName: Optional[str]) -> Type:
        if not hasattr(cls, "_mapper"):
            cls.createMapper()

        t = cls._mapper.get(typeName, None)
        if not t:
            raise ValueError(f"Unknown type '{typeName}' for field '{fieldName}'")
        return t

    @classmethod
    def MinimalFromSingle(
        cls,
        value: Any,
        fieldType: str,
        fieldName: Optional[str],
        connection: Optional["LOGSConnection"],
    ) -> Any:
        from LOGS.Entity.ConnectedEntity import ConnectedEntity

        result = ConnectedEntity.checkAndConvertWithConnection(
            value,
            fieldType=cls._typeByTypename(fieldType, fieldName),
            fieldName=fieldName,
            allowNone=True,
            connection=connection,
        )

        return result

    @classmethod
    def MinimalFromList(
        cls,
        value: Any,
        fieldType: str,
        fieldName: Optional[str],
        connection: Optional["LOGSConnection"],
    ) -> Any:
        from LOGS.Entity.ConnectedEntity import ConnectedEntity

        if isinstance(value, (int, str)):
            value = {"id": value}

        if isinstance(value, list):
            l = []
            for v in value:
                if isinstance(v, (int, str)):
                    l.append({"id": v})
                else:
                    l.append(v)
            value = l

        l = ConnectedEntity.checkListAndConvertWithConnection(
            value,
            fieldType=cls._typeByTypename(fieldType, fieldName),
            fieldName=fieldName,
            allowNone=True,
            connection=connection,
        )
        result = [a for a in l if a]

        if len(result) < 1:
            return None

        return result

    @classmethod
    def getAttachmentMinimalClass(cls):
        from LOGS.Entities.AttachmentMinimal import AttachmentMinimal

        return AttachmentMinimal

    @classmethod
    def getBridgeMinimalClass(cls):
        from LOGS.Entities.BridgeMinimal import BridgeMinimal

        return BridgeMinimal

    @classmethod
    def getDatasetMinimalClass(cls):
        from LOGS.Entities.DatasetMinimal import DatasetMinimal

        return DatasetMinimal

    @classmethod
    def getDataFormatInstrumentMinimalClass(cls):
        from LOGS.Entities.DataFormatInstrumentMinimal import (
            DataFormatInstrumentMinimal,
        )

        return DataFormatInstrumentMinimal

    @classmethod
    def getMethodMinimalClass(cls):
        from LOGS.Entities.MethodMinimal import MethodMinimal

        return MethodMinimal

    @classmethod
    def getDataFormatMinimalClass(cls):
        from LOGS.Entities.DataFormatMinimal import DataFormatMinimal

        return DataFormatMinimal

    @classmethod
    def getVendorMinimalClass(cls):
        from LOGS.Entities.VendorMinimal import VendorMinimal

        return VendorMinimal

    @classmethod
    def getNotebookMinimalClass(cls):
        return cls.getLabNotebookMinimalClass()

    @classmethod
    def getLabNotebookMinimalClass(cls):
        from LOGS.Entities.LabNotebookMinimal import LabNotebookMinimal

        return LabNotebookMinimal

    @classmethod
    def getNotebookExperimentMinimalClass(cls):
        return cls.getLabNotebookExperimentMinimalClass()

    @classmethod
    def getLabNotebookExperimentMinimalClass(cls):
        from LOGS.Entities.LabNotebookExperimentMinimal import (
            LabNotebookExperimentMinimal,
        )

        return LabNotebookExperimentMinimal

    @classmethod
    def getNotebookEntryMinimalClass(cls):
        return cls.getLabNotebookEntryMinimalClass()

    @classmethod
    def getLabNotebookEntryMinimalClass(cls):
        from LOGS.Entities.LabNotebookEntryMinimal import LabNotebookEntryMinimal

        return LabNotebookEntryMinimal

    @classmethod
    def getNotebookTemplateMinimalClass(cls):
        return cls.getLabNotebookTemplateMinimalClass()

    @classmethod
    def getLabNotebookTemplateMinimalClass(cls):
        from LOGS.Entities.LabNotebookTemplateMinimal import LabNotebookTemplateMinimal

        return LabNotebookTemplateMinimal

    @classmethod
    def getOriginMinimalClass(cls):
        from LOGS.Entities.OriginMinimal import OriginMinimal

        return OriginMinimal

    @classmethod
    def getPersonMinimalClass(cls):
        from LOGS.Entities.PersonMinimal import PersonMinimal

        return PersonMinimal

    @classmethod
    def getProjectMinimalClass(cls):
        from LOGS.Entities.ProjectMinimal import ProjectMinimal

        return ProjectMinimal

    @classmethod
    def getSampleMinimalClass(cls):
        from LOGS.Entities.SampleMinimal import SampleMinimal

        return SampleMinimal

    @classmethod
    def getSharedContentMinimalClass(cls):
        from LOGS.Entities.SharedContentMinimal import SharedContentMinimal

        return SharedContentMinimal

    @classmethod
    def getInventoryItemMinimalClass(cls):
        from LOGS.Entities.InventoryItemMinimal import InventoryItemMinimal

        return InventoryItemMinimal

    @classmethod
    def getCustomTypeMinimalClass(cls):
        from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal

        return CustomTypeMinimal

    @classmethod
    def getCustomFieldMinimalClass(cls):
        from LOGS.Entities.CustomFieldMinimal import CustomFieldMinimal

        return CustomFieldMinimal
