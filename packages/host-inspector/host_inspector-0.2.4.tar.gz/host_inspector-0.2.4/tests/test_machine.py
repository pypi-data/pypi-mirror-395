from host_inspector.machine import get_machine_id


def test_get_machine_id():
    if machine_id := get_machine_id():
        assert len(get_machine_id()) == 36  # noqa: PLR2004
    else:
        assert machine_id is None
