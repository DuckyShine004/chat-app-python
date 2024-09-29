"""The module containing the main driver code."""

import logging
import datetime

from src.server.application import Application

from src.common.utilities.utility import Utility

from src.common.constants.constants import PATHS


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


def main() -> None:
    """The main driver code.

    Must only be called once the server connection has been established.
    """

    setup()

    Application().run()


if __name__ == "__main__":
    main()
