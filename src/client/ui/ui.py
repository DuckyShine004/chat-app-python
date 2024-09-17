from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QSizePolicy,
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
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centre_window()

        self.login.setupUi(self.login_widget)
        self.chat.setupUi(self.chat_widget)

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.chat_widget)

        self.chat.scrollArea.setWidgetResizable(True)

        self.chat_layout = QVBoxLayout(self.chat.scrollAreaWidgetContents)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.login.login_button.clicked.connect(self.handle_login)
        self.login.username_input.returnPressed.connect(self.handle_login)

        self.chat.send_button.clicked.connect(self.handle_messaging)
        self.chat.message_input.returnPressed.connect(self.handle_messaging)

        self.show_login_page()

    def centre_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        x = (screen_geometry.x() + (screen_geometry.width() - self.width())) // 2
        y = (screen_geometry.y() + (screen_geometry.height() - self.height())) // 2

        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def add_message(self, sender, message):
        entry_layout = QVBoxLayout()
        entry_layout.setSpacing(0)

        name_label = QLabel(sender)
        name_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed))

        message_widget = MessageWidget(message, sender)
        message_layout = QHBoxLayout()

        if sender != "You":
            name_label.setStyleSheet("color: white; font-weight: bold; margin-left: 10px;")
            entry_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignLeft)
            message_layout.addWidget(message_widget)
            message_layout.addStretch()
        else:
            name_label.setStyleSheet("color: white; font-weight: bold; margin-right: 10px;")
            entry_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignRight)
            message_layout.addStretch()
            message_layout.addWidget(message_widget)

        entry_layout.addLayout(message_layout)

        self.chat_layout.addLayout(entry_layout)

        self.chat_layout.setSpacing(20)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)

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

        self.client.send({"type": "login", "username": username})
        self.show_chat_page()

    def handle_login_error(self):
        self.login.username_input.move(480, 550)
        self.login.login_title_label.move(480, 460)
        self.login.error_label.show()

    def handle_messaging(self):
        message = self.chat.message_input.text().strip()

        if not message:
            return

        self.client.send(message)
        self.chat.message_input.setText("")

    def show_login_page(self):
        self.login.error_label.hide()
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_chat_page(self):
        self.chat.send_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.stacked_widget.setCurrentWidget(self.chat_widget)

        for _ in range(5):
            self.add_message("You", "brother I am")
            self.add_message("Bruh", "brother I am not the one that is everything that I have")
