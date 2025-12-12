from typing import Dict, List, Optional

from LOGS.Entity.SerializableContent import SerializableClass


class DatatypeFormattedTableSettings(SerializableClass):
    _type: str = "formatted_table"
    _name: Optional[str] = None
    _id: str = ""
    _cells: List[str] = []
    _cellIds: Dict[str, str] = {}
