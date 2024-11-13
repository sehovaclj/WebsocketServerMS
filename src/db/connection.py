"""
This module handles connection to a Redis instance with logging.

Functions:
    connect_to_redis() -> Union[redis.StrictRedis, None]:
        Connects to Redis and returns the client if successful; logs and
        returns None on failure.
"""

from typing import Union

import redis

from src.config.logging import LoggingConfig
from src.config.db import DbConfig

# Configure the logger
logger = LoggingConfig.get_logger(__name__)


def connect_to_redis() -> Union[redis.StrictRedis, None]:
    """
    Connects to a Redis instance and returns the Redis client if the
        connection is successful.

    Returns:
        redis.StrictRedis or None: Redis client if connected, None otherwise.
    """
    try:
        client = redis.StrictRedis(
            host=DbConfig.REDIS_HOST,
            port=DbConfig.REDIS_PORT,
            db=DbConfig.REDIS_DB,
            password=DbConfig.REDIS_PASS,
            decode_responses=False
        )
        # Test the connection
        if client.ping():
            logger.info("Successfully connected to Redis.")
            return client
    except redis.ConnectionError as err:
        logger.error("Failed to connect to Redis: %s", err)
        return None
