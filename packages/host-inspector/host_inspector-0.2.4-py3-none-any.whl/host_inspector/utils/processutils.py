import contextlib
import logging
import signal
import sys
import time
from functools import cache
from pathlib import Path

import psutil
import setproctitle

from .byteutils import human_readable_bytes
from .datetimeutils import human_delta

logger = logging.getLogger(__name__)


def set_process_title(title: str) -> None:
    """Set the process title."""
    if sys.platform == "darwin":
        setproctitle.setproctitle(title)


@cache
def get_process() -> psutil.Process:
    """Return the current process."""
    return psutil.Process()


def get_mem_usage(process: psutil.Process) -> str:
    """Return memory usage in human readable units."""
    mem_info = process.memory_info()
    return human_readable_bytes(mem_info.rss, metric=False)


def get_vmem_usage(process: psutil.Process) -> str:
    """Return virtual memory usage in human readable units."""
    mem_info = process.memory_info()
    return human_readable_bytes(mem_info.vms, metric=False)


def get_mem_usage_perc(process: psutil.Process) -> str:
    """Return memory usage as a percent."""
    mem_usage = process.memory_percent()
    return f"{round(mem_usage, 2)}%"


def get_proc_usage(process: psutil.Process) -> str:
    """Return memory usage in MB."""
    cpu_usage = process.cpu_percent()
    return f"{cpu_usage}%"


def get_process_by_name(name) -> psutil.Process | None:
    """Return a Process or None."""
    if isinstance(name, Path):
        # macOS uses the stem, Linux/Windows uses the name
        name = name.stem if sys.platform == "darwin" else name.name

    name = name.lower()
    for proc in psutil.process_iter(["name", "cmdline"]):
        try:
            proc_name = proc.name().lower()
            if proc_name == name:
                return proc

            if sys.platform == "linux":
                for arg in proc.cmdline():
                    if name in Path(arg).name.lower():
                        return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # logger.warning("Could not access process: %s", name)
            continue
    return None


def get_process_by_pid(pid: int) -> psutil.Process | None:
    """Return a Process or None."""
    with contextlib.suppress(psutil.NoSuchProcess):
        return psutil.Process(pid)
    return None


def is_process_running_by_name(name) -> bool:
    if isinstance(name, Path):
        # macOS uses the stem, Linux/Windows uses the name
        name = name.stem if sys.platform == "darwin" else name.name
    return proc.is_running() if (proc := get_process_by_name(name)) else False


def is_process_running_by_pid(pid) -> bool:
    return get_process_by_pid(pid).is_running()


def kill_process(process: psutil.Process) -> bool:
    """
    Kill a given process.

    :param process: psutil.Process object
    :return: bool
    """
    try:
        process.kill()
        process.wait(timeout=3)
        return True
    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
        psutil.TimeoutExpired,
    ):
        logger.error(  # noqa: TRY400
            "Failed to kill process %s with PID %s", process.info["name"], process.pid
        )
        return False


def kill_child_processes(parent_pid, sig=signal.SIGTERM) -> None:
    """Kill child processes. Untested."""
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for child in children:
        child.send_signal(sig)
        # child.kill()
    parent.kill()


def get_uptime(process: psutil.Process) -> int:
    """Return the uptime of a process in seconds."""
    return int(time.time() - process.create_time())


def get_uptime_as_string(process: psutil.Process) -> str:
    """Return uptime as string."""
    return human_delta(get_uptime(process))
