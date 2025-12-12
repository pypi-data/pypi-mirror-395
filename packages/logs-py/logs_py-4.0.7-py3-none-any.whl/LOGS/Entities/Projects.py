from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Project import Project
from LOGS.Entities.ProjectRequestParameter import ProjectRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("projects")
class Projects(EntityIterator[Project, ProjectRequestParameter]):
    """LOGS connected Projects iterator"""

    _generatorType = Project
    _parameterType = ProjectRequestParameter
