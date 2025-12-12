import time
from datetime import datetime
from functools import cache

import psutil

from .utils.datetimeutils import human_date
from .utils.datetimeutils import human_date_short
from .utils.datetimeutils import human_delta
from .utils.datetimeutils import human_time


@cache
def boot_time() -> datetime:
    """Return datetime of CPU boot time."""
    return datetime.fromtimestamp(psutil.boot_time()).astimezone()


@cache
def date_as_string(dt: datetime) -> str:
    """Return boot time date as string."""
    return dt.strftime("%Y-%m-%d")


@cache
def time_as_string(dt: datetime, *, military=False) -> str:
    """Return boot time as string."""
    return human_time(dt) if not military else boot_time().strftime("%H:%M")


@cache
def date_as_day(dt: datetime) -> str:
    """Return boot time as day string."""
    return human_date(dt)


@cache
def date_as_day_short(dt: datetime) -> str:
    """Return boot time as day string."""
    return human_date_short(dt)


def uptime_in_seconds() -> int:
    """Return uptime in seconds."""
    return int(time.time() - psutil.boot_time())


def uptime_as_string() -> str:
    """Return uptime as string."""
    return human_delta(uptime_in_seconds())


def get_uptime_info() -> dict:
    """Return uptime info as a dict."""
    dt = boot_time()
    return {
        "day": date_as_day(dt),
        "day_short": date_as_day_short(dt),
        "date": date_as_string(dt),
        "time": time_as_string(dt),
        "military_time": time_as_string(dt, military=True),
        "uptime": uptime_as_string(),
        "seconds": uptime_in_seconds(),
    }
