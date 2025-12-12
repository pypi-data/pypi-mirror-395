from functools import cache

import psutil

from host_inspector.utils.importutils import get_platform_module

platform_module = get_platform_module(__name__)

get_processor_name = platform_module.get_processor_name
get_temp_info = platform_module.get_temp_info


def mhz_to_ghz(m) -> float:
    """Convert MHz to GHz."""
    return round(m / 1000, 2)


@cache
def cpu_physical_count() -> int:
    """Get the number of physical CPUs on the system."""
    return psutil.cpu_count(logical=False)


@cache
def cpu_logical_count() -> int:
    """Get the number of logical CPUs on the system."""
    return psutil.cpu_count()


@cache
def cpu_freq() -> float:
    """Get the maximum frequency of the CPU in GHz."""
    return mhz_to_ghz(psutil.cpu_freq().max)


def cpu_percent() -> float:
    """Get the current CPU usage percentage."""
    return psutil.cpu_percent()


def get_cpu_info() -> dict:
    """Return CPU info as a dict."""
    cpu_usage = cpu_percent()
    cpu_ghz = cpu_freq()
    return {
        "count": cpu_physical_count(),
        "logical": cpu_logical_count(),
        "percent": cpu_usage,
        "percent_str": f"{cpu_usage}%",
        "processor": get_processor_name(),
        "frequency": cpu_ghz,
        "frequency_str": f"{cpu_ghz} GHz",
        "temperature": get_temp_info(),
    }
