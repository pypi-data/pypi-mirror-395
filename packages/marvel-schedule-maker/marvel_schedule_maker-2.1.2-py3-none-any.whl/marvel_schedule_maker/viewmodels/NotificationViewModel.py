from PyQt6.QtCore import QObject, pyqtSignal, QTimer

from marvel_schedule_maker.models.NotificationTypes import NotificationType


class NotificationViewModel(QObject):
    """ViewModel for Notification - handles business logic and timing."""
    
    # Signals for view updates
    message_ready = pyqtSignal(str, NotificationType)  # message, type
    hide_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Timer for auto-hide
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide_requested.emit)
        
        # Configuration
        self._auto_hide_duration = 3000  # milliseconds
    
    def show_message(self, message: str, notification_type: NotificationType = NotificationType.SUCCESS):
        """Request to show a notification message."""
        self.message_ready.emit(message, notification_type)
        self._hide_timer.start(self._auto_hide_duration)
    
    def cancel_auto_hide(self):
        """Cancel the auto-hide timer."""
        self._hide_timer.stop()
    
    def set_auto_hide_duration(self, milliseconds: int):
        """Configure auto-hide duration."""
        self._auto_hide_duration = milliseconds