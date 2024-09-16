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

        self.message_label = QLabel(Utility.get_wrapped_text(message, font, 440))
        self.message_label.setWordWrap(True)

        layout.addWidget(self.message_label)

        css_path = Utility.get_path(PATHS["resources"] + ["ui", "css", "message.css"])
        self.setStyleSheet(Utility.load_file_data(css_path))

        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed))
        self.message_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed))

        self.adjustSize()

    def sizeHint(self):
        return QSize(self.message_label.sizeHint().width(), self.message_label.sizeHint().height() + 20)
