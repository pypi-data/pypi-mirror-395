from host_inspector import get_cpu_info


def test_get_cpu_info():
    cpu_info = get_cpu_info()

    assert isinstance(cpu_info, dict)
    assert set(cpu_info.keys()) == {
        "count",
        "logical",
        "percent",
        "percent_str",
        "processor",
        "frequency",
        "frequency_str",
        "temperature",
    }

    # If you want to check that the values are not None
    for key, value in cpu_info.items():
        assert value is not None, f'Key "{key}" is None.'
