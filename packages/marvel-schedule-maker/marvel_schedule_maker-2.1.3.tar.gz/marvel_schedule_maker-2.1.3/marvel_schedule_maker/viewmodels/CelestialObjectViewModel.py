from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Tuple

from marvel_schedule_maker.models.CelestialObjectModel import CelestialObjectModel
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class CelestialObjectViewModel(QObject):
    """
    ViewModel for celestial object catalog.
    Manages UI state and coordinates catalog operations.
    """
    
    # Signals
    catalog_loaded = pyqtSignal(list)  # List[Tuple[str, str, str]] for table display
    save_completed = pyqtSignal(bool, str)  # (success, message)
    
    def __init__(self, services: ApplicationServices):
        """Initialize ViewModel."""
        super().__init__()
        self.services = services
        self.model = CelestialObjectModel()
    
    # ==================== Query Methods ====================
    
    def load_objects(self) -> List[Tuple[str, str, str]]:
        """Load objects from catalog for display in table."""
        objects = self.model.get_all()
        
        # Convert floats to strings for table display
        display_data = [
            (name, ra, dec)
            for name, ra, dec in objects
        ]
        
        self.catalog_loaded.emit(display_data)
        return display_data
    
    def get_object_count(self) -> int:
        """Get number of objects in catalog."""
        return self.model.object_count()
    
    # ==================== Commands ====================
    
    def save_all(self, table_data: List[Tuple[str, str, str]]) -> None:
        """
        Save all objects from table data.
        Validates each row, shows errors, and persists to file.
        """
        errors = []
        success_count = 0
        
        # Clear existing catalog
        self.model.clear_all()
        
        # Add each row with validation
        for row_idx, (name, ra, dec) in enumerate(table_data):
            name = name.strip()
            ra = ra.strip()
            dec = dec.strip()
            
            # Skip empty rows
            if not name and not ra and not dec:
                continue
            
            # Validate and add
            success, error_msg = self.model.add_object(name, ra, dec)
            if success:
                success_count += 1
            else:
                errors.append(f"Row {row_idx + 1} ({name}): {error_msg}")
        
        # Persist to file
        save_success = self.model.save()
        
        # Show results and emit signal
        if errors:
            # Show first few errors in toast
            error_preview = "\n".join(errors[:3])
            if len(errors) > 3:
                error_preview += f"\n... and {len(errors) - 3} more errors"
            
            message = f"Saved {success_count} objects with {len(errors)} errors:\n{error_preview}"
            self.services.show_warning(message)
            self.save_completed.emit(False, message)
            
        elif not save_success:
            message = "Failed to save catalog to file"
            self.services.show_error(message)
            self.save_completed.emit(False, message)
            
        else:
            message = f"Successfully saved {success_count} celestial object(s)"
            self.services.show_success(message)
            self.save_completed.emit(True, message)
    
    def add_new_object(self) -> Tuple[str, str, str]:
        """Create default data for new object row."""
        return ("NEW_OBJECT", "0.0", "0.0")
    
    # ==================== Validation ====================
    
    def validate_row(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Validate a single row without adding to catalog."""
        return self.model.validate_object(name, ra, dec)