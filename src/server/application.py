"""This module provides application related APIs for the main driver code."""

import sys

from PySide6.QtWidgets import QApplication

from src.client.ui.ui import UI

from src.client.client import Client

from src.common.utilities.logger import Logger


class Application:
    """The application class provides API for running the chat application.

    Attributes:
        client: the client
        application: the pyqt application instance
        ui: the application UI
    """

    def __init__(self) -> None:
        """Initialises the application fields."""

        self.client: Client = Client()

        self.application: QApplication = QApplication(sys.argv)
        self.ui: UI = UI(self.client)

    def connect(self) -> None:
        """Connects the client to the server."""

        Logger.info("Client: Waiting for server to respond with id")
        elapsed_time = self.client.connect()
        Logger.info(f"Client: Connected to the server with id: {self.client.id}")
        Logger.info(f"Client: Connection took {elapsed_time} seconds")

    def run(self) -> None:
        """Run the application.

        Includes connecting the client to the server and initialising
        the UI.
        """

        self.connect()
        self.ui.show()
        self.quit()

    def quit(self) -> None:
        """Safely cleanup pyqt application."""

        sys.exit(self.application.exec())
