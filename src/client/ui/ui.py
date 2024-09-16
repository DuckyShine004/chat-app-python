from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.client.ui.chat import Ui_Chat
from src.client.ui.login import Ui_Login

from src.client.ui.custom.message_widget import MessageWidget

from src.common.constants.constants import (
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


class UI(QMainWindow):
    def __init__(self, client):
        super().__init__()

        self.client = client

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_widget = QWidget()
        self.login = Ui_Login()

        self.chat = Ui_Chat()
        self.chat_widget = QWidget()

        self.initialise()

    def initialise(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.centre_window()

        self.login.setupUi(self.login_widget)
        self.chat.setupUi(self.chat_widget)

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.chat_widget)

        self.chat.scrollArea.setWidgetResizable(True)
        self.chat_layout = QVBoxLayout(self.chat.scrollAreaWidgetContents)
        # self.chat_layout = QVBoxLayout()

        self.login.login_button.clicked.connect(self.handle_login)

        self.show_login_page()

    def centre_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        x = (screen_geometry.x() + (screen_geometry.width() - self.width())) // 2
        y = (screen_geometry.y() + (screen_geometry.height() - self.height())) // 2

        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def add_message(self, sender, message):
        message_widget = MessageWidget(message, sender)

        container_layout = QHBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(message_widget)

        self.chat_layout.addLayout(container_layout)
        self.chat.scrollArea.verticalScrollBar().setValue(self.chat.scrollArea.verticalScrollBar().maximum())

    def send_message(self):
        message = self.chat.message_input.text().strip()

        if not message:
            return

        self.add_message("You", message)

    def handle_login(self):
        username = self.login.username_input.text().strip()

        if not username:
            self.handle_login_error()
            return

        self.client.send(username)
        self.show_chat_page()

    def handle_login_error(self):
        self.login.username_input.move(480, 550)
        self.login.login_title_label.move(480, 460)
        self.login.error_label.show()

    def show_login_page(self):
        self.login.error_label.hide()
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_chat_page(self):
        self.stacked_widget.setCurrentWidget(self.chat_widget)

        for _ in range(2):
            self.add_message(
                "bruh", "fjksadlfjksladfjklsdajfdklasadhjfkjlsadhfjksdahkjfhsadkjfhsakjfhsajkdfhjksadf1hkjsdafhjksadhfjkashkfj"
            )
