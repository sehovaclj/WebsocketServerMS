"""
Configures the Db parameters using environment variables.

Reads from a `.env` file to set Db parameters.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class DbConfig:
    """
    Configuration class for Db settings.

    This class loads the Db configuration from environment
        variables.
    """
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_DB = int(os.getenv('REDIS_DB'))
    REDIS_PASS = os.getenv('REDIS_PASS')
