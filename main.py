"""The module containing the main driver code."""

from src.server.application import Application

from src.common.utilities.logger import Logger


def main() -> None:
    """The main driver code.

    Must only be called once the server connection has been established.
    """

    Logger.setup()

    Application().run()


if __name__ == "__main__":
    main()
