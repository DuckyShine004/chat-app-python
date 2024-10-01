"""This module provides custom defined logging APIs."""

import logging
import datetime

from typing import Any

from src.common.utilities.utility import Utility

from src.common.constants.constants import PATHS


class Logger:
    """The Logger class provides global static methods that can be used by
    other classes to log events.

    Attributes:
        __LOGGER: the logger
    """

    __LOGGER: Any = logging.getLogger()

    @staticmethod
    def setup() -> None:
        """Perform application configurations before running the chat
        application."""

        filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        path = Utility.get_path(PATHS["logs"], [filename])

        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s - %(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(path),
                logging.StreamHandler(),
            ],
        )

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
