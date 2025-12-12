from dataclasses import dataclass
from typing import Optional


@dataclass
class LOGSOptions:
    showRequestUrl: bool = False
    showRequestHeader: bool = False
    showRequestBody: bool = False
    showServerInfo: bool = False
    proxyTargetUrl: Optional[str] = None
