"""
This module provides utility functions for working with date and time.
"""

from datetime import datetime, timezone


def utc_now_timestamp() -> int:
    """
    Gets the current UTC time as a timestamp in milliseconds.

    Returns:
        int: The current UTC timestamp in milliseconds since the Unix epoch.
    """
    return int(datetime.now(timezone.utc).timestamp() * 1000)
