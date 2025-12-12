from host_inspector.os import get_os_info
from host_inspector.os.mac import _get_mac_os_edition


def test_get_os_info():
    os_info = get_os_info()

    assert isinstance(os_info, dict)

    required_keys = {"name", "version", "edition", "build"}
    assert required_keys.issubset(os_info.keys())

    # If you want to check that the values are not None
    for key, value in os_info.items():
        assert value is not None, f'Key "{key}" is None.'


def test_get_mac_os_edition():
    assert _get_mac_os_edition("10.15") == "Catalina"
    assert _get_mac_os_edition("11") == "Big Sur"
    assert _get_mac_os_edition("12") == "Monterey"
    assert _get_mac_os_edition("13") == "Ventura"
    assert _get_mac_os_edition("14") == "Sonoma"
    assert _get_mac_os_edition("99") == "--"
