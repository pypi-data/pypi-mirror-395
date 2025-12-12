import re
import shlex
import subprocess
from functools import cache

from .utils import clean_name


@cache
def get_gpu():
    """Safely get GPU."""
    try:
        cmd = "system_profiler SPDisplaysDataType"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:  # pragma: no cover
        return None


@cache
def get_model() -> str:
    """Get GPU chipset model."""
    if result := get_gpu():
        for line in result.split("\n"):
            if "Chipset Model" in line:
                return clean_name(re.sub(r"\s+Chipset Model:\s+", "", line, count=1))
    return "--"  # pragma: no cover


@cache
def get_vram() -> str:
    """Get GPU VRAM."""
    if result := get_gpu():
        for line in result.split("\n"):
            if "VRAM" in line:
                return line.split(":")[1].strip()
    return "--"  # pragma: no cover


@cache
def get_resolution() -> str:
    """Get resolution."""
    if result := get_gpu():
        regex = r"(\d+) x (\d+)"
        if match := re.search(regex, result):
            return f"{match[1]} x {match[2]}"
    return "--"  # pragma: no cover


@cache
def get_refresh_rate() -> str:
    """Get refresh rate."""
    pattern = re.compile(r"@ (\d+\.\d+)Hz")
    output = get_gpu()
    if output:
        match = pattern.search(output)
        if match:
            return f"{match.group(1)} Hz"
    return "--"  # pragma: no cover


@cache
def get_gpu_info() -> dict:
    """Return a dict of GPU info."""
    return {
        "model": get_model(),
        "vram": get_vram(),
        "resolution": get_resolution(),
        "refresh_rate": get_refresh_rate(),
    }
