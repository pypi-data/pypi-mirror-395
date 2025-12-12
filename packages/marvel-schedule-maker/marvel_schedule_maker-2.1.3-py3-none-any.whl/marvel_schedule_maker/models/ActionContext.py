from dataclasses import dataclass, field
from datetime import date
from typing import Any, Callable, Dict, List, Optional

@dataclass
class ActionContext:
    """Shared state container for form fields during action creation/editing."""
    observation_date: date
    _values: Dict[str, Any] = field(default_factory=dict)
    _full_values: Dict[str, Any] = field(default_factory=dict)
    _observers: Dict[str, List[Callable]] = field(default_factory=dict)

    # ==================== Value Access ====================

    def get(self, name: str, default: Any = None):
        """Get raw value for a field. Used by all tiers for reading."""
        return self._values.get(name, default)

    def get_full(self, name: str, default: Any = None):
        """Get full/formatted value for a field. Used for final data collection."""
        return self._full_values.get(name, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all raw values. Used by observers and dependent fields."""
        return self._values.copy()
    
    def get_all_full(self) -> Dict[str, Any]:
        """Get all formatted values. Used by ViewModel for insert/save."""
        return self._full_values.copy()

    # ==================== Value Mutation ====================
    
    def set(self, name: str, value: Any, full_value: Any = None, notify: bool = True):
        """Set value for a field and notify observers."""
        old_value = self._values.get(name)

        self._values[name] = value
        self._full_values[name] = full_value if full_value is not None else value

        # Only notify on raw value changes
        if notify and old_value != value:
            self._notify_observers(name, value)

    # ==================== Observer Management ====================

    def watch(self, field_name: str, callback: Callable[[str, Any], None]):
        """Register a callback to watch a field for changes."""
        self._observers.setdefault(field_name, []).append(callback)

    def _notify_observers(self, name: str, value: Any):
        """Notify all callbacks watching this field."""
        if name not in self._observers:
            return
        
        for callback in self._observers.get(name, []):
            try:
                callback(name, value)
            except Exception as e:
                print(f"Observer callback failed for field '{name}': {e}")

    # ==================== Convenience Properties ====================

    @property
    def telescope(self) -> Optional[int]:
        """Convenience property for telescope field."""
        return self.get("telescope")
    
    @telescope.setter
    def telescope(self, value: Optional[int]):
        """Convenience setter for telescope field."""
        self.set("telescope", value, value)



