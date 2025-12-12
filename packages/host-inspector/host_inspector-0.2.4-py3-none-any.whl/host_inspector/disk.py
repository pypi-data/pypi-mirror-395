import math
from functools import cache

import humanize
import psutil

from .utils.byteutils import bytes_to_gb


@cache
def disk_physical(du):
    """Return physical disk available in GiB. We round up to the nearest GB.
    This is what is marketed as the total disk space."""
    return math.ceil(bytes_to_gb(du.total))


@cache
def disk_physical_str(du):
    """Return physical disk as a human-readable string."""
    return f"{disk_physical(du)} GB"


def disk_used(du):
    """Return disk used in GB."""
    return bytes_to_gb(du.used)


def disk_used_str(du):
    """Return disk used as a human-readable string."""
    return humanize.naturalsize(du.used, binary=False)


def disk_avail(du):
    """Return disk available in GB."""
    return bytes_to_gb(du.free)


def disk_avail_str(du):
    """Return disk available as a human-readable string."""
    return humanize.naturalsize(du.free, binary=False)


def disk_percent(du):
    """Return disk usages as a percent."""
    return du.percent


def get_disk_info(path="/") -> dict:
    """Return disk usage info as dict."""
    du = psutil.disk_usage(path)
    return {
        "physical": disk_physical(du),
        "physical_str": disk_physical_str(du),
        "used": disk_used(du),
        "used_str": disk_used_str(du),
        "avail": disk_avail(du),
        "avail_str": disk_avail_str(du),
        "percent": disk_percent(du),
        "percent_str": f"{disk_percent(du)}%",
    }
