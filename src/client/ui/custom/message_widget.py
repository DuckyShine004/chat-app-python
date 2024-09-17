from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from src.common.utilities.utility import Utility

from src.common.constants.constants import PATHS


class MessageWidget(QWidget):
    def __init__(self, message, sender="You"):
        super().__init__()

        layout = QVBoxLayout()
        font = self.font()

        self.setLayout(layout)
        self.set_css(sender)

        self.message_label = QLabel(Utility.get_wrapped_text(message, font, 1000))
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.message_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred))

        layout.addWidget(self.message_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))

        self.adjustSize()

    def set_css(self, sender):
        filename = "receiver" if sender == "You" else "sender"
        css = Utility.get_path(PATHS["resources"] + ["ui", "css", f"{filename}.css"])
        self.setStyleSheet(Utility.load_file_data(css))
