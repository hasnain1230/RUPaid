import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

class ScaledPixmapLabel(QLabel):
    def __init__(self, pixmap_path, parent=None):
        super().__init__(parent)
        self.pixmap_path = pixmap_path
        self.original_pixmap = QPixmap(pixmap_path)

    def resizeEvent(self, event):
        scaled_pixmap = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        # Print the current path of current python file
        super().resizeEvent(event)
