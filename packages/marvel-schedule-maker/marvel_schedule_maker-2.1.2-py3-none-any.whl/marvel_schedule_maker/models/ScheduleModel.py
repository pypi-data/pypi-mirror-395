from typing import Optional
import uuid
from PyQt6.QtCore import QObject, pyqtSignal


class ScheduleModel(QObject):
    """Schedule data manager - handles CRUD operations on schedule entries."""
    
    data_changed = pyqtSignal()  # Emitted when schedule data changes
    entry_added = pyqtSignal(str)  # Emitted when new entry added (entry_id)
    
    def __init__(self):
        super().__init__()
        self._entries: list[dict] = []

    # ==================== Data Access ====================

    def get_entries(self) -> list[dict]:
        """Get all schedule entries."""
        return self._entries

    def get_entries_without_id(self) -> list[dict]:
        return [{x:y for x,y in x.items() if x != 'id'} for x in self._entries]

    def get_entry_count(self) -> int:
        """Get number of entries in schedule."""
        return len(self._entries)

    # ==================== ID-Based Lookups ====================
    
    def get_row_by_id(self, entry_id: Optional[str]) -> Optional[int]:
        """Find row index by entry ID."""
        if entry_id is None:
            return None
        for i, entry_data in enumerate(self._entries):
            if entry_data.get('id') == entry_id:
                return i
        return None
    
    def get_data_entry_by_id(self, entry_id: Optional[str]) -> Optional[dict]:
        """Find data entry by ID."""
        if entry_id is None:
            return None
        row = self.get_row_by_id(entry_id)
        if row is not None:
            return self._entries[row]
        return None
    
    # ==================== CRUD Operations ====================
    
    def add_entry(self, new_data: dict) -> None:
        """Add a new entry to the schedule."""
        # Generate ID if not present
        if 'id' not in new_data:
            new_data['id'] = str(uuid.uuid4())
        self._entries.append(new_data)
        self.data_changed.emit()
        self.entry_added.emit(new_data['id'])
    
    def update_entry(self, entry_id: Optional[str], updated_data: dict) -> None:
        """Update an existing entry."""
        row = self.get_row_by_id(entry_id)
        if row is not None:
            # Preserve the ID
            updated_data['id'] = self._entries[row]['id']
            self._entries[row] = updated_data
            self.data_changed.emit()
    
    def delete_entry(self, entry_id: str) -> None:
        """Delete an entry by ID."""
        row = self.get_row_by_id(entry_id)
        if row is not None:
            del self._entries[row]
            self.data_changed.emit()
    
    def insert_entry_above(self, entry_id: str, new_data: dict) -> None:
        """Insert a new entry above the specified entry."""
        row = self.get_row_by_id(entry_id)
        if row is not None:
            # Remove id if present to generate new one
            new_data = {k: v for k, v in new_data.items() if k != 'id'}
            new_data['id'] = str(uuid.uuid4())
            self._entries.insert(row, new_data)
            self.data_changed.emit()
            self.entry_added.emit(new_data['id'])
    
    def insert_entry_below(self, entry_id: str, new_data: dict) -> None:
        """Insert a new entry below the specified entry."""
        row = self.get_row_by_id(entry_id)
        if row is not None:
            # Remove id if present to generate new one
            new_data = {k: v for k, v in new_data.items() if k != 'id'}
            new_data['id'] = str(uuid.uuid4())
            self._entries.insert(row + 1, new_data)
            self.data_changed.emit()
            self.entry_added.emit(new_data['id'])
    
    def move_entry_to(self, entry_id: str, new_index: int) -> None:
        """Move an entry to a new position."""
        row = self.get_row_by_id(entry_id)
        if row is not None and 0 <= new_index < len(self._entries):
            entry_data = self._entries.pop(row)
            self._entries.insert(new_index, entry_data)
            self.data_changed.emit()
    
    def move_entry_up(self, entry_id: str) -> None:
        """Move an entry up one position."""
        row = self.get_row_by_id(entry_id)
        if row is not None and row > 0:
            entry_data = self._entries.pop(row)
            self._entries.insert(row - 1, entry_data)
            self.data_changed.emit()
    
    def move_entry_down(self, entry_id: str) -> None:
        """Move an entry down one position."""
        row = self.get_row_by_id(entry_id)
        if row is not None and row < len(self._entries) - 1:
            entry_data = self._entries.pop(row)
            self._entries.insert(row + 1, entry_data)
            self.data_changed.emit()
    
    def clear(self) -> None:
        """Clear all entries."""
        self._entries.clear()
        self.data_changed.emit()
    
    def set_entries(self, entries: list[dict]) -> None:
        """Replace all entries with new list (without emitting signals during load)."""
        self._entries = entries.copy()
        self.data_changed.emit()
    
    def create_default_data(self, telescope: int) -> dict:
        """Create a default action data dictionary."""
        return {
            'id': str(uuid.uuid4()),
            'telescope': telescope
        }
