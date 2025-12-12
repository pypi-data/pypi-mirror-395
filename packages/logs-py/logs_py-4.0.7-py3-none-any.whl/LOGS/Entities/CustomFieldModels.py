from enum import Enum
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from LOGS.Entity.EntityWithIntId import IEntityWithIntId


class CustomTypeEntityType(Enum):
    Sample = "Sample"
    Dataset = "Dataset"
    InventoryItem = "InventoryItem"
    Project = "Project"
    Person = "Person"


class CustomTypeEntityTypeMapper:
    @classmethod
    def getClass(cls, entityType: CustomTypeEntityType) -> Type["IEntityWithIntId"]:
        mapping = {
            CustomTypeEntityType.Sample: cls.Sample(),
            CustomTypeEntityType.Dataset: cls.Dataset(),
            CustomTypeEntityType.InventoryItem: cls.InventoryItem(),
            CustomTypeEntityType.Project: cls.Project(),
            CustomTypeEntityType.Person: cls.Person(),
        }
        result = mapping.get(entityType, None)
        if result is None:
            raise Exception(f"Unknown entity type '{entityType.name}'.")
        return result

    @classmethod
    def Sample(cls):
        from LOGS.Entities.Sample import Sample

        return Sample

    @classmethod
    def Dataset(cls):
        from LOGS.Entities.Dataset import Dataset

        return Dataset

    @classmethod
    def InventoryItem(cls):
        from LOGS.Entities.InventoryItem import InventoryItem

        return InventoryItem

    @classmethod
    def Project(cls):
        from LOGS.Entities.Project import Project

        return Project

    @classmethod
    def Person(cls):
        from LOGS.Entities.Person import Person

        return Person


class CustomFieldDataType(Enum):
    String = "String"
    StringArray = "StringArray"
    Integer = "Integer"
    IntegerArray = "IntegerArray"
    Float = "Float"
    FloatArray = "FloatArray"
    Boolean = "Boolean"
    Date = "Date"
    DateArray = "DateArray"
    DateTime = "DateTime"
    DateTimeArray = "DateTimeArray"
    Time = "Time"
    TimeArray = "TimeArray"
    DateTimeRange = "DateTimeRange"
    TimeRange = "TimeRange"
    Dataset = "Dataset"
    DatasetArray = "DatasetArray"
    Sample = "Sample"
    SampleArray = "SampleArray"
    Project = "Project"
    ProjectArray = "ProjectArray"
    Person = "Person"
    PersonArray = "PersonArray"
    Method = "Method"
    MethodArray = "MethodArray"
    SharedContent = "SharedContent"
    SharedContentArray = "SharedContentArray"
    LabNotebook = "LabNotebook"
    LabNotebookArray = "LabNotebookArray"
    LabNotebookExperiment = "LabNotebookExperiment"
    LabNotebookExperimentArray = "LabNotebookExperimentArray"
    LabNotebookEntry = "LabNotebookEntry"
    LabNotebookEntryArray = "LabNotebookEntryArray"
    Attachment = "Attachment"
    InventoryItem = "InventoryItem"
    InventoryItemArray = "InventoryItemArray"
    Barcode = "Barcode"
    Url = "Url"
    UrlArray = "UrlArray"


class CustomFieldValuesSearchPredicate(Enum):
    AND = "AND"
    OR = "OR"


class CustomFieldValueType(Enum):
    CustomField = "CustomField"
    CustomTypeSection = "CustomTypeSection"
