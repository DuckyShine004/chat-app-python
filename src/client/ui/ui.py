from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.client.ui.chat import Ui_Chat
from src.client.ui.login import Ui_Login
from src.client.ui.signup import Ui_Signup

from src.client.ui.custom.message_widget import MessageWidget

from src.common.constants.constants import (
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


class UI(QMainWindow):
    new_message = Signal(str, dict)
    login_error = Signal(str)
    signup_error = Signal(str)

    def __init__(self, client):
        super().__init__()

        self.client = client
        self.client.ui = self

        self.messages = []

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login = Ui_Login()
        self.login_widget = QWidget()

        self.chat = Ui_Chat()
        self.chat_widget = QWidget()

        self.signup = Ui_Signup()
        self.signup_widget = QWidget()

        self.is_password_visible = 0

        self.initialise()

    def initialise(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centre_window()

        self.login.setupUi(self.login_widget)
        self.chat.setupUi(self.chat_widget)
        self.signup.setupUi(self.signup_widget)

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.chat_widget)
        self.stacked_widget.addWidget(self.signup_widget)

        self.chat.scrollArea.setWidgetResizable(True)

        self.chat_layout = QVBoxLayout(self.chat.scrollAreaWidgetContents)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.login.login_button.clicked.connect(self.handle_login)
        self.login.username_input.returnPressed.connect(self.handle_login)
        self.login.password_input.returnPressed.connect(self.handle_login)
        self.login.password_input.setEchoMode(QLineEdit.Password)
        self.login.sign_up_button.clicked.connect(self.show_signup_page)

        self.signup.sign_up_button.clicked.connect(self.handle_signup)
        self.signup.username_input.returnPressed.connect(self.handle_signup)
        self.signup.password_input.returnPressed.connect(self.handle_signup)
        self.signup.password_input.setEchoMode(QLineEdit.Password)

        self.signup.eye_icon.mousePressEvent = self.toggle_signup_password_visibility
        self.login.eye_icon.mousePressEvent = self.toggle_login_password_visibility

        self.chat.send_button.clicked.connect(self.handle_messaging)
        self.chat.message_input.returnPressed.connect(self.handle_messaging)

        self.new_message.connect(self.add_message)
        self.login_error.connect(self.handle_server_login)
        self.login.password_input.setTextMargins(0, 0, 35, 0)
        self.signup_error.connect(self.handle_server_signup)
        self.signup.password_input.setTextMargins(0, 0, 35, 0)

        self.login.error_label.hide()
        self.signup.error_label.hide()

        self.chat.scrollArea.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.show_login_page()

    def centre_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        x = (screen_geometry.x() + (screen_geometry.width() - self.width())) // 2
        y = (screen_geometry.y() + (screen_geometry.height() - self.height())) // 2

        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def add_message(self, role, message):
        if role == "client":
            self.add_client_message(message["username"], message["content"])
        else:
            self.add_server_message(message["content"])

    def add_client_message(self, sender, message):
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
        self.chat_layout.setContentsMargins(0, 10, 0, 0)

    def add_server_message(self, message):
        server_message_label = QLabel(message)
        server_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_message_label.setStyleSheet("color: #787b82; font-weight: bold;")

        entry_layout = QVBoxLayout()
        entry_layout.addWidget(server_message_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.chat_layout.addLayout(entry_layout)
        self.chat_layout.setSpacing(20)
        self.chat_layout.setContentsMargins(0, 10, 0, 0)

    def handle_second_client(self):
        if self.client.id == 0:
            return

        self.client.send({"type": "receive_messages"})

    def handle_login(self):
        username = self.login.username_input.text().strip()
        password = self.login.password_input.text().strip()

        self.client.send({"type": "login", "username": username, "password": password})

    def handle_signup(self):
        username = self.signup.username_input.text().strip()
        password = self.signup.password_input.text().strip()

        self.client.send({"type": "client_signup", "username": username, "password": password})

    def handle_server_login(self, error=""):
        print(f"Server error: {error}")
        if error:
            self.login.error_label.setText(f"    {error}")
            self.login.error_label.show()

            return

        self.show_chat_page()
        self.handle_second_client()

    def handle_server_signup(self, error=""):
        if error:
            self.signup.error_label.setText(f"    {error}")
            self.signup.error_label.show()

            return

        self.show_chat_page()
        self.handle_second_client()

    def handle_messaging(self):
        message = self.chat.message_input.text().strip()

        if not message:
            return

        self.client.send({"type": "message", "message": message})

        self.add_client_message("You", message)
        self.chat.message_input.setText("")

    def toggle_login_password_visibility(self, event):
        icons = [":/icons/ui/icons/eye_closed.png", ":/icons/ui/icons/eye_opened.png"]
        self.is_password_visible ^= 1
        current_icon = icons[self.is_password_visible]
        self.login.eye_icon.setStyleSheet(f"QLabel {{ image: url({current_icon}); background-color: transparent; }}")

        if self.is_password_visible:
            self.login.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.login.password_input.setEchoMode(QLineEdit.Password)

    def toggle_signup_password_visibility(self, event):
        icons = [":/icons/ui/icons/eye_closed.png", ":/icons/ui/icons/eye_opened.png"]
        self.is_password_visible ^= 1
        current_icon = icons[self.is_password_visible]
        self.signup.eye_icon.setStyleSheet(f"QLabel {{ image: url({current_icon}); background-color: transparent; }}")

        if self.is_password_visible:
            self.signup.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.signup.password_input.setEchoMode(QLineEdit.Password)

    def scroll_to_bottom(self, min_val=None, max_val=None):
        self.chat.scrollArea.verticalScrollBar().setValue(self.chat.scrollArea.verticalScrollBar().maximum())

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_chat_page(self):
        self.chat.send_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        print("bruh")
        self.stacked_widget.setCurrentWidget(self.chat_widget)

    def show_signup_page(self):
        self.is_password_visible = 0
        self.stacked_widget.setCurrentWidget(self.signup_widget)
