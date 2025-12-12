from host_inspector.platform import get_platform_info


def test_get_model():
    info = get_platform_info()

    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "system",
        "release",
        "machine",
        "architecture",
        "manufacturer",
        "model",
        "serial",
    }

    # If you want to check that the values are not None
    for key, value in info.items():
        assert value is not None, f'Key "{key}" is None.'
