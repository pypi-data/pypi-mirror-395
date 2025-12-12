from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.CustomFieldRequestParameter import CustomFieldRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("custom_fields")
class CustomFields(EntityIterator[CustomField, CustomFieldRequestParameter]):
    """LOGS connected CustomFields iterator"""

    _generatorType = CustomField
    _parameterType = CustomFieldRequestParameter
