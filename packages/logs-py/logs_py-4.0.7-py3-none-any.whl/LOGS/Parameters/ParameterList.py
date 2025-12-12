from typing import Any, List, cast

from LOGS.Parameters.ParameterBase import ParameterBase


class ParameterList(ParameterBase):
    _type = "list"
    _content: List[ParameterBase] = []

    def __init__(self, ref=None):
        if isinstance(ref, list):
            ref = {"name": "<root>", "content": ref}

        super().__init__(ref)

    def __iter__(self):
        for c in self._content:
            yield c

    def findItems(self, name: str) -> List[ParameterBase]:
        return [c for c in self._content if c.name == name]

    def findItemsRecursively(self, name: str) -> List[ParameterBase]:
        result = self.findItems(name)
        # print([c.name for c in self._content])
        # print("->", [c.name for c in result])

        for c in self._content:
            if isinstance(c, ParameterList):
                result.extend(c.findItemsRecursively(name))

        return result

    @property
    def content(self) -> List[ParameterBase]:
        return self._content

    @content.setter
    def content(self, value: List[ParameterBase]):
        from LOGS.Parameters.ParameterConverter import ParameterConverter

        # for e in value:
        #     p = ParameterConverter.convert(e)
        #     p.printJson()
        #     print("-------------------")

        self._content = self.checkListAndConvert(
            value,
            ParameterBase,
            "content",
            converter=cast(Any, ParameterConverter.convert),
        )
