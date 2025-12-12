import os
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from LOGS.Entities.Attachment import Attachment
    from LOGS.Entities.Bridge import Bridge
    from LOGS.Entities.CustomField import CustomField
    from LOGS.Entities.CustomType import CustomType
    from LOGS.Entities.DataFormat import DataFormat
    from LOGS.Entities.DataFormatInstrument import DataFormatInstrument
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.DatasetTemplate import DatasetTemplate
    from LOGS.Entities.DataSource import DataSource
    from LOGS.Entities.FileEntry import FileEntry
    from LOGS.Entities.InventoryItem import InventoryItem
    from LOGS.Entities.LabNotebook import LabNotebook
    from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
    from LOGS.Entities.LabNotebookExperiment import LabNotebookExperiment
    from LOGS.Entities.LabNotebookTemplate import LabNotebookTemplate
    from LOGS.Entities.Method import Method
    from LOGS.Entities.Origin import Origin
    from LOGS.Entities.Person import Person
    from LOGS.Entities.Project import Project
    from LOGS.Entities.Role import Role
    from LOGS.Entities.Sample import Sample
    from LOGS.Entities.Vendor import Vendor


class Constants:
    _control_character = {
        "0": ("\u0000", "null"),
        "1": ("\u0001", "start of heading"),
        "2": ("\u0002", "start of text"),
        "3": ("\u0003", "end of text"),
        "4": ("\u0004", "end of transmission"),
        "5": ("\u0005", "enquiry"),
        "6": ("\u0006", "acknowledge"),
        "7": ("\u0007", "bell"),
        "8": ("\u0008", "backspace"),
        "9": ("\u0009", "horizontal tabulation"),
        "a": ("\u000a", "line feed"),
        "b": ("\u000b", "vertical tabulation"),
        "c": ("\u000c", "form feed"),
        "d": ("\u000d", "carriage return"),
        "e": ("\u000e", "shift out"),
        "f": ("\u000f", "shift in"),
        "10": ("\u0010", "data link escape"),
        "11": ("\u0011", "device control one"),
        "12": ("\u0012", "device control two"),
        "13": ("\u0013", "device control three"),
        "14": ("\u0014", "device control four"),
        "15": ("\u0015", "negative acknowledge"),
        "16": ("\u0016", "synchronous idle"),
        "17": ("\u0017", "end of transmission block"),
        "18": ("\u0018", "cancel"),
        "19": ("\u0019", "end of medium"),
        "1a": ("\u001a", "substitute"),
        "1b": ("\u001b", "escape"),
        "1c": ("\u001c", "file separator"),
        "1d": ("\u001d", "group separator"),
        "1e": ("\u001e", "record separator"),
        "1f": ("\u001f", "unit separator"),
    }

    byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z"]

    exceptionIndentation = " " * 2

    # Typing aliases constants
    ID_TYPE = Union[int, str]

    FILE_TYPE = Union[str, os.DirEntry, "FileEntry"]

    TYPED_ENTITIES = Union[
        "Sample", "Dataset", "InventoryItem", "DatasetTemplate", "Person", "Project"
    ]

    ENTITIES = Union[
        "Bridge",
        "CustomField",
        "CustomType",
        "Dataset",
        "DataSource",
        "InventoryItem",
        "LabNotebook",
        "LabNotebookEntry",
        "LabNotebookExperiment",
        "LabNotebookTemplate",
        "Origin",
        "Person",
        "Project",
        "Sample",
        "DataFormat",
        "Role",
        "Vendor",
        "DataFormatInstrument",
        "Method",
        "Attachment",
    ]
