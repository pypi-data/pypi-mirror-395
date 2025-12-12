from enum import Enum, auto

from PyQt6.QtWidgets import QFrame, QWidget, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from marvel_schedule_maker.models.NotificationTypes import NotificationType
from marvel_schedule_maker.viewmodels.NotificationViewModel import NotificationViewModel


class NotificationPopup(QFrame):
    """Notification widget - pure presentation layer."""
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._parent = parent
        
        # Create ViewModel
        self._viewmodel = NotificationViewModel(parent=self)
        
        # Connect to ViewModel signals
        self._viewmodel.message_ready.connect(self._display_message)
        self._viewmodel.hide_requested.connect(self.hide)
        
        # Setup UI
        self._setup_ui()
        
        # Initially hidden
        self.hide()
    
    def _setup_ui(self):
        """Initialize UI components."""

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setAutoFillBackground(True)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15)
        
        # Icon Label
        self._icon_label = QLabel()
        self._icon_label.setFixedSize(28, 28)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Message label
        self._message_label = QLabel()
        self._message_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 500;
        """)
        self._message_label.setWordWrap(False)
        
        main_layout.addWidget(self._icon_label)
        main_layout.addWidget(self._message_label)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
    
    def show_message(self, message: str, notification_type: NotificationType = NotificationType.SUCCESS):
        """Public API: Request to show a message (delegates to ViewModel)."""
        self._viewmodel.show_message(message, notification_type)
    
    def _display_message(self, message: str, notification_type: NotificationType):
        """Internal: Display the message (called by ViewModel)."""
        if self._parent is None:
            return
        
        # Configure appearance based on type
        icon_text, icon_style, border_color = self._get_style_for_type(notification_type)
        
        self._icon_label.setText(icon_text)
        self._icon_label.setStyleSheet(icon_style)
        self._message_label.setText(message)
        
        # Update container styling
        self.setStyleSheet(f"""
            Notification {{
                background-color: white;
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        
        # Position and show
        self.adjustSize()
        x = (self._parent.width() - self.width()) // 2
        y = 20
        self.move(x, y)
        self.show()
        self.raise_()
    
    def _get_style_for_type(self, notification_type: NotificationType) -> tuple[str, str, str]:
        """Get icon text, icon style, and border color for notification type."""
        if notification_type == NotificationType.SUCCESS:
            return (
                "✓",
                "font-size: 22px; font-weight: bold; color: #28a745;",
                "#28a745"
            )
        elif notification_type == NotificationType.ERROR:
            return (
                "✖",
                "font-size: 20px; font-weight: bold; color: #dc3545;",
                "#dc3545"
            )
        else:  # WARNING
            return (
                "⚠",
                "font-size: 22px; font-weight: bold; color: #ffc107;",
                "#ffc107"
            )
