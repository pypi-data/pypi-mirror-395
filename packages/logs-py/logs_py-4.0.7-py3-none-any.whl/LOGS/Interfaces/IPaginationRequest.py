from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    pass


@dataclass
class IPaginationRequest:
    page: Optional[int] = None
    pageSize: Optional[int] = None
