from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entity.ConnectedEntity import ConnectedEntity

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


class ProjectPersonPermission(ConnectedEntity):
    _person: Optional["PersonMinimal"] = None
    _project: Optional["ProjectMinimal"] = None
    _administer: Optional[bool] = None
    _edit: Optional[bool] = None
    _add: Optional[bool] = None
    _read: Optional[bool] = None

    def _fromRef(
        self,
        ref,
        selfClass,
        convertOtherType: Union[Tuple[type, Callable[[Any], Any]], None] = None,
    ):
        if isinstance(ref, dict) and "read" in ref:
            self._read = ref["read"]
            del ref["read"]
        return super()._fromRef(ref, selfClass, convertOtherType)

    def __str__(self):
        attrList = self._getAttrList()

        s1 = f"'{self.person.name}'" if self.person else ""
        s2 = ",".join(k for k in attrList if getattr(self, k, None) is True)
        return f"<{type(self).__name__} {s1} access:{s2}>"

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        return str(self)

    @property
    def person(self) -> Optional["PersonMinimal"]:
        return self._person

    @person.setter
    def person(self, value):
        self._person = MinimalModelGenerator.MinimalFromSingle(
            value, "PersonMinimal", "person", self._getConnection()
        )

    @property
    def project(self) -> Optional["ProjectMinimal"]:
        return self._project

    @project.setter
    def project(self, value):
        self._project = MinimalModelGenerator.MinimalFromSingle(
            value, "ProjectMinimal", "project", self._getConnection()
        )

    @property
    def administer(self) -> Optional[bool]:
        return self._administer

    @administer.setter
    def administer(self, value):
        self._administer = self.checkAndConvertNullable(value, bool, "administer")
        if self._administer:
            self._edit = True
            self._add = True

    @property
    def edit(self) -> Optional[bool]:
        return self._edit

    @edit.setter
    def edit(self, value):
        self._edit = self.checkAndConvertNullable(value, bool, "edit")
        if self._edit:
            self._add = True
        else:
            self._administer = False

    @property
    def add(self) -> Optional[bool]:
        return self._add

    @add.setter
    def add(self, value):
        self._add = self.checkAndConvertNullable(value, bool, "add")
        if not self._add:
            self._edit = False
            self._administer = False

    @property
    def read(self) -> Optional[bool]:
        return self._read

    @read.setter
    def read(self, _):
        raise Exception(
            "Every person added to a project has automatically read permissions."
        )
