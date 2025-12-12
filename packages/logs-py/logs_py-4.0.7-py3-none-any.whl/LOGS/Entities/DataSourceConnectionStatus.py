from datetime import datetime
from typing import List, Optional

from LOGS.Entities.DataSourceStatus import DataSourceStatus
from LOGS.Entity.SerializableContent import SerializableClass


class DataSourceConnectionStatus(SerializableClass):
    isConnected: Optional[bool] = None
    nextScheduledDate: Optional[datetime] = None
    lastClientStatus: Optional[DataSourceStatus] = None
    statusHistory: Optional[List[DataSourceStatus]] = None
