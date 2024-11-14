"""
WebSocket route definition for real-time communication.

This module provides an endpoint to handle WebSocket connections, allowing
clients to connect, stay updated with messages, and disconnect gracefully.
The WebSocketManager manages connections and disconnections for each client.

"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.services.ws_manager import WebSocketManager
from src.config.logging import LoggingConfig

# Initialize logger and WebSocket manager
logger = LoggingConfig.get_logger(__name__)
ws_manager = WebSocketManager()

# Create a router specifically for WebSocket routes
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time communication.

    This endpoint accepts a WebSocket connection, registers it with the
    WebSocketManager, and listens for messages from Redis channels via
    the background task started in `startup_event`. When the connection
    is closed, it is properly removed.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
    """
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.error("WebSocket client disconnected")
    finally:
        await ws_manager.disconnect(websocket)
