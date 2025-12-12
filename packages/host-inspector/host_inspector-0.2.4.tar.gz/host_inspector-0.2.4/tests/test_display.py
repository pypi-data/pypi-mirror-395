from host_inspector import get_display_info


def test_get_display_info():
    displays = get_display_info()
    assert isinstance(displays, list)
    for display in displays:
        assert isinstance(display, dict)
        assert set(display.keys()) == {
            "name",
            "display_id",
            "resolution_actual",
            "resolution",
            "refresh_rate",
        }
        assert isinstance(display["name"], str)
        assert isinstance(display["display_id"], int)
        assert isinstance(display["resolution_actual"], str)
        assert isinstance(display["resolution"], str)
        assert isinstance(display["refresh_rate"], str)
