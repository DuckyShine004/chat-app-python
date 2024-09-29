"""This module provides custom defined logging APIs."""

import logging

from typing import Any


class Logger:
    """The Logger class provides global static methods that can be used by
    other classes to log events.

    Attributes:
        __LOGGER: the logger
    """

    __LOGGER: Any = logging.getLogger()

    @staticmethod
    def info(message: str) -> None:
        """Logs information.

        Args:
            message: the message to be logged
        """

        Logger.__LOGGER.info(message)

    @staticmethod
    def warn(message: str) -> None:
        """Logs warning.

        Args:
            message: the message to be logged
        """

        Logger.__LOGGER.warning(message)

    @staticmethod
    def error(message: str) -> None:
        """Logs error.

        Args:
            message: the message to be logged
        """

        Logger.__LOGGER.error(message)
