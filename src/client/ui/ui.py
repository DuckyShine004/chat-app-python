"""This module provides an interface for interacting with the UI."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtCore import Qt, Signal

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
    ICONS,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)

if TYPE_CHECKING:
    from src.client.client import Client


class UI(QMainWindow):
    """The UI class manages anything UI related, such as invoking methods when
    the user presses a GUI element.

    Attributes:
        new_message_signal: the new message signal
        login_error_signal: the login error signal
        signup_error_signal: the signup error signal
        chat_label_signal: the chat label signal
        client: the client
        stacked_widget: the stacked widget
        login: the login instance
        login_widget: the login widget
        chat: the chat instance
        chat_widget: the chat widget
        signup: the signup instance
        signup_widget: the signup widget
        chat_layout: the chat layout
        is_password_visible: is the password visible
    """

    new_message_signal: Signal = Signal(str, dict)
    chat_label_signal: Signal = Signal(str)
    login_error_signal: Signal = Signal(str)
    signup_error_signal: Signal = Signal(str)

    def __init__(self, client: Client) -> None:
        """Initialises the UI instance fields.

        Args:
            client: the client instance
        """

        super().__init__()

        self.client: Client = client
        self.client.ui = self

        self.stacked_widget: QStackedWidget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login: Ui_Login = Ui_Login()
        self.login_widget: QWidget = QWidget()

        self.chat: Ui_Chat = Ui_Chat()
        self.chat_widget: QWidget = QWidget()

        self.signup: Ui_Signup = Ui_Signup()
        self.signup_widget: QWidget = QWidget()

        self.chat_layout: QVBoxLayout = None
        self.is_password_visible: int = 0

        self.initialise()

    def initialise(self) -> None:
        """Initialises the UI."""

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centre_window()

        self.initialise_login_page()
        self.initialise_signup_page()
        self.initialise_chat_page()

        self.show_login_page()

    def initialise_signup_page(self) -> None:
        """Initialises the signup page."""

        self.signup.setupUi(self.signup_widget)

        self.stacked_widget.addWidget(self.signup_widget)

        self.signup.sign_up_button.clicked.connect(self.handle_signup)

        self.signup.username_input.returnPressed.connect(self.handle_signup)

        self.signup.password_input.returnPressed.connect(self.handle_signup)
        self.signup.password_input.setEchoMode(QLineEdit.Password)
        self.signup.password_input.setTextMargins(0, 0, 35, 0)

        self.signup.eye_icon.mousePressEvent = self.toggle_signup_password_visibility

        self.signup.error_label.hide()

        self.signup_error_signal.connect(self.handle_server_signup)

    def initialise_login_page(self) -> None:
        """Initialises the login page."""

        self.login.setupUi(self.login_widget)

        self.stacked_widget.addWidget(self.login_widget)

        self.login.login_button.clicked.connect(self.handle_login)

        self.login.username_input.returnPressed.connect(self.handle_login)

        self.login.password_input.returnPressed.connect(self.handle_login)
        self.login.password_input.setEchoMode(QLineEdit.Password)
        self.login.password_input.setTextMargins(0, 0, 35, 0)

        self.login.sign_up_button.clicked.connect(self.show_signup_page)

        self.login.eye_icon.mousePressEvent = self.toggle_login_password_visibility

        self.login.error_label.hide()

        self.chat_label_signal.connect(self.handle_second_username)
        self.login_error_signal.connect(self.handle_server_login)

    def initialise_chat_page(self) -> None:
        """Initialises the chat page."""

        self.chat.setupUi(self.chat_widget)

        self.stacked_widget.addWidget(self.chat_widget)

        self.chat_layout = QVBoxLayout(self.chat.scrollAreaWidgetContents)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.chat.send_button.clicked.connect(self.handle_messaging)

        self.chat.message_input.returnPressed.connect(self.handle_messaging)

        self.chat.scrollArea.setWidgetResizable(True)
        self.chat.scrollArea.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.new_message_signal.connect(self.add_message)

    def centre_window(self) -> None:
        """Centres the application window."""

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        x = (screen_geometry.x() + (screen_geometry.width() - self.width())) // 2
        y = (screen_geometry.y() + (screen_geometry.height() - self.height())) // 2

        self.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def add_message(self, role: str, message: Any) -> None:
        """Adds a message to the chat based on the role.

        Args:
            role: the role can be client or server
            message: the message to be added
        """

        if role == "client":
            self.add_client_message(message["username"], message["content"])
        else:
            self.add_server_message(message["content"])

    def add_client_message(self, sender: str, message: str) -> None:
        """Adds a client message to the chat, based on who is sending it.

        Args:
            sender: the sender
            message: the message to be added
        """

        entry_layout = QVBoxLayout()
        entry_layout.setSpacing(0)

        name_label = QLabel(sender)
        name_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed))

        message_widget = MessageWidget(message, sender)
        message_layout = QHBoxLayout()

        if sender != "You":
            self.add_sender_message(message_widget, name_label, entry_layout, message_layout)
        else:
            self.add_receiver_message(message_widget, name_label, entry_layout, message_layout)

        entry_layout.addLayout(message_layout)

        self.chat_layout.addLayout(entry_layout)
        self.chat_layout.setSpacing(20)
        self.chat_layout.setContentsMargins(0, 10, 0, 0)

    def add_receiver_message(
        self,
        message_widget: MessageWidget,
        name_label: QLabel,
        entry_layout: QVBoxLayout,
        message_layout: QHBoxLayout,
    ) -> None:
        """Adds the receiver's message to the chat.

        Args:
            widget: the message widget
            name_label: the name label
            entry_layout: the entry layout
            message_layout: the message layout
        """

        name_label.setStyleSheet("color: white; font-weight: bold; margin-right: 10px;")
        entry_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignRight)
        message_layout.addStretch()
        message_layout.addWidget(message_widget)

    def add_sender_message(
        self,
        message_widget: MessageWidget,
        name_label: QLabel,
        entry_layout: QVBoxLayout,
        message_layout: QHBoxLayout,
    ) -> None:
        """Adds the sender's message to the chat.

        Args:
            widget: the message widget
            name_label: the name label
            entry_layout: the entry layout
            message_layout: the message layout
        """

        name_label.setStyleSheet("color: white; font-weight: bold; margin-left: 10px;")
        entry_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignLeft)
        message_layout.addWidget(message_widget)
        message_layout.addStretch()

    def add_server_message(self, message: str) -> None:
        """Adds a server message to the chat.

        Args:
            message: the message sent from the server
        """

        server_message_label = QLabel(message)
        server_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_message_label.setStyleSheet("color: #787b82; font-weight: bold;")

        entry_layout = QVBoxLayout()
        entry_layout.addWidget(server_message_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.chat_layout.addLayout(entry_layout)
        self.chat_layout.setSpacing(20)
        self.chat_layout.setContentsMargins(0, 10, 0, 0)

    def handle_second_username(self, second_username: str) -> None:
        """Handles the second user's username. It updates the chat title to
        reflect who the current user is chatting with.

        Args:
            second_username: the second user's username
        """

        self.chat.chat_label.setText(f"YOU ARE CHATTING WITH {second_username}")

    def handle_login(self) -> None:
        """Handles the client logging in."""

        username = self.login.username_input.text().strip()
        password = self.login.password_input.text().strip()

        self.client.send({"type": "client_login", "username": username, "password": password})

    def handle_signup(self) -> None:
        """Handles the client signing up and creating a new account."""

        username = self.signup.username_input.text().strip()
        password = self.signup.password_input.text().strip()

        self.client.send({"type": "client_signup", "username": username, "password": password})

    def handle_server_login(self, error: str = "") -> None:
        """Handles the client logging in.

        Args:
            error: the validity of the form submitted
        """

        if error:
            self.login.error_label.setText(f"\u26A0  {error}")
            self.login.error_label.show()

            return

        self.show_chat_page()

    def handle_server_signup(self, error: str = "") -> None:
        """Handles the client signing up.

        Args:
            error: the validity of the form submitted
        """

        if error:
            self.signup.error_label.setText(f"\u26A0  {error}")
            self.signup.error_label.show()
            return

        self.show_chat_page()

    def handle_messaging(self) -> None:
        """Handles the client sending messages to other clients."""

        message = self.chat.message_input.text().strip()

        if not message:
            return

        self.client.send({"type": "client_message", "message": message})

        self.add_client_message("You", message)
        self.chat.message_input.setText("")

    def toggle_login_password_visibility(self, event: Any) -> None:
        """Toggles the password visibility for the login page.

        Args:
            event:
        """

        self.set_password_visibility(self.login)

    def toggle_signup_password_visibility(self, event: Any) -> None:
        """Toggles the password visibility for the signup page.

        Args:
            event: the widget event
        """

        self.set_password_visibility(self.signup)

    def set_password_visibility(self, widget: Any) -> None:
        """Sets the password visibility for the login or signup page.

        Args:
            widget: the login or signup widget
        """

        self.is_password_visible ^= 1

        icon = ICONS[self.is_password_visible]
        widget.eye_icon.setStyleSheet(f"QLabel {{ image: url({icon}); background-color: transparent; }}")

        if self.is_password_visible:
            widget.password_input.setEchoMode(QLineEdit.Normal)
        else:
            widget.password_input.setEchoMode(QLineEdit.Password)

    def scroll_to_bottom(self, min_val: int = None, max_val: int = None) -> None:
        """Automatically scrolls the chat to the bottom.

        Args:
            min_val: the minimum scroll value
            max_val: the maximum scroll value
        """

        self.chat.scrollArea.verticalScrollBar().setValue(self.chat.scrollArea.verticalScrollBar().maximum())

    def show_login_page(self) -> None:
        """Switch to the login page."""

        self.stacked_widget.setCurrentWidget(self.login_widget)

    def show_chat_page(self) -> None:
        """Switch to the chat page."""

        self.chat.send_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.stacked_widget.setCurrentWidget(self.chat_widget)

    def show_signup_page(self) -> None:
        """Switch to the signup page."""

        self.is_password_visible = 0
        self.signup.username_input.setFocus()
        self.stacked_widget.setCurrentWidget(self.signup_widget)
