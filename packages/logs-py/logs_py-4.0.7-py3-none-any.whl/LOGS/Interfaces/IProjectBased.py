from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


@dataclass
class IProjectBasedRequest:
    projectIds: Optional[List[int]] = None


class IProjectBased(IEntityInterface):
    _projects: Optional[List["ProjectMinimal"]] = None

    @property
    def projects(self) -> Optional[List["ProjectMinimal"]]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = MinimalModelGenerator.MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self._getEntityConnection()
        )
