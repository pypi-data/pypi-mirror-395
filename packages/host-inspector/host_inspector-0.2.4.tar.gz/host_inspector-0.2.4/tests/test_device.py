from host_inspector import get_device_info


def test_get_device_info():
    device_dict = get_device_info()
    assert isinstance(device_dict, dict)

    expected_keys = {"os", "platform", "network", "gpu", "display"}
    missing_keys = [key for key in expected_keys if key not in device_dict]
    assert not missing_keys, f"Missing keys: {missing_keys}"

    # assert set(device_info.keys()) == {"os", "platform", "network", "gpu", "display"}

    assert isinstance(device_dict["os"], dict)
    assert isinstance(device_dict["platform"], dict)
    assert isinstance(device_dict["network"], dict)
    assert isinstance(device_dict["gpu"], dict | list)
    assert isinstance(device_dict["display"], list)
