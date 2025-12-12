import platform
import winreg
from functools import cache

from .utils import clean_name


@cache
def get_processor_name() -> str:
    """Safely get processor name."""
    try:
        key = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        chnd = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
        return clean_name(winreg.QueryValueEx(chnd, "ProcessorNameString")[0])
    except FileNotFoundError:
        return platform.processor()


def get_temp_info():
    # TODO: Implement temperature retrieval for Windows
    temp_c = 0.0
    temp_f = 0.0
    return {
        "celsius": temp_c,
        "fahrenheit": temp_f,
        "celsius_str": f"{temp_c if temp_c != 0 else '--'} °C",
        "fahrenheit_str": f"{temp_f if temp_f != 0 else '--'} °F",
    }
