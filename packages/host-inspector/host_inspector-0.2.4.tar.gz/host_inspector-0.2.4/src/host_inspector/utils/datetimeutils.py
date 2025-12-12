import sys

import humanize


def format_date(dt, format_string):
    """Return formatted date string, handling platform differences."""
    if sys.platform == "win32":
        format_string = format_string.replace("%-", "%#")  # pragma: no cover
    return dt.strftime(format_string)


def human_date(dt) -> str:
    """Return date string. eg - Monday, August 4"""
    return format_date(dt, "%A, %B %-d, %Y")


def human_date_short(dt) -> str:
    """Return short date string. eg - Mon, Aug 4"""
    return format_date(dt, "%a, %b %-d, %Y")


def human_time(dt, *, seconds=False) -> str:
    """Return time string. eg - 1:23 PM"""
    format_string = "%I:%M:%S %p" if seconds else "%I:%M %p"
    time_string = format_date(dt, format_string)
    # Remove leading zero from hour on all platforms
    return time_string.lstrip("0") if time_string[0] == "0" else time_string


def human_datetime(dt) -> str:
    """Return datetime string. eg - Monday, August 4 1:23 PM"""
    return f"{human_date(dt)} {human_time(dt)}"


def human_datetime_short(dt) -> str:
    """Return datetime string. eg - Mon, Aug 4 1:23 PM"""
    return f"{human_date_short(dt)} {human_time(dt)}"


def human_delta(seconds: int) -> str:
    """Return uptime as string."""
    delta = humanize.precisedelta(seconds)
    return delta.split(" and ")[0]
