"""
Main entry point for the FastAPI application with WebSocket support.

This module initializes and runs the FastAPI application using Uvicorn. The
application is created via the `create_app` function from `src.websocket.app`,
and it includes WebSocket routes and logging configuration.

"""

import uvicorn
from src.websocket.app import create_app
from src.config.ws import WsConfig

app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app",
                host=WsConfig.WS_HOST,
                port=WsConfig.WS_PORT)
