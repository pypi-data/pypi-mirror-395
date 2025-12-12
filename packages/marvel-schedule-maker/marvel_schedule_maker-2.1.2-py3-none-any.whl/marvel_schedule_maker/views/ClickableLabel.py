from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor


class ClickableLabel(QLabel):
    """QLabel that emits clicked signal when clicked."""
    clicked = pyqtSignal()
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent=parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QLabel {
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }
            QLabel:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
        """)
    
    def mousePressEvent(self, event):
        """Emit clicked signal on left click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            return
        super().mousePressEvent(event)
            