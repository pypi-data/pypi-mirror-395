import contextlib
import platform
import re
import shlex
import subprocess
from functools import cache


@cache
def get_manufacturer() -> str:
    """Safely get manufacturer."""

    if "Raspberry Pi" in get_model():
        return "Raspberry Pi Ltd."

    try:
        cmd = "sudo dmidecode -s system-manufacturer"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def get_model() -> str:
    """Safely get model."""
    # Raspberry Pi
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "cat /sys/firmware/devicetree/base/model"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip().rstrip("\x00")
    # Linux
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "sudo dmidecode -s system-family"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    return "--"


@cache
def get_serial() -> str:
    """Safely get serial number."""
    # Raspberry Pi
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "cat /proc/cpuinfo"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        regex = r"(Serial\s+:)(.+)"
        if match := re.search(regex, result):
            return match[2]

    # Linux
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "sudo dmidecode -s system-serial-number"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    return "--"


@cache
def get_platform_info() -> dict:
    """Return platform info as dict."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "release": uname.release,
        "machine": uname.machine,
        "architecture": platform.architecture()[0],
        "manufacturer": get_manufacturer(),
        "model": get_model(),
        "serial": get_serial(),
    }
