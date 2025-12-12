from enum import Enum
from typing import Dict, Generic, List, Optional, Union

from typing_extensions import TypeVar

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableClass


class LogsErrorType(Enum):
    EntityList = "EntityList"
    ParameterValidation = "ParameterValidation"


class ILogsErrorClass(SerializableClass):
    pass


_T = TypeVar("_T", bound=ILogsErrorClass)
_idType = TypeVar("_idType", bound=Union[int, str])


class EntityListErrorClass(Generic[_idType], ILogsErrorClass):
    ids: List[_idType] = []
    errors: List[str] = []


class LOGSErrorResponse(Generic[_T], SerializableClass):
    _noSerialize = ["errorStringList", "details"]

    header: Optional[str] = None
    title: Optional[str] = None
    status: Optional[int] = None
    errorsType: Optional[LogsErrorType] = None
    errorsClass: Optional[Dict] = None
    errors: Optional[Union[Dict, List]] = None
    details: Optional[str] = None

    def _fieldToStr(self, d: Union[Dict, List], indentation: int = 0) -> List[str]:
        tab = self._indentationString * indentation

        if isinstance(d, list):
            s = []
            for v in d:
                s.extend(self._fieldToStr(v, indentation))
            return s
        elif isinstance(d, dict):
            s = []
            nextTab = tab + self._indentationString
            for k, v in d.items():
                l = self._fieldToStr(v)
                if l is None:
                    continue
                if len(l) < 1:
                    s.append(f"{tab}{k}: <empty>")
                if len(l) > 1:
                    s.append(f"{tab}{k}:")
                    s.extend([f"{nextTab}{i}" for i in l])
                else:
                    s.append(f"{tab}{k}: {l[0]}")

            return s

        if d is None:
            return None
        return [str(d)]

    def __str__(self):
        s1 = f":{self.status}" if self.status else ""
        s2 = f"'{Tools.truncString(self.title, 50)}'" if self.title else ""
        return f"<{type(self).__name__}{s1} {s2}>"

    def errorString(self, prefix: str = "") -> str:
        return "\n".join(f"{prefix}{f}" for f in self.errorStringList)

    @property
    def errorStringList(self) -> List[str]:
        errors: List[str] = []

        if self.title:
            errors.append(str(self.title))
        elif self.header:
            errors.append(str(self.header))

        if self.errors:
            errors.append(f"{self._indentationString}Details:")
            errors.extend(self._fieldToStr(self.errors, 2))

        return errors
