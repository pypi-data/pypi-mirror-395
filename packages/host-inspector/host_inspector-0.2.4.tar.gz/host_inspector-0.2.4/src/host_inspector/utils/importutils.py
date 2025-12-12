import importlib
import logging
import sys

logger = logging.getLogger(__name__)


def get_platform_module_name() -> str:
    """Get the platform module name for the current platform."""
    platform_module_map = {
        "darwin": ".mac",
        "win32": ".windows",
        "linux": ".linux",
    }

    try:
        return platform_module_map[sys.platform]
    except KeyError:  # pragma: no cover
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg) from None


def get_platform_module(package: str):
    """Get the platform module for the current platform."""
    return importlib.import_module(
        get_platform_module_name(),
        package=package,
    )
