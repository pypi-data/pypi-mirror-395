from host_inspector import get_gpu_info


def test_get_gpu_info():
    gpu_info = get_gpu_info()
    assert isinstance(gpu_info, dict | list)

    expected_keys = {"model", "vram", "resolution", "refresh_rate"}

    assert isinstance(gpu_info, dict | list)
    if isinstance(gpu_info, dict):
        assert set(gpu_info.keys()) == expected_keys
    elif isinstance(gpu_info, list):
        for item in gpu_info:
            assert isinstance(item, dict)
            assert set(item.keys()) == expected_keys
