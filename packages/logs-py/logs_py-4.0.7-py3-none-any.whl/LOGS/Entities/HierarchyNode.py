from typing import Optional, Sequence, Union

from LOGS.Entities.HierarchyLeaf import HierarchyLeaf
from LOGS.Entity.SerializableContent import SerializableContent


class HierarchyNode(SerializableContent):
    _name: Optional[str] = None
    _content: Optional[Sequence[Union["HierarchyNode", HierarchyLeaf]]] = None

    def _converter(self, value):
        if isinstance(value, dict) and "type" in value:
            type = value["type"]
            if type == "node":
                return self.checkAndConvert(value, HierarchyNode, "node.content")
            elif type == "leaf":
                return self.checkAndConvert(value, HierarchyLeaf, "leaf")
        return None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def content(self) -> Optional[Sequence[Union["HierarchyNode", HierarchyLeaf]]]:
        return self._content

    @content.setter
    def content(self, value):
        l = self.checkListAndConvertNullable(
            value,
            fieldType=HierarchyNode,
            converter=self._converter,
            fieldName="content",
        )
        self._content = [c for c in l if c]
