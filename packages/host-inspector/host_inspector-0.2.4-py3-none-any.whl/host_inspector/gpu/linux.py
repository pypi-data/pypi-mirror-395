import re
import shlex
import subprocess
from functools import cache


@cache
def get_gpu():
    """Safely get GPU."""
    try:
        cmd = "vcgencmd get_config int"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


@cache
def get_model() -> str:
    """Get GPU chipset model."""
    model_map = {
        "bcm2835": "Broadcom VideoCore IV",
        "bcm2836": "Broadcom VideoCore IV",
        "bcm2837": "Broadcom VideoCore IV",
        "bcm2711": "Broadcom VideoCore VI",
        "bcm2710A1": "Broadcom VideoCore VI",
    }
    try:
        cmd = "cat /sys/firmware/devicetree/base/gpu/compatible"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        for m, model in model_map.items():
            if m in result:
                return model
        return "Unknown GPU Model"
    except subprocess.CalledProcessError:
        pass

    try:
        result = subprocess.run(
            ["/usr/bin/bash", "-c", 'DISPLAY=:0 glxinfo | grep "OpenGL renderer"'],
            capture_output=True,
            text=True,
            check=True,
        )
        gpu_info = result.stdout.strip()
        return gpu_info.split(":")[1].strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def get_vram() -> str:
    """Safely get GPU VRAM."""
    try:
        cmd = "vcgencmd get_mem gpu"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        return result.replace("gpu=", "").replace("M", " MB")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "--"


@cache
def get_resolution() -> str:
    """Safely get resolution."""
    try:
        cmd = "xrandr -display :0.0"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        result = proc.stdout.strip()
        regex = r"current (\d+) x (\d+)"
        if match := re.search(regex, result):
            return f"{match[1]} x {match[2]}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "--"


@cache
def get_refresh_rate() -> str:
    """Safely get refresh rate."""
    if result := get_gpu():
        for line in result.splitlines():
            if line.startswith("lcd_framerate="):
                return f"{int(line.split('=')[1])} Hz"
    return "--"


@cache
def get_gpu_info() -> dict:
    """Return a dict of GPU info."""
    return {
        "model": get_model(),
        "vram": get_vram(),
        "resolution": get_resolution(),
        "refresh_rate": get_refresh_rate(),
    }
