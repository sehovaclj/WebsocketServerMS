import pytest
from datetime import datetime, timezone
from src.utils.datetime_utils import utc_now_timestamp


@pytest.mark.datetime_utils
def test_utc_now_timestamp():
    # Get the current timestamp
    timestamp = utc_now_timestamp()

    # Assert that the timestamp is an integer
    assert isinstance(timestamp, int), "The timestamp should be an integer."

    # Assert that the timestamp is close to the current UTC time
    current_timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    tolerance = 1000  # 1 second tolerance in milliseconds
    assert abs(
        current_timestamp - timestamp) < tolerance, "The timestamp should be close to the current UTC time."
