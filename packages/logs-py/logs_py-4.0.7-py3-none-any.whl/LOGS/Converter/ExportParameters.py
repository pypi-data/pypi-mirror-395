from typing import Any, Dict, Optional

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableClass


class ExportParameters(SerializableClass):

    def __init__(
        self,
        ref=None,
        types: Optional[Dict[str, type]] = None,
    ):
        self._lock = False
        if types is not None:
            if not isinstance(types, dict):
                raise Exception("type must be a dictionary")
            for k, v in types.items():
                if not isinstance(v, type):
                    raise Exception(
                        f"Invalid type for key '{k}'. (Expected '{type.__name__}' got '{type(v).__name__}')"
                    )
        else:
            types = {}

        self._typeMapping: Dict[str, type] = {}
        if isinstance(ref, dict):
            if "_parentId" in ref:
                self._parentId: Optional[str] = str(ref["_parentId"])
                del ref["_parentId"]
            else:
                self._parentId = None

            self._includeNone = True
            for k in ref.keys():
                setattr(self, k, ref[k])
                if k in types:
                    self._typeMapping[k] = types[k]
        super().__init__(ref)
        self._lock = True

    def fromDict(self, ref) -> None:
        if getattr(self, "_lock", False):
            if isinstance(ref, dict):
                if "parameters" in ref and isinstance(ref["parameters"], list):
                    for p in ref["parameters"]:
                        if "id" in p and "value" in p:
                            setattr(self, p["id"], p["value"])
                for k, v in ref.items():
                    setattr(self, k, v)
        return super().fromDict(ref)

    def toDict(self) -> Dict[str, Any]:
        l = [
            {"id": k, "value": getattr(self, k)}
            for k in self.__dict__
            if k[0] != "_" and getattr(self, k) is not None
        ]
        if l:
            return {"parameters": l}
        return {}

    def __repr__(self):
        fields = [
            f"{k}{':' + self._typeMapping[k].__name__ if k in self._typeMapping else ''}={v}"
            for k, v in self.toDict().items()
        ]
        return f'{self.identifier}({", ".join(fields)})'

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_lock", False):
            if name not in self._typeMapping:
                raise Exception(f"Unknown field '{self.identifier}.{name}'")

            if name in self._typeMapping:
                value = Tools.checkAndConvert(
                    value,
                    self._typeMapping[name],
                    f"{self.identifier}.{name}",
                    allowNone=True,
                )
        return super().__setattr__(name, value)

    @property
    def identifier(self):
        return f"{self.__class__.__name__}{'<' + self._parentId + '>' if self._parentId else ''}"

    def __str__(self):
        return self.__repr__()
