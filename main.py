import logging
import datetime

from src.server.application import Application

from src.common.utilities.utility import Utility

from src.common.constants.constants import PATHS


def setup():
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


def main():
    setup()

    application = Application()
    application.run()


if __name__ == "__main__":
    main()
