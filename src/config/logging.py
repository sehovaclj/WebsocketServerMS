"""
This module provides a LoggingConfig class for configuring logging settings
with a specific log level and timestamp format that includes milliseconds.
"""

import logging
import sys


class LoggingConfig:
    """
    Configures logging settings for an application,
    including log level and format.
    """

    # Set the desired logging level
    LOG_LEVEL = logging.INFO

    # Define a logging formatter that includes milliseconds in the timestamp
    LOG_FORMATTER = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        """
        Retrieves a logger configured to output to stdout with the
        specified format. For more extensive logging, configure it to write
        to a file, then use a monitoring tool such as Prometheus or Grafana
        Loki. For now, to speed up and reduce overhead, print to stdout and
        check Docker logs.

        Args:
            name (str): The name for the logger (default is the module's
            __name__).

        Returns:
            logging.Logger: A logger instance with stdout handler and
            custom formatter.
        """
        logger = logging.getLogger(name)
        logger.setLevel(LoggingConfig.LOG_LEVEL)

        # Avoid adding multiple handlers if logger already has one
        if not logger.hasHandlers():
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(LoggingConfig.LOG_FORMATTER)
            logger.addHandler(stdout_handler)

        return logger
