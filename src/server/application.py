import sys

from PySide6.QtWidgets import QApplication

from src.client.ui.ui import UI

from src.client.client import Client

from src.common.utilities.logger import Logger


class Application:
    def __init__(self):
        self.client = Client()

        self.application = QApplication(sys.argv)
        self.ui = UI(self.client)

    def connect(self):
        Logger.info("Client: Waiting for server to respond with id")
        elapsed_time = self.client.connect()
        Logger.info(f"Client: Connected to the server with id: {self.client.id}!")
        Logger.info(f"Client: Connection took {elapsed_time} seconds")

    def run(self):
        self.connect()
        self.ui.show()

        self.quit()

    def quit(self):
        sys.exit(self.application.exec())
