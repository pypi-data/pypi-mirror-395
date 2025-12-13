"""
Parse and convert datetimes and timezones.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import Literal

# ZoneInfo: introduced in Python 3.9
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None
    

#region Time zones

_local_tz: tzinfo|None = None

def parse_tz(tz: tzinfo|Literal['local','utc']|str|None = 'local') -> tzinfo:
    if isinstance(tz, tzinfo):
        return tz
    elif tz is None:
        return get_local_tz()
    elif isinstance(tz, str):
        lower_tz = tz.lower()
        if lower_tz == 'local' or lower_tz == 'localtime':
            return get_local_tz()
        elif lower_tz == 'utc':
            return timezone.utc
        
        if not ZoneInfo:
            # pytz: used to parse timezones on Python < 3.9 (no ZoneInfo available)
            try:
                import pytz  # type: ignore
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'pytz' is required on Python < 3.9 to parse timezones from strings") from None
            return pytz.timezone(tz)
        if sys.platform == 'win32':
            # tzdata: used to parse timezones from strings through ZoneInfo on Windows (Windows does not maintain a database of timezones)
            try:
                import tzdata  # pyright: ignore[reportMissingImports]
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'tzdata' is required on Windows to parse timezones from strings") from None
        return ZoneInfo(tz)
    else:
        raise TypeError(f"Invalid timezone type: {tz} ({type(tz).__name__})")


def get_local_tz() -> tzinfo:
    global _local_tz

    if _local_tz is None:
        if not ZoneInfo or sys.platform == 'win32':
            # tzlocal: used to parse timezones from strings on Windows (Windows does not maintain a database of timezones and `tzdata` only is not enough)
            # NOTE: using `datetime.now().astimezone().tzinfo` results in a timezone info that are not aware of the daylight saving time variations
            try:
                import tzlocal  # type: ignore
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"Module 'tzlocal' is required on Windows or on Python < 3.9 to retrieve local timezone") from None
            tz: tzinfo = tzlocal.get_localzone()
            _local_tz = tz

        else:
            _local_tz = ZoneInfo('localtime')
    
    return _local_tz


def make_aware(value: datetime, tz: tzinfo|Literal['local','utc']|str|None = 'local') -> datetime:
    """
    Make a naive datetime aware in the given timezone (use `tz='local'` for the system local timezone or `tz='utc' for UTC`).
    """
    if value is None:
        return None
    
    if value.tzinfo:
        raise ValueError(f"The datetime is already aware: {value.tzinfo}")
    
    if tz is None or tz == 'local' or tz == 'localtime':
        tz = None
    elif tz == 'utc':
        tz = timezone.utc
    elif not isinstance(tz, tzinfo):
        tz = parse_tz(tz)
    
    if hasattr(tz, 'localize'):
        # See: https://stackoverflow.com/a/6411149
        return tz.localize(value) # type: ignore
    else:
        return value.astimezone(tz)


def make_naive(value: datetime, tz: tzinfo|Literal['local','utc']|str|None = 'local') -> datetime:
    """
    Make an aware datetime naive in the given timezone (use `tz='local'` for the system local timezone or `tz='utc' for UTC`).
    """
    if value is None:
        return None

    if not value.tzinfo:
        raise ValueError(f"The datetime is already naive: {value}")
    
    if value.year >= 2999: # avoid astimezone() issue for conversion of datetimes such as 9999-12-31 23:59:59.999999+00:00 or 4000-01-02 23:00:00+00:00
        return value.replace(tzinfo=None)
    
    if tz is None or tz == 'local' or tz == 'localtime':
        tz = None
    elif tz == 'utc':
        tz = timezone.utc
    elif not isinstance(tz, tzinfo):
        tz = parse_tz(tz)
    
    value = value.astimezone(tz)
    return value.replace(tzinfo=None)


def now_aware(tz: tzinfo|Literal['local','utc']|str|None = 'local', *, no_microseconds = False):
    """
    Get the current aware datetime in the given timezone (use `tz='local'` for the system local timezone or `tz='utc' for UTC`).
    """
    if tz is None or tz == 'local' or tz == 'localtime':
        tz = None
    elif tz == 'utc':
        tz = timezone.utc
    elif not isinstance(tz, tzinfo):
        tz = parse_tz(tz)
    
    now = datetime.now().astimezone(tz)
    if no_microseconds:
        now = now.replace(microsecond=0)
    return now


def now_naive(tz: tzinfo|Literal['local','utc']|str|None = 'local', *, no_microseconds = False):
    """
    Get the current naive datetime in the given timezone (use `tz='local'` for the system local timezone or `tz='utc' for UTC`).
    """
    if tz is None or tz == 'local' or tz == 'localtime':
        tz = None
    elif tz == 'utc':
        tz = timezone.utc
    elif not isinstance(tz, tzinfo):
        tz = parse_tz(tz)

    now = datetime.now(tz=tz).replace(tzinfo=None)

    if no_microseconds:
        now = now.replace(microsecond=0)
    return now

#endregion


#region Parse from strings

def is_iso_datetime(value: str|None) -> bool:
    """
    Recognize if the given string value may be parsed as ISO datetime.
    
    This is used to handle datetime values (typically coming from APIs with JSON-encoded data) as datetimes, notably to perform CSV and JSON parsing and timezone handling.
    """
    if value is None:
        return False
    elif re.match(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?(?:Z|[\+\-]\d{2}(?::?\d{2})?)?$', value):
        return True
    else:
        return False
    

def parse_datetime(value: str|date, *, use_locale = False) -> datetime:
    if isinstance(value, datetime):
        raise TypeError(f"value: {type(value).__name__}")  # a datetime is also a date so we need it here (before checking for date) to avoid transforming datetimes by mistake
    elif isinstance(value, date):
        return datetime(value.year, value.month, value.day, 0)
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value).__name__}")
    
    if 'T' in value: # ISO separator between date and time
        return datetime.fromisoformat(value)
    
    
    pos = value.rfind(' ')
    if pos == -1:
        pos = len(value)

    datepart = value[0:pos]
    timepart = value[pos+1:]

    d = parse_date(datepart, use_locale=use_locale)
    if not d:
        raise ValueError(f"Invalid date in {value}")

    value = d.isoformat() + ' ' + (timepart if timepart else '00:00:00')
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f %z') # format not accepted by fromisoformat (contrary to other non-ISO but still frequent "%Y-%m-%d %H:%M:%S.%f")


def parse_month(text: str|int) -> int:
    if isinstance(text, int):
        return text
    elif re.match(r'^\d+$', text):
        return int(text)
    
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    if norm.startswith(('jan',)):
        return 1
    elif norm.startswith(('feb','fev')):
        return 2
    elif norm.startswith(('mar',)):
        return 3
    elif norm.startswith(('apr','avr')):
        return 4
    elif norm.startswith(('may','mai')):
        return 5
    elif norm.startswith(('jun','juin')):
        return 6
    elif norm.startswith(('jul','juil')):
        return 7
    elif norm.startswith(('aug','aou')):
        return 8
    elif norm.startswith(('sep')):
        return 9
    elif norm.startswith(('oct',)):
        return 10
    elif norm.startswith(('nov',)):
        return 11
    elif norm.startswith(('dec',)):
        return 12
    else:
        raise ValueError(f"Unknown month: {text}")


def parse_date(value: str|datetime, *, use_locale = False) -> date:
    if isinstance(value, datetime):
        return value.date()
    elif isinstance(value, date):
        return value
    elif not isinstance(value, str):
        raise TypeError(f"value: {type(value).__name__}")
    
    m = re.match(r'^(?P<val1>\d{1,4}|[a-z]{3,4})(?P<sep1>[/\.\-])(?P<val2>\d{1,2}|[a-z]{3,4})(?P<sep2>[/\.\-])(?P<val3>\d{1,4}|[a-z]{3,4})$', value)
    if not m or m['sep1'] != m['sep2']:
        raise ValueError(f"Invalid date string: {value}")
    
    vals = [m['val1'], m['val2'], m['val3']]

    if m['sep1'] == '-':
        return date(int(vals[0]), parse_month(vals[1]), int(vals[2]))
    elif m['sep1'] == '.':
        return date(int(vals[2]), parse_month(vals[1]), int(vals[0]))
    
    years: list[int] = []
    months: list[int] = []
    months_from_str: list[int] = []
    days: list[int] = []
    for val in vals:
        ival = parse_month(val)
        if ival <= 12:
            (months if re.match(r'^\d+$', val) else months_from_str).append(ival)
        elif ival <= 31:
            days.append(ival)
        else:
            years.append(ival)

    if any(months_from_str):
        days += months
        months = months_from_str
    
    if len(years) == 1 and len(months) == 1 and len(days) == 1:
        return date(years[0], months[0], days[0])

    ldf = None        
    if use_locale:
        from zut.locale import get_locale_date_format
        ldf = get_locale_date_format()
    
    if not ldf:
        raise ValueError(f"Ambiguous date string: {value}")
    
    fmt = re.sub(r'[^ymd]', '', ldf.lower())
    
    if len(fmt) == 3:
        y_index = fmt.rfind('y')
        m_index = fmt.rfind('m')
        d_index = fmt.rfind('d')
        if y_index >= 0 and m_index >= 0 and d_index >= 0:
            return date(int(vals[y_index]), int(vals[m_index]), int(vals[d_index]))
    
    raise ValueError(f"Unexpected locale date format: {fmt}")

#endregion


#region Convert to strings

def get_duration_str(duration: timedelta) -> str:
    # Adapted from: django.utils.duration.duration_iso_string
    if duration < timedelta(0):
        sign = "-"
        duration *= -1
    else:
        sign = ""

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = ".{:06d}".format(microseconds) if microseconds else ""
    return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
        sign, days, hours, minutes, seconds, ms
    )


def _get_duration_components(duration: timedelta):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds

#endregion
