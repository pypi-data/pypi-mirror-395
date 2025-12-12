from PyQt6.QtCore import QObject, pyqtSignal

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class MainWindowViewModel(QObject):
    """ViewModel for the main application window."""
    
    celestial_object_modal_visible_changed = pyqtSignal(bool)
    
    def __init__(self, services: ApplicationServices):
        super().__init__()
        self._services = services
        self._celestial_object_modal_visible = False
    
    def open_celestial_object_modal(self):
        """Open the settings modal."""
        self._celestial_object_modal_visible = True
        self.celestial_object_modal_visible_changed.emit(True)
    
    def close_celestial_object_modal(self):
        """Close the settings modal."""
        self._celestial_object_modal_visible = False
        self.celestial_object_modal_visible_changed.emit(False)
    
    def is_celestial_object_modal_visible(self) -> bool:
        """Check if settings modal is visible."""
        return self._celestial_object_modal_visible
