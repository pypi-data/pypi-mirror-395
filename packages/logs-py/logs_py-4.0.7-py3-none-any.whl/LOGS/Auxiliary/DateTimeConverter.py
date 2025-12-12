import datetime as dt
import re
import time
from typing import List, cast

import pytz


class DateTimeConverter:
    # When adding pattern here put the pattern with most information on top
    _datePatterns = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]
    _timePatterns = ["%H:%M:%S.%f", "%H:%M:%S", "%H:%M"]
    utc_offset_re = re.compile(r"([\+-])(\d+)$")
    multiSpace_re = re.compile(r"( {2,})")

    @classmethod
    def _getLocalTime(cls):
        import platform

        if platform.system() == "Windows":
            from tzlocal.win32 import get_localzone_name

            return pytz.timezone(get_localzone_name())
        else:
            return pytz.timezone(time.tzname[0])

    @classmethod
    def convertTime(cls, entry: str):
        entry = re.sub(cls.multiSpace_re, " ", entry)
        match = cls.utc_offset_re.search(entry)
        if match and len(match.group(2)) == 3:
            entry = entry.replace(match.group(0), match.group(1) + "0" + match.group(2))

        times: List[dt.time] = []
        for pattern in set(cast(List[str], cls._timePatterns)):
            try:
                times.append(dt.datetime.strptime(entry, pattern).time())
            except:
                continue
        if len(times) < 1:
            return None

        return times[0]

    @classmethod
    def convertDateTime(cls, entry: str):
        entry = re.sub(cls.multiSpace_re, " ", entry)
        match = cls.utc_offset_re.search(entry)
        if match and len(match.group(2)) == 3:
            entry = entry.replace(match.group(0), match.group(1) + "0" + match.group(2))

        dates: List[dt.datetime] = []
        for pattern in set(cast(List[str], cls._datePatterns)):
            try:
                dates.append(dt.datetime.strptime(entry, pattern))
            except:
                continue
        if len(dates) < 1:
            return None

        d = dates[0]
        if d.tzinfo == pytz.UTC or d.tzinfo is None:
            local_tz = cls._getLocalTime()
            d = d.replace(tzinfo=pytz.utc).astimezone(local_tz)

        return d
