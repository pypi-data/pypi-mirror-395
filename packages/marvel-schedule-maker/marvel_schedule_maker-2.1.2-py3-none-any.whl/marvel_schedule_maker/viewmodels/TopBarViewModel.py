import os
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class TopBarViewModel(QObject):

    # Signals
    file_dialog_requested = pyqtSignal(str, str)  # action: "open"/"save", suggested_path
    
    def __init__(self, services: ApplicationServices, parent=None):
        super().__init__(parent)

        self._services = services
        
        # File state
        self.current_file_path: Optional[str] = None
    
    # ==================== Query Methods ====================
    
    def generate_suggested_filename(self) -> str:
        """Create filename from observation date."""
        try:
            date_str = self._services.get_observation_date().strftime("%Y%m%d")
            return f"scheduler_{date_str}.csv"
        except:
            return "scheduler.csv"
    
    # ==================== New Schedule Operations ====================
    
    def request_new_schedule(self):
        """Create a new empty schedule."""
        self._services.new_schedule()
        self.current_file_path = None
    
    # ==================== Load Operations ====================
    
    def request_load_schedule(self):
        """Request to load schedule from file."""
        self.file_dialog_requested.emit("open", "")
    
    def load_schedule(self, filepath: str):
        """Load schedule from file."""
        if not filepath:
            return
        
        if not os.path.exists(filepath):
            self._services.show_error(f"File not found: {filepath}")
            return
        
        try:
            self._services.load_schedule(filepath)
            self.current_file_path = filepath
        except Exception as e:
            self._services.show_error(f"Failed to load: {str(e)}")
    
    # ==================== Save Operations ====================
    
    def request_save_schedule(self):
        """Request to save schedule (to current file or new file)."""
        if self.current_file_path:
            self.save_schedule(self.current_file_path)
        else:
            suggested = self.generate_suggested_filename()
            self.file_dialog_requested.emit("save", suggested)
    
    def save_schedule(self, filepath: str):
        """Save schedule to file."""
        if not filepath:
            return
        
        try:
            self._services.save_schedule(filepath)
            self.current_file_path = filepath
        except Exception as e:
            self._services.show_error(f"Failed to save: {str(e)}")
