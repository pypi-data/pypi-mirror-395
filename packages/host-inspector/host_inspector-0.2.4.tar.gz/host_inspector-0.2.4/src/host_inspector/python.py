import platform
import sys
from functools import cache
from pathlib import Path


@cache
def get_python_info() -> dict:
    """Get current Python info as dict."""
    return {
        "version": platform.python_version(),
        "path": str(Path(sys.executable)),
    }
