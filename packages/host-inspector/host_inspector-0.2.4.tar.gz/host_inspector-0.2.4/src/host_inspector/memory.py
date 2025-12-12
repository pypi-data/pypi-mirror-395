import math
from functools import cache

import humanize
import psutil

from .utils.byteutils import bytes_to_gb


@cache
def mem_physical(mu):
    """Return physical memory available in GB. We round up to the nearest GB.
    This is what is marketed as the total RAM."""
    return math.ceil(bytes_to_gb(mu.total))


@cache
def mem_physical_str(mu):
    """Return physical memory as a human-readable string."""
    return f"{mem_physical(mu)} GB"


def mem_used(mu):
    """Return memory used in GiB."""
    return bytes_to_gb(mu.used)


def mem_used_str(mu):
    """Return memory used as a human-readable string."""
    return humanize.naturalsize(mu.used, binary=False)


def mem_avail(mu):
    """Return memory available in GiB."""
    return bytes_to_gb(mu.available)


def mem_avail_str(mu):
    """Return memory available as a human-readable string."""
    return humanize.naturalsize(mu.available, binary=False)


def mem_percent(mu):
    """Return memory usages as a percent."""
    return mu.percent


def get_mem_info() -> dict:
    """Return memory info as a dict."""
    mu = psutil.virtual_memory()
    return {
        "physical": mem_physical(mu),
        "physical_str": mem_physical_str(mu),
        "used": mem_used(mu),
        "used_str": mem_used_str(mu),
        "avail": mem_avail(mu),
        "avail_str": mem_avail_str(mu),
        "percent": mem_percent(mu),
        "percent_str": f"{mem_percent(mu)}%",
    }
