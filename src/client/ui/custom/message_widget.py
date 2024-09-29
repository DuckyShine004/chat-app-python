"""This module provides MessageWidget class used as part of the chat's GUI."""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from src.common.utilities.utility import Utility

from src.common.constants.constants import PATHS


class MessageWidget(QWidget):
    """The MessageWidget class is a child class of QWidget and defines the
    overall look of the message 'bubble'."""

    def __init__(self, message: str, sender: str = "You") -> None:
        """Initialises the MessageWidget instance.

        Args:
            message: the message
            sender: the sender
        """

        super().__init__()

        self.initialise(message, sender)

    def initialise(self, message: str, sender: str) -> None:
        """Initialises the MessageWidget by styling it.

        Args:
            message: the message
            sender: the sender
        """

        layout = QVBoxLayout()
        font = self.font()

        self.setLayout(layout)
        self.set_css(sender)

        message_label = QLabel(Utility.get_wrapped_text(message, font, 1000))
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        message_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred))

        layout.addWidget(message_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))

        self.adjustSize()

    def set_css(self, sender: str) -> None:
        """Sets the css stylesheet for the chat's message widget (bubble).

        Args:
            sender: the sender
        """

        filename = "receiver" if sender == "You" else "sender"
        css_file = Utility.get_path(PATHS["resources"] + ["ui", "css", f"{filename}.css"])

        self.setStyleSheet(Utility.load_file_data(css_file))
