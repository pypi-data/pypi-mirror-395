import shlex
import subprocess
from functools import cache

from .utils import clean_name


@cache
def get_processor_name() -> str:
    """Safely get processor name."""
    try:
        cmd = "sysctl -n machdep.cpu.brand_string"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd), check=True, capture_output=True, text=True
        )
        return clean_name(proc.stdout.strip())
    except subprocess.CalledProcessError:  # pragma: no cover
        return "--"


def get_temp_info():
    # TODO: Implement temperature retrieval for MacOS
    temp_c = 0.0
    temp_f = 0.0
    return {
        "celsius": temp_c,
        "fahrenheit": temp_f,
        "celsius_str": f"{temp_c if temp_c != 0 else '--'} °C",
        "fahrenheit_str": f"{temp_f if temp_f != 0 else '--'} °F",
    }
