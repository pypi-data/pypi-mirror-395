import time
from datetime import datetime

from host_inspector.utils.datetimeutils import human_date
from host_inspector.utils.datetimeutils import human_date_short
from host_inspector.utils.datetimeutils import human_time


def get_now() -> datetime:
    """Return current local datetime."""
    return datetime.now().astimezone()


def is_dst() -> bool:
    """Return True if Daylight Savings Time."""
    return time.localtime().tm_isdst == 1


def local_timezone(now: datetime) -> str:
    """Get local Timezone."""
    return str(now.tzinfo)


def date_as_string(now: datetime) -> str:
    """Return boot time date as string."""
    return now.strftime("%Y-%m-%d")


def date_as_day(now) -> str:
    """Return date as a string."""
    return human_date(now)


def date_as_day_short(now) -> str:
    """Return date as a string."""
    return human_date_short(now)


def time_as_string(now, *, military=False) -> str:
    """Return time as a string."""
    return human_time(now) if not military else now.strftime("%H:%M")


def get_datetime_info() -> dict:
    """Get date/time information as a dict."""
    now = get_now()
    return {
        "timestamp": now.isoformat(),
        "day": date_as_day(now),
        "day_short": date_as_day_short(now),
        "date": date_as_string(now),
        "time": time_as_string(now),
        "military_time": time_as_string(now, military=True),
        "timezone": local_timezone(now),
        "is_dst": is_dst(),
    }
