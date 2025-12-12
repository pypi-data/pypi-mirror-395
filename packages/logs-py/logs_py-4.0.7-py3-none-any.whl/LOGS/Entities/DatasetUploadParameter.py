from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DatasetUploadParameter:
    name: Optional[str] = None
    methodId: Optional[int] = None
    instrumentId: Optional[int] = None
    experimentId: Optional[int] = None
    sampleId: Optional[int] = None
    projectIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
    operatorIds: Optional[List[int]] = None
