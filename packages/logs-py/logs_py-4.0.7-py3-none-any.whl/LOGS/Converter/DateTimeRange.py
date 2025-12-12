from datetime import datetime
from typing import Any, Dict, Optional, cast

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entity.SerializableContent import SerializableContent


class DateTimeRange(SerializableContent):
    """Represents a range of two datetime values"""

    _start: Optional[datetime] = None
    _end: Optional[datetime] = None

    def __init__(
        self, ref=None, start: Optional[datetime] = None, end: Optional[datetime] = None
    ):
        if isinstance(ref, list):
            ref = {
                "start": (ref[0] if len(ref) > 0 else None),
                "end": (ref[1] if len(ref) > 1 else None),
            }
        super().__init__(ref=ref)
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end

    def toDict(self) -> Dict[str, Any]:
        return cast(
            Dict[str, Any],
            [
                Tools.datetimeToUTCString(self.start),
                Tools.datetimeToUTCString(self.end),
            ],
        )

    def __str__(self) -> str:
        return f"<DateTimeRange [{self.start}, {self.end}]>"

    @property
    def start(self) -> Optional[datetime]:
        return self._start

    @start.setter
    def start(self, value: Optional[datetime]):
        self._start = Tools.checkAndConvert(
            value, datetime, "DateTimeRange.start", allowNone=True
        )

    @property
    def end(self) -> Optional[datetime]:
        return self._end

    @end.setter
    def end(self, value: Optional[datetime]):
        self._end = Tools.checkAndConvert(
            value, datetime, "DateTimeRange.end", allowNone=True
        )
