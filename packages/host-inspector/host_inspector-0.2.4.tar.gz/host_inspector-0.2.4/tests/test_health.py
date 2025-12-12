from host_inspector import get_health_info


def test_get_health_info():
    health_dict = get_health_info()
    assert isinstance(health_dict, dict)

    expected_keys = {"cpu", "mem", "disk", "uptime", "local_datetime"}
    missing_keys = [key for key in expected_keys if key not in health_dict]
    assert not missing_keys, f"Missing keys: {missing_keys}"

    for value in health_dict.values():
        assert isinstance(value, dict)
