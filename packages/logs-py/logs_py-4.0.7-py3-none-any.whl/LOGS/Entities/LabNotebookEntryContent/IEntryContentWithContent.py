from typing import List, Optional, Tuple, Type, TypeVar, Union, cast

from LOGS.Entities.LabNotebookEntryContent.EntryContentConverter import (
    EntryContentConverter,
)
from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entity.SerializableContent import SerializableContent

_T = TypeVar("_T", bound=EntryContentItem)


class IEntryContentWithContent(SerializableContent):
    _content: List[EntryContentItem] = cast(List[EntryContentItem], None)

    def listContentItems(
        self, types: Optional[Union[Type[_T], Tuple[Type[_T], ...]]] = None
    ) -> List[_T]:
        items = []
        for item in self.content:
            if not types or isinstance(item, types):
                items.append(item)
            if isinstance(item, IEntryContentWithContent):
                items.extend(item.listContentItems(types))

        return items

    def append(self, item: _T) -> _T:
        raise NotImplementedError()

    @property
    def content(self) -> List[EntryContentItem]:
        if self._content is None:
            self._content = []
        return self._content

    @content.setter
    def content(self, value):
        self._content = EntryContentConverter.convertList(value, fieldName="content")
