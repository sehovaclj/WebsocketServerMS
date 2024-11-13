"""
Main entry point for the FastAPI application with WebSocket support.

This module initializes a FastAPI application, sets up a WebSocket endpoint for
real-time communication, and configures logging. The WebSocketManager handles
connections and disconnections for WebSocket clients, and a background task
listens to Redis channels for broadcasting messages to connected clients.
"""

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.services.ws_manager import WebSocketManager
from src.config.logging import LoggingConfig
from src.config.ws import WsConfig

# Initialize FastAPI app and logger
app = FastAPI()
logger = LoggingConfig.get_logger(__name__)
# initialize our ws manager
ws_manager = WebSocketManager()


@app.websocket("/ws")
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
        # Keep the WebSocket connection open to receive data, if any
        while True:
            # Optional: Await client messages if needed, included this in case
            # we did want bidirectional communication with the websocket
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.error("Websocket client disconnected")
    finally:
        await ws_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host=WsConfig.WS_HOST, port=WsConfig.WS_PORT)
