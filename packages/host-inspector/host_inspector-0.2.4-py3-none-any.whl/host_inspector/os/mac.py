import logging
import re
import shlex
import subprocess
from functools import cache

logger = logging.getLogger(__name__)


@cache
def _get_mac_os() -> dict:
    """Parse command line for name, version, and edition."""
    cmd = "sw_vers"
    proc = subprocess.run(  # noqa: S603
        shlex.split(cmd),
        check=True,
        capture_output=True,
        text=True,
    )
    result = proc.stdout.strip()

    NAME = r"ProductName:(.+)"  # noqa: N806
    VERSION = r"ProductVersion:(.+)"  # noqa: N806
    BUILD = r"BuildVersion:(.+)"  # noqa: N806

    def search_pattern(pattern):
        if matches := re.search(pattern, result):
            return matches[1].strip()
        return None  # pragma: no cover

    return {
        "name": search_pattern(NAME),
        "version": search_pattern(VERSION),
        "build": search_pattern(BUILD),
    }


@cache
def _get_mac_os_edition(version) -> str:
    """Get macOS edition."""
    editions = {
        # OS X
        "10.0": "Cheetah",
        "10.1": "Puma",
        "10.2": "Jaguar",
        "10.3": "Panther",
        "10.4": "Tiger",
        "10.5": "Leopard",
        "10.6": "Snow Leopard",
        "10.7": "Lion",
        "10.8": "Mountain Lion",
        "10.9": "Mavericks",
        "10.10": "Yosemite",
        "10.11": "El Capitan",
        "10.12": "Sierra",
        "10.13": "High Sierra",
        "10.14": "Mojave",
        "10.15": "Catalina",
        # macOS
        "11": "Big Sur",
        "12": "Monterey",
        "13": "Ventura",
        "14": "Sonoma",
        "15": "Sequoia",
    }

    if version in editions:
        return editions.get(version)

    major = version.split(".")[0]
    if major in editions:
        return editions.get(major)

    return "--"


@cache
def get_os_info() -> dict:
    """Return OS info as dict."""

    data = _get_mac_os()

    return {
        "name": data["name"],
        "version": data["version"],
        "edition": _get_mac_os_edition(data["version"]),
        "build": data["build"],
    }
