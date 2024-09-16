import sys

from PySide6.QtWidgets import QApplication

from src.client.ui.ui import UI

from src.client.client import Client

from src.common.utilities.logger import Logger

from src.common.constants.constants import WINDOW_TITLE


class Application:
    def __init__(self):
        self.client = Client()

        self.application = QApplication(sys.argv)
        self.ui = UI(self.client)

    def connect(self):
        Logger.info("Client: Waiting for server to respond")

        self.client.connect()

        Logger.info("Client: Connected to the server!")

    def run(self):
        self.connect()
        self.ui.show()
        self.quit()

    def quit(self):
        sys.exit(self.application.exec())
