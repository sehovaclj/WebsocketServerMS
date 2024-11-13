"""
This module provides the RedisManager class for managing interactions with
Redis. The RedisManager class connects to a Redis instance, subscribes to
channels for monitoring battery data, retrieves battery data, and allows
for dynamic subscription and unsubscription from Redis PubSub channels.
"""
import redis.client

from src.config.logging import LoggingConfig
from src.db.connection import connect_to_redis

logger = LoggingConfig.get_logger(__name__)


class RedisManager:
    """
    A class to manage Redis interactions for storing and publishing
        battery data.

    Attributes:
        battery_ids_key (str): Redis key where the list of battery IDs
            is stored.
        redis_client (redis.Redis): The Redis client connection.
        redis_pubsub (redis.client.PubSub): The Redis PubSub instance
            used for subscribing and unsubscribing from channels.
        channel_subscription_counts (dict): A dictionary to track the count
            of active subscriptions for each channel.
    """

    def __init__(self):
        """
        Initializes the RedisManager by connecting to Redis, defining
        the battery IDs key, and retrieving the list of existing battery IDs.
        """
        # connect to redis
        self.redis_client = connect_to_redis()
        # initialize the pubsub from the redis client
        self.redis_pubsub = self.redis_client.pubsub()
        # configure the info batteries id key
        self.battery_ids_key = 'info:batteries:ids'
        # keep track of channel subscription counts
        self.channel_subscription_counts = {}

    def get_battery_ids(self) -> set:
        """
        Fetch battery IDs from the info:batteries:ids set.

        Returns:
            set: A set of battery IDs as strings.
        """
        return self.redis_client.smembers(self.battery_ids_key)

    def get_battery_data(self) -> dict:
        """
        Retrieve data for all batteries based on battery IDs.

        Returns:
            dict: A dictionary with battery data, where each key is
                  the battery data channel and each value is the data.
        """
        battery_data = {}
        battery_ids = self.get_battery_ids()
        for battery_id in battery_ids:
            key = f'battery:{battery_id}:data'
            battery_data[key] = self.redis_client.get(key)
        return battery_data

    def subscribe_to_channels(self) -> redis.client.PubSub:
        """
        Subscribe to channels for each battery based on battery IDs.

        Returns:
            redis.client.PubSub: The Redis PubSub instance for the
                subscribed channels.
        """
        battery_ids = self.get_battery_ids()
        for battery_id in battery_ids:
            channel = f"battery:{int(battery_id)}:data"
            self.redis_pubsub.subscribe(channel)
            # Update the subscription count
            if channel in self.channel_subscription_counts:
                self.channel_subscription_counts[channel] += 1
            else:
                self.channel_subscription_counts[channel] = 1
            logger.info(
                "Subscribed to %s (count: %s)", channel,
                self.channel_subscription_counts[channel]
            )
        return self.redis_pubsub

    def unsubscribe_from_channels(self) -> None:
        """
        Unsubscribe from all channels for each battery based on battery IDs.
        """
        battery_ids = self.get_battery_ids()
        for battery_id in battery_ids:
            channel = f"battery:{battery_id}:data"
            self.redis_pubsub.unsubscribe(channel)
            # Update the subscription count
            if channel in self.channel_subscription_counts:
                self.channel_subscription_counts[channel] -= 1
                # Remove the channel if the count reaches zero
                if self.channel_subscription_counts[channel] <= 0:
                    del self.channel_subscription_counts[channel]
            logger.info(
                "Unsubscribed from %s (count: %s)", channel,
                self.channel_subscription_counts.get(channel, 0)
            )
