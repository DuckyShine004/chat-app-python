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

        # self.message_label = QLabel(Utility.get_wrapped_text(message, font, 420))
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.message_label)
        # layout.setAlignment(Qt.AlignmentFlag.AlignRight if sender == "You" else Qt.AlignmentFlag.AlignLeft)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setMaximumWidth(1000)  # Set maximum width
        self.message_label.setMaximumWidth(1000)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum))
        self.message_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))

        self.adjustSize()

    def set_css(self, sender):
        filename = "receiver" if sender == "You" else "sender"
        css = Utility.get_path(PATHS["resources"] + ["ui", "css", f"{filename}.css"])
        self.setStyleSheet(Utility.load_file_data(css))
