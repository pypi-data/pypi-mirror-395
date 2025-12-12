import json
import platform
import shlex
import subprocess
from functools import cache


@cache
def get_hardware():
    """Safely get hardware."""
    try:
        cmd = "system_profiler -json SPHardwareDataType"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(proc.stdout.strip())
        if "SPHardwareDataType" in result:
            return result["SPHardwareDataType"][0]
    except subprocess.CalledProcessError:  # pragma: no cover
        return None


@cache
def get_model() -> str:
    """Safely get model."""
    return result.get("machine_name") if (result := get_hardware()) else ""


@cache
def get_serial() -> str:
    """Safely get serial number."""
    return result.get("serial_number") if (result := get_hardware()) else ""


@cache
def get_platform_info() -> dict:
    """Return platform info as dict."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "release": uname.release,
        "machine": uname.machine,
        "architecture": platform.architecture()[0],
        "manufacturer": "Apple Inc.",
        "model": get_model(),
        "serial": get_serial(),
    }
