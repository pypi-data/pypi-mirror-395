from typing import List, Tuple, Optional

from marvel_schedule_maker.repository.CelestialObjectRepository import CelestialObjectRepository
from marvel_schedule_maker.models.ActionFieldModel import Ra, Dec


class CelestialObjectModel:
    """
    MVVM Model for celestial objects.
    Provides validation layer over CelestialObjectRepository.
    """
    
    def __init__(self, catalog_path: Optional[str] = None):
        """Initialize model with repository."""
        self._repo = CelestialObjectRepository(catalog_path)
    
    # ==================== Query Methods ====================
    
    def get_all(self) -> List[Tuple[str, str, str]]:
        """ Get all objects as list of tuples for display. """
        all_objects = self._repo.get_all()
        result = []
        for name, entry in all_objects.items():
            result.append((name, entry.RA, entry.DEC))
        return result
    
    def get_object(self, name: str) -> Optional[Tuple[str, str]]:
        """Get object coordinates."""
        entry = self._repo.get(name)
        if not entry:
            return None
        return (entry.RA, entry.DEC)
    
    def object_count(self) -> int:
        """Get number of objects in catalog."""
        return len(self._repo)
    
    # ==================== Persistence ====================
    
    def load(self) -> bool:
        """Reload catalog from file."""
        return self._repo.load()
    
    def save(self) -> bool:
        """Persist catalog to file."""
        return self._repo.save()
    
    # ==================== CRUD Operations ====================
    
    def add_object(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Add object with validation (in-memory)."""
        is_valid, error_msg = self.validate_object(name, ra, dec)
        if not is_valid:
            return (False, error_msg)
        success = self._repo.add(name, ra, dec)
        return (success, "" if success else "Failed to add object to catalog")
    
    def remove_object(self, name: str) -> bool:
        """Remove object from catalog (in-memory)."""
        return self._repo.delete(name)
    
    def clear_all(self) -> None:
        """Clear all objects from catalog (in-memory)."""
        self._repo.clear()
    
    # ==================== Validation ====================
    
    def validate_object(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Validate object data using ActionFieldModel validators."""
        # Check name
        if not name or not name.strip():
            return (False, "Object name cannot be empty")
        
        # Validate RA using existing validator
        ra_parsed = Ra.parse(ra)
        if ra_parsed is None:
            return (False, f"Invalid RA format: '{ra}'. Expected format: 18.072497 or 18:04:20.99")
        
        # Validate DEC using existing validator
        dec_parsed = Dec.parse(dec)
        if dec_parsed is None:
            return (False, f"Invalid DEC format: '{dec}'. Expected format: 41.268750 or 41:16:07.5")
        
        return (True, "")