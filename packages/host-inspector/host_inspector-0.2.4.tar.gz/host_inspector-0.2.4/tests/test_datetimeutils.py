import datetime
from datetime import UTC

from host_inspector.utils import datetimeutils


def test_human_date():
    dt = datetime.datetime(2024, 8, 6, tzinfo=UTC)
    assert datetimeutils.human_date(dt) == "Tuesday, August 6, 2024"


def test_human_date_short():
    dt = datetime.datetime(2024, 8, 6, tzinfo=UTC)
    assert datetimeutils.human_date_short(dt) == "Tue, Aug 6, 2024"


def test_human_time():
    dt = datetime.datetime(2024, 8, 6, 15, 30, tzinfo=UTC)
    assert datetimeutils.human_time(dt) == "3:30 PM"


def test_human_datetime():
    dt = datetime.datetime(2024, 8, 6, 15, 30, tzinfo=UTC)
    assert datetimeutils.human_datetime(dt) == "Tuesday, August 6, 2024 3:30 PM"


def test_human_datetime_short():
    dt = datetime.datetime(2024, 8, 6, 15, 30, tzinfo=UTC)
    assert datetimeutils.human_datetime_short(dt) == "Tue, Aug 6, 2024 3:30 PM"


def test_human_delta():
    # Example: 3661 seconds = "1 hour, 1 minute"
    result = datetimeutils.human_delta(3661)
    assert "hour" in result or "minute" in result
