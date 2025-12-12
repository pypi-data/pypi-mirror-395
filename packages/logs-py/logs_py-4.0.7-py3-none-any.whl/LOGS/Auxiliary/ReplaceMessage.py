from typing import List, Optional, Union


class ReplaceMessage:
    def __init__(self, message: str = "", path: Optional[List[Union[str, int]]] = None):
        self.message = message
        self.path = path if path else []

    def __str__(self):
        return self.message

    def unshiftPath(self, pathEntry: Union[str, int]):
        self.path.insert(0, pathEntry)
