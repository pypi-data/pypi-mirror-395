import logging
import re
import shlex
import subprocess
from functools import cache

logger = logging.getLogger(__name__)


@cache
def _get_linux_os() -> dict:
    """Parse /etc/os-release file for name, version, and edition."""
    cmd = "cat /etc/os-release"
    proc = subprocess.run(  # noqa: S603
        shlex.split(cmd),
        check=True,
        capture_output=True,
        text=True,
    )
    # Dumb hack for now as makes regex easier
    result = proc.stdout.strip().replace("PRETTY_NAME", "PRETTY")

    ID = r"ID=\"(.+)\""  # noqa: N806
    NAME = r"NAME=\"(.+)\""  # noqa: N806
    VERSION = r"VERSION_ID=\"(.+)\""  # noqa: N806
    EDITION = r"VERSION_CODENAME=(.+)"  # noqa: N806

    def search_pattern(pattern):
        if matches := re.search(pattern, result):
            return matches[1].strip()
        return None

    return {
        "id": search_pattern(ID),
        "name": search_pattern(NAME),
        "version": search_pattern(VERSION),
        "edition": search_pattern(EDITION),
    }


@cache
def get_os_info() -> dict:
    """Return OS info as dict."""

    data = _get_linux_os()

    return {
        "name": data["name"],
        "version": data["version"],
        "edition": data["edition"],
        "build": "--",
    }
