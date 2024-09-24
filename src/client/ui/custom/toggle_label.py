from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class ToggleLabel(QLabel):
    def __init__(self, images, parent=None):
        super().__init__(parent)

        self.images = images
        self.image_index = 0

        self.set_image()

    def set_image(self):
        current_image = self.images[self.image_index]
        self.setStyleSheet(f"QLabel {{ image: url({current_image}); background-color: transparent; }}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.image_index ^= 1

        self.set_image()
