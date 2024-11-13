"""
Configures the Ws Server parameters using environment variables.

Reads from a `.env` file to set Ws Server parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class WsConfig:
    """
    Configuration class for Ws settings.

    This class loads the Ws configuration from environment
        variables.
    """
    WS_HOST = os.getenv('WS_HOST')
    WS_PORT = int(os.getenv('WS_PORT'))
