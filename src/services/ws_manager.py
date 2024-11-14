"""
This module provides the WebSocketManager class, which manages WebSocket
connections and facilitates real-time communication with clients through
Redis PubSub channels. The WebSocketManager class handles the connection,
disconnection, and message broadcasting for WebSocket clients and listens
to Redis channels for battery data updates.
"""

import asyncio
from fastapi import WebSocket

from src.config.logging import LoggingConfig
from src.services.redis_manager import RedisManager
from src.utils.datetime_utils import utc_now_timestamp

# initialize the logger for this module
logger = LoggingConfig.get_logger(__name__)


class WebSocketManager:
    """
    A class to manage WebSocket connections, send initial battery data,
    and listen to Redis channels to broadcast updates in real time.

    Attributes:
        redis_manager (RedisManager): Instance of RedisManager for handling
            Redis interactions.
        active_connections (set): A set to track active WebSocket connections.
        redis_listener_task (Optional[asyncio.Task]): Task that listens to
        Redis channels for updates; started when first client connects and
            stopped when the last client disconnects.
    """

    def __init__(self):
        """
        Initializes the WebSocketManager with a RedisManager instance and an
        empty set of active WebSocket connections.
        """
        self.redis_manager = RedisManager()
        self.active_connections: set[WebSocket] = set()
        self.redis_listener_task: asyncio.Task | None = None

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accepts a WebSocket connection, adds it to the active connections set,
        and sends initial battery data to the client.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        await websocket.accept()
        logger.info("Client connected")
        self.active_connections.add(websocket)
        initial_data = self.redis_manager.get_battery_data()
        await websocket.send_json(initial_data)

        # Start the Redis listener if this is the first connection
        if not self.redis_listener_task:
            self.redis_listener_task = asyncio.create_task(
                self.listen_to_redis_channels())
            logger.info("Redis listener task started")
        else:
            # Simply subscribe to channels for this new connection
            self.redis_manager.subscribe_to_channels()

    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Removes a WebSocket connection from the active connections set
        and unsubscribes from all channels for that client.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
        """
        logger.info("Client disconnected")
        self.active_connections.remove(websocket)
        # Unsubscribe from all channels for the client
        self.redis_manager.unsubscribe_from_channels()

        # Stop the Redis listener if there are no active connections
        if not self.active_connections and self.redis_listener_task:
            self.redis_listener_task.cancel()
            try:
                await self.redis_listener_task
            except asyncio.CancelledError:
                logger.info("Redis listener task cancelled")
            self.redis_listener_task = None
            logger.info("Redis listener task stopped")

    async def broadcast(self, message: dict) -> None:
        """
        Sends a message to all active WebSocket connections.

        Args:
            message (dict): The message to be sent to each WebSocket client.
        """
        for connection in self.active_connections:
            await connection.send_json(message)

    async def listen_to_redis_channels(self) -> None:
        """
        Listens to Redis channels for updates, retrieves the latest data,
        and broadcasts it to all active WebSocket connections.
        """
        pubsub = self.redis_manager.subscribe_to_channels()
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                # Decode the channel name and data if they are in bytes
                channel = message.get('channel')
                if isinstance(channel, bytes):
                    channel = channel.decode('utf-8')

                # Extract the battery_id from the channel name
                # Channel format: "battery:{battery_id}:data"
                if channel.startswith("battery:") and channel.endswith(
                        ":data"):
                    battery_id = channel.split(":")[1]  # Extract battery_id

                    # Fetch the latest data for this battery from Redis
                    redis_key = f"battery:{battery_id}:data"
                    latest_data = self.redis_manager.redis_client.hgetall(
                        redis_key)

                    # Convert bytes to strings/integers as needed
                    latest_data = {k.decode('utf-8'): int(v) for k, v in
                                   latest_data.items()}

                    # Add a timestamp for WebSocket tracking
                    latest_data["ws_timestamp"] = utc_now_timestamp()

                    time_difference = latest_data["ws_timestamp"] - \
                                      latest_data["timestamp"]
                    latest_data["latency_ms"] = time_difference

                    # Broadcast the latest data
                    await self.broadcast({redis_key: latest_data})
            await asyncio.sleep(0.001)  # Prevent a tight loop, 1ms delay
