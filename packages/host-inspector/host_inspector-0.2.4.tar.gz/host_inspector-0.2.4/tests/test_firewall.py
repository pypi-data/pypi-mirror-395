import sys

import pytest

from host_inspector import get_firewall_info
from host_inspector.firewall import is_firewall_enabled


@pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
@pytest.mark.parametrize(
    ("ports", "direction", "enabled_only", "exclude_any_ports"),
    [
        ([80], "in", True, False),
        ([22, 443], "out", False, True),
        ([], "in", False, False),
    ],
)
def test_get_firewall_info(ports, direction, enabled_only, exclude_any_ports):
    firewall_info = get_firewall_info(
        ports=ports,
        direction=direction,
        enabled_only=enabled_only,
        exclude_any_ports=exclude_any_ports,
    )
    assert isinstance(firewall_info, dict)
    assert "status" in firewall_info
    assert "rules" in firewall_info
    assert isinstance(firewall_info["rules"], list)


@pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
def test_get_firewall_info_empty_ports():
    firewall_info = get_firewall_info(ports=[])
    assert isinstance(firewall_info, dict)
    assert "status" in firewall_info
    assert "rules" in firewall_info


def test_ensure_rules_not_empty():
    if not is_firewall_enabled():
        pytest.skip("Firewall is not enabled; skipping test.")
    firewall_info = get_firewall_info()
    assert isinstance(firewall_info, dict)
    assert "rules" in firewall_info
    assert isinstance(firewall_info["rules"], list)
    assert len(firewall_info["rules"]) > 0, "Firewall rules should not be empty"


# @pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
# def test_check_firewall_status():
#     result = check_firewall_status()
#     assert isinstance(result, bool)


# @pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
# def test_is_firewall_enabled():
#     enabled = is_firewall_enabled()
#     assert isinstance(enabled, bool)
