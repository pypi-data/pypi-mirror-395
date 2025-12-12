import platform
import shlex
import subprocess
from functools import cache


@cache
def get_manufacturer() -> str:
    """Safely get manufacturer."""
    try:
        cmd = "powershell -Command '(Get-CimInstance -ClassName Win32_ComputerSystem).Manufacturer'"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        result = proc.stdout.strip()
        return result.replace("Manufacturer", "").strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def get_model() -> str:
    """Safely get model."""

    try:
        cmd = "powershell -Command '(Get-CimInstance -ClassName Win32_ComputerSystem).Model'"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        result = proc.stdout.strip()
        return result.replace("Model", "").strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def get_serial() -> str:
    """Safely get serial number."""
    try:
        cmd = "powershell -Command '(Get-WmiObject win32_bios).SerialNumber'"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        result = proc.stdout.strip()
        return result.replace("SerialNumber", "").strip()
    except subprocess.CalledProcessError:
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
