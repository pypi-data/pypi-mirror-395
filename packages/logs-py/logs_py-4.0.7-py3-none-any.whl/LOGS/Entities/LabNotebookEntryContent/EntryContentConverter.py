from typing import Generic, List, Optional, TypeVar, cast

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem

_T = TypeVar("_T", bound=EntryContentItem)


class EntryContentConverter(Generic[_T]):

    @classmethod
    def _convertEntryContentDocument(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentDocument import (
            EntryContentDocument,
        )

        return EntryContentDocument(item)

    @classmethod
    def _convertEntryContentHeading(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentHeading import (
            EntryContentHeading,
        )

        return EntryContentHeading(item)

    @classmethod
    def _convertEntryContentText(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentText import (
            EntryContentText,
        )

        return EntryContentText(item)

    @classmethod
    def _convertEntryContentParagraph(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentParagraph import (
            EntryContentParagraph,
        )

        return EntryContentParagraph(item)

    @classmethod
    def _convertEntryContentBlockquote(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentBlockquote import (
            EntryContentBlockquote,
        )

        return EntryContentBlockquote(item)

    @classmethod
    def _convertEntryContentBulletList(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentBulletList import (
            EntryContentBulletList,
        )

        return EntryContentBulletList(item)

    @classmethod
    def _convertEntryContentOrderedList(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentOrderedList import (
            EntryContentOrderedList,
        )

        return EntryContentOrderedList(item)

    @classmethod
    def _convertEntryContentCallout(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentCallout import (
            EntryContentCallout,
        )

        return EntryContentCallout(item)

    @classmethod
    def _convertEntryContentContentPlaceholderNode(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentContentPlaceholderNode import (
            EntryContentContentPlaceholderNode,
        )

        return EntryContentContentPlaceholderNode(item)

    @classmethod
    def _convertEntryContentEntity(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentEntity import (
            EntryContentEntity,
        )

        return EntryContentEntity(item)

    @classmethod
    def _convertEntryContentEntityMention(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentEntityMention import (
            EntryContentEntityMention,
        )

        return EntryContentEntityMention(item)

    @classmethod
    def _convertEntryContentHorizontalRule(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentHorizontalRule import (
            EntryContentHorizontalRule,
        )

        return EntryContentHorizontalRule(item)

    @classmethod
    def _convertEntryContentListItem(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentListItem import (
            EntryContentListItem,
        )

        return EntryContentListItem(item)

    @classmethod
    def _convertEntryContentTaskList(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentTaskList import (
            EntryContentTaskList,
        )

        return EntryContentTaskList(item)

    @classmethod
    def _convertEntryContentTaskListItem(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentTaskListItem import (
            EntryContentTaskListItem,
        )

        return EntryContentTaskListItem(item)

    @classmethod
    def _convertEntryContentTable(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentTable import (
            EntryContentTable,
        )

        return EntryContentTable(item)

    @classmethod
    def _convertEntryContentTableCell(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentTableCell import (
            EntryContentTableCell,
        )

        return EntryContentTableCell(item)

    @classmethod
    def _convertEntryContentTableRow(cls, item: dict):
        from LOGS.Entities.LabNotebookEntryContent.EntryContentTableRow import (
            EntryContentTableRow,
        )

        return EntryContentTableRow(item)

    @classmethod
    def convert(cls, item: dict, fieldName: Optional[str] = None) -> _T:
        field = f"in field {fieldName}" if fieldName else ""

        if isinstance(item, EntryContentItem):
            return cast(_T, item)

        if not isinstance(item, dict):
            raise ValueError(
                f"EntryContentItem {field} must be of type 'dict'. (Got type '{type(item).__name__}')"
            )

        if "type" not in item:
            raise ValueError(
                f"EntryContentItem {field} must contain a 'type' field. (Got '{Tools.truncString(str(item))}')"
            )

        _typeMapper = {
            "blockquote": cls._convertEntryContentBlockquote,
            "bulletList": cls._convertEntryContentBulletList,
            "callout": cls._convertEntryContentCallout,
            "contentPlaceholderNode": cls._convertEntryContentContentPlaceholderNode,
            "doc": cls._convertEntryContentDocument,
            "entity": cls._convertEntryContentEntity,
            "entityMention": cls._convertEntryContentEntityMention,
            "heading": cls._convertEntryContentHeading,
            "horizontalRule": cls._convertEntryContentHorizontalRule,
            "listItem": cls._convertEntryContentListItem,
            "orderedList": cls._convertEntryContentOrderedList,
            "paragraph": cls._convertEntryContentParagraph,
            "table": cls._convertEntryContentTable,
            "tableCell": cls._convertEntryContentTableCell,
            "tableRow": cls._convertEntryContentTableRow,
            "taskList": cls._convertEntryContentTaskList,
            "taskListItem": cls._convertEntryContentTaskListItem,
            "text": cls._convertEntryContentText,
        }

        mapper = _typeMapper.get(item["type"], None)
        if mapper:
            return cast(_T, mapper(item))

        return cast(_T, EntryContentItem(item))

    @classmethod
    def convertList(cls, items, fieldName: Optional[str] = None) -> List[_T]:
        if not isinstance(items, list):
            items = [items]

        return [
            cls.convert(item, fieldName=f"{fieldName}[{i}]" if fieldName else None)
            for i, item in enumerate(items)
        ]
