from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem, QWidget

from src.client.ui.custom.message_label import MessageLabel


class MessageWidget(QWidget):
    def __init__(self, message, is_right=True):
        super().__init__()

        layout = QHBoxLayout()
        self.label = MessageLabel(message)
        layout.addWidget(self.label)

        self.handle_alignment(layout, is_right)

    def handle_alignment(self, layout, is_right):
        if is_right:
            layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))

        layout.addWidget(self.label)

        if not is_right:
            layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))

        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)
