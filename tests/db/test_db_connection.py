"""
Unit tests for Redis functions.
"""

import pytest
from src.db.connection import connect_to_redis


@pytest.mark.db_utils
def test_connect_to_redis_success():
    """
    Unit test to connect to redis, perform ping to test connectivity, then
        close the connection.
    """
    client = connect_to_redis()
    if client is not None:
        # Perform a simple ping Redis command to verify connection
        response = client.ping()
        assert response is True

        # Disconnect from Redis
        client.close()
    else:
        pytest.fail("Failed to connect to Redis.")
