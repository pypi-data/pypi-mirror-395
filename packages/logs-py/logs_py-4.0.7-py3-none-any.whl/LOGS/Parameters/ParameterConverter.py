from typing import cast

from LOGS.Parameters.ParameterBase import ParameterBase
from LOGS.Parameters.ParameterElement import ParameterElement
from LOGS.Parameters.ParameterList import ParameterList
from LOGS.Parameters.ParameterTable import ParameterTable


class ParameterConverter:
    @classmethod
    def convert(cls, parameter):
        if not isinstance(parameter, dict) or "type" not in parameter:
            return cast(ParameterBase, None)

        if parameter["type"] == "parameter":
            return ParameterElement(parameter)

        if parameter["type"] == "list":
            return ParameterList(parameter)

        if parameter["type"] == "table":
            return ParameterTable(parameter)

        return cast(ParameterBase, None)
