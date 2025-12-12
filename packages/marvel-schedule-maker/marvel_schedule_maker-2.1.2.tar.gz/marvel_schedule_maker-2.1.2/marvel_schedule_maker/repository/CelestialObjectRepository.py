import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class CelestialObjectEntry:
    """Data class for celestial object catalog entries."""
    RA: str
    DEC: str

    def to_dict(self) -> Dict[str, str]:
        """Convert entry to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'CelestialObjectEntry':
        """Create entry from dictionary."""
        return cls(RA=data['RA'], DEC=data['DEC'])


class CelestialObjectRepository:
    """Repository for managing celestial object catalog persistence."""
    
    def __init__(self, catalog_path: Optional[str] = None):
        """Initialize repository with catalog file path."""
        if catalog_path is None:
            # Default to assets/OBJECT_CATALOG.json relative to project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            catalog_path = os.path.join(project_root, "assets", "OBJECT_CATALOG.json")

        self.catalog_path = catalog_path
        self._catalog: Dict[str, CelestialObjectEntry] = {}
        self.load()

    # ==================== Persistence ====================

    def load(self) -> bool:
        """
        Load catalog from JSON file.
        Creates empty catalog if file doesn't exist.
        """
        try:
            if not os.path.exists(self.catalog_path):
                self._catalog = {}
                # Create directory if needed
                os.makedirs(os.path.dirname(self.catalog_path), exist_ok=True)
                self.save()
                return True
        
            with open(self.catalog_path, 'r') as f:
                data = json.load(f)
                self._catalog = {
                    name: CelestialObjectEntry.from_dict(coords)
                    for name, coords in data.items()
                }
            return True
        except Exception as e:
            print(f"Error loading catalog: {e}")
            self._catalog = {}
            return False
        
    def save(self) -> bool:
        """Save catalog to JSON file with pretty formatting."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.catalog_path), exist_ok=True)
            
            data = {
                name: entry.to_dict()
                for name, entry in self._catalog.items()
            }
            with open(self.catalog_path, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)
            return True
        except Exception as e:
            print(f"Error saving catalog: {e}")
            return False
    
    # ==================== CRUD Operations ====================
    
    def add(self, object_name: str, ra: str, dec: str) -> bool:
        """Add or update an object in the catalog (in-memory only)."""
        try:
            self._catalog[object_name] = CelestialObjectEntry(RA=ra, DEC=dec)
            return True
        except Exception as e:
            print(f"Error adding object: {e}")
            return False
    
    def delete(self, object_name: str) -> bool:
        """Delete an object from the catalog (in-memory only)."""
        if object_name not in self._catalog:
            return False
        
        try:
            del self._catalog[object_name]
            return True
        except Exception as e:
            print(f"Error deleting object: {e}")
            return False
    
    def get(self, object_name: str) -> Optional[CelestialObjectEntry]:
        """Get an object's entry from the catalog."""
        return self._catalog.get(object_name)
    
    def exists(self, object_name: str) -> bool:
        """Check if an object exists in the catalog."""
        return object_name in self._catalog
    
    def get_all(self) -> Dict[str, CelestialObjectEntry]:
        """Get all objects in the catalog."""
        return self._catalog.copy()
    
    def get_names(self) -> List[str]:
        """Get all object names in the catalog."""
        return list(self._catalog.keys())
    
    def clear(self) -> bool:
        """Clear all entries from the catalog (in-memory only)."""
        self._catalog = {}
        return True
    
    # ==================== Magic Methods ====================
    
    def __len__(self) -> int:
        """Return number of objects in catalog."""
        return len(self._catalog)
    
    def __contains__(self, object_name: str) -> bool:
        """Check if object exists using 'in' operator."""
        return object_name in self._catalog
    
    def __getitem__(self, object_name: str) -> CelestialObjectEntry:
        """Get object using bracket notation."""
        return self._catalog[object_name]
    
    def __repr__(self) -> str:
        """String representation of repository."""
        return f"CelestialObjectRepository(objects={len(self._catalog)}, path='{self.catalog_path}')"