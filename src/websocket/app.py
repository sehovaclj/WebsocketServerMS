"""
Application setup module for the FastAPI application with WebSocket support.

This module provides the `create_app` function, which initializes and
configures the FastAPI app, including WebSocket routes for real-time
communication. The WebSocket routes are included from separate modules,
allowing modular app structure and scalability.
"""

from fastapi import FastAPI

from src.config.logging import LoggingConfig
from src.websocket.endpoints import router as websocket_router

# Initialize logger
logger = LoggingConfig.get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure a FastAPI application instance.

    Returns:
        FastAPI: The FastAPI application instance with WebSocket route support.
    """
    app = FastAPI()

    # Include the WebSocket router
    app.include_router(websocket_router)

    return app
