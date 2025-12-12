import json
import re
import subprocess
from typing import Any

_RES_RE = re.compile(r"^\s*(\d+)\s*x\s*(\d+)(?:\s*@\s*([\d.]+)\s*Hz)?\s*$", re.I)


def _parse_res(
    res_str: str | None,
) -> tuple[int | None, int | None, float | None]:
    """Parse strings like '3440 x 1440 @ 60.00Hz' or '1728 x 1117'."""
    if not res_str or not isinstance(res_str, str):
        return None, None, None
    m = _RES_RE.search(res_str)
    if not m:
        return None, None, None
    w = int(m.group(1))
    h = int(m.group(2))
    hz = float(m.group(3)) if m.group(3) else None
    return w, h, hz


def _to_int_maybe(s: Any) -> int | None:
    try:
        return int(str(s).strip())
    except ValueError:  # pragma: no cover
        return None


def _parse_display_output(sp_json) -> list[dict[str, Any]]:
    """
    Return only name, display_id, resolution_actual, pixel_resolution, refresh_hz
    from macOS 'system_profiler SPDisplaysDataType -json'.
    """
    out = []
    for gpu in sp_json.get("SPDisplaysDataType", []):
        for drv in gpu.get("spdisplays_ndrvs", []) or []:
            name = drv.get("_name") or "Display"

            # Actual (scaled) UI resolution + refresh (from *_resolution fields)
            res_str = (
                drv.get("_spdisplays_resolution")
                or drv.get("spdisplays_resolution")
                or drv.get("_spdisplays_pixels")  # fallback if only pixels exist
            )
            act_w, act_h, hz = _parse_res(res_str)

            # Native panel pixel resolution (from *_pixels)
            px_str = drv.get("_spdisplays_pixels")
            px_w, px_h, _ = _parse_res(px_str)

            # Display ID
            display_id = _to_int_maybe(drv.get("_spdisplays_displayID"))

            out.append(
                {
                    "name": name,
                    "display_id": display_id,
                    "resolution_actual": f"{act_w} x {act_h}",
                    "resolution": f"{px_w} x {px_h}",
                    "refresh_rate": f"{hz} Hz" if hz else "--",
                }
            )
    return out


def get_display_info() -> list[dict[str, Any]]:
    try:
        cmd = ["system_profiler", "SPDisplaysDataType", "-json"]
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)  # noqa: S603
        all_info = proc.stdout.strip()
        return _parse_display_output(json.loads(all_info))
    except subprocess.CalledProcessError:  # pragma: no cover
        return []
