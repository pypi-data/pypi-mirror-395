import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from marvel_schedule_maker.models.TaskRectUIConfig import TaskRectUIConfig
from marvel_schedule_maker.models.Timeline import TimelineEntry
from marvel_schedule_maker.models.TimelinePanelUIConfig import TimelinePanelUIConfig
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


@dataclass
class TaskDisplayData:
    """Pre-calculated display data for a single task rectangle."""
    entry_id: str
    entry: TimelineEntry
    x: float
    y: float
    width: float
    height: float
    is_copied: bool
    is_editing: bool
    telescope_idx: int


class TimelinePanelViewModel(QObject):
    """ViewModel for TimelinePanel - handles all calculations and business logic."""
    
    # Signals
    display_data_changed = pyqtSignal()
    zoom_changed = pyqtSignal(float)  # pixels_per_second
    scroll_to_entry_requested = pyqtSignal(str)  # entry_id
    
    def __init__(self, services: ApplicationServices):
        super().__init__()
        
        self._services = services
        self._ui_config = TimelinePanelUIConfig()
        self._task_ui_config = TaskRectUIConfig()
        
        # Display state
        self._pixels_per_second: float = self._ui_config.default_zoom
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._task_display_data: List[TaskDisplayData] = []
        self._scroll_ratio: float = 0.0
        self._scene_width: float = 0
        self._scene_height: float = 0
        self._viewport_width: int = 1000  # Default, updated by view
        
        # Connect to ApplicationServices signals
        self._services.signals.timeline_updated.connect(self._on_timeline_updated)
        self._services.signals.observation_date_changed.connect(self._on_observation_date_changed)
        self._services.signals.clipboard_updated.connect(self._on_clipboard_changed)
        self._services.signals.editing_state_changed.connect(self._on_editing_changed)
        
        # Initial calculation
        self._recalculate_display_data()
    
    # ==================== Public Query Methods ====================
    
    def get_time_range(self) -> tuple[Optional[datetime], Optional[datetime]]:
        """Get start and end time for timeline display."""
        return (self._start_time, self._end_time)
    
    def get_task_display_data(self) -> List[TaskDisplayData]:
        """Get all pre-calculated task display data."""
        return self._task_display_data
    
    def get_pixels_per_second(self) -> float:
        """Get current zoom level (pixels per second)."""
        return self._pixels_per_second
    
    def get_scene_dimensions(self) -> tuple[float, float]:
        """Get scene width and height."""
        return (self._scene_width, self._scene_height)
    
    def get_scroll_ratio(self) -> float:
        """Get scroll position ratio for restoration after refresh."""
        return self._scroll_ratio
    
    def get_ui_config(self) -> TimelinePanelUIConfig:
        """Get UI configuration."""
        return self._ui_config
    
    def get_task_ui_config(self) -> TaskRectUIConfig:
        """Get task rectangle UI configuration."""
        return self._task_ui_config
    
    def get_column_width(self) -> float:
        """Calculate column width based on viewport."""
        available_width = max(self._viewport_width, self._ui_config.min_scene_width)
        total_spacing = self._ui_config.column_spacing * (self._ui_config.column_count - 1)
        column_width = (available_width - total_spacing) / self._ui_config.column_count
        return column_width
    
    # ==================== Public Action Methods ====================
    
    def set_zoom(self, pixels_per_second: float):
        """Set zoom level and recalculate display."""
        self._pixels_per_second = pixels_per_second
        self._recalculate_display_data()
        self.zoom_changed.emit(pixels_per_second)
        self.display_data_changed.emit()
    
    def set_scroll_ratio(self, ratio: float):
        """Store scroll position ratio for restoration."""
        self._scroll_ratio = ratio
    
    def set_viewport_width(self, width: int):
        """Update viewport width and recalculate if needed."""
        if self._viewport_width != width:
            self._viewport_width = width
            self._recalculate_display_data()
            self.display_data_changed.emit()
    
    def request_scroll_to_entry(self, entry_id: str):
        """Request view to scroll to specific entry."""
        self.scroll_to_entry_requested.emit(entry_id)
    
    # ==================== Context Menu Action Handlers ====================
    
    def handle_edit(self, entry_id: str, action_type: str):
        """Handle edit request for entry."""
        self._services.set_editing_entry(entry_id)
        self._services.set_action_type(action_type)
    
    def handle_copy(self, entry_id: str):
        """Handle copy request for entry."""
        entry_data = self._services.schedule.get_data_entry_by_id(entry_id)
        if entry_data:
            self._services.set_clipboard(entry_data)
            entry_type = entry_data.get('type', 'Unknown')
            self._services.show_success(f"Copied {entry_type} entry")
    
    def handle_delete(self, entry_id: str):
        """Handle delete request for entry."""
        entry_data = self._services.schedule.get_data_entry_by_id(entry_id)
        if entry_data:
            entry_type = entry_data.get('type', 'Unknown')
            self._services.schedule.delete_entry(entry_id)
            self._services.show_success(f"Deleted {entry_type} entry")
    
    def handle_insert_above(self, entry_id: str):
        """Handle insert above request."""
        timeline_entry = self._services.get_timeline_entry_by_id(entry_id)
        if timeline_entry:
            new_data = self._services.schedule.create_default_data(timeline_entry.telescope)
            self._services.schedule.insert_entry_above(entry_id, new_data)
            self._services.show_success("Inserted blank entry above")
    
    def handle_insert_below(self, entry_id: str):
        """Handle insert below request."""
        timeline_entry = self._services.get_timeline_entry_by_id(entry_id)
        if timeline_entry:
            new_data = self._services.schedule.create_default_data(timeline_entry.telescope)
            self._services.schedule.insert_entry_below(entry_id, new_data)
            self._services.show_success("Inserted blank entry below")
    
    def handle_insert_copied_above(self, entry_id: str):
        """Handle insert copied above request."""
        copied_data = self._services.get_clipboard()
        if copied_data:
            self._services.schedule.insert_entry_above(entry_id, copied_data)
            self._services.clear_clipboard()
            self._services.show_success(f"Pasted {copied_data.get('type')} entry above")
    
    def handle_insert_copied_below(self, entry_id: str):
        """Handle insert copied below request."""
        copied_data = self._services.get_clipboard()
        if copied_data:
            self._services.schedule.insert_entry_below(entry_id, copied_data)
            self._services.clear_clipboard()
            self._services.show_success(f"Pasted {copied_data.get('type')} entry below")
    
    def has_clipboard(self) -> bool:
        """Check if clipboard has data."""
        return self._services.has_clipboard()
    
    # ==================== Private Signal Handlers ====================
    
    def _on_timeline_updated(self):
        """Handle timeline update from ApplicationServices."""
        self._recalculate_display_data()
        self.display_data_changed.emit()
    
    def _on_observation_date_changed(self):
        """Handle observation date change from ApplicationServices."""
        self._recalculate_display_data()
        self.display_data_changed.emit()
    
    def _on_clipboard_changed(self):
        """Handle clipboard change - need to update copied state."""
        self._recalculate_display_data()
        self.display_data_changed.emit()
    
    def _on_editing_changed(self):
        """Handle editing state change - need to update editing state."""
        self._recalculate_display_data()
        self.display_data_changed.emit()
    
    # ==================== Private Calculation Methods ====================
    
    def _recalculate_display_data(self):
        """Master calculation method - recalculates everything."""
        self._calculate_time_range()
        self._calculate_scene_dimensions()
        self._calculate_task_positions()
    
    def _calculate_time_range(self):
        """Calculate start and end time based on twilight times and timeline entries."""
        dates = self._services.dates
        timeline = self._services.get_timeline()
        
        # Start with twilight times plus padding
        start_raw = dates.civil_twilight_start - timedelta(hours=self._ui_config.time_padding_hours)
        start_time = start_raw.replace(minute=0, second=0, microsecond=0)
        
        end_raw = dates.civil_twilight_end + timedelta(hours=self._ui_config.time_padding_hours)
        end_time = end_raw.replace(minute=0, second=0, microsecond=0)
        
        # Extend time range if tasks go beyond twilight times
        for entry in timeline:
            if entry.start_time < start_time:
                # Don't extend for WAIT_TIMESTAMP actions
                if entry.action_data.get('type') != 'WAIT_TIMESTAMP':
                    start_time = entry.start_time
            
            if entry.end_time > end_time:
                end_time = entry.end_time
        
        self._start_time = start_time
        self._end_time = end_time
    
    def _calculate_scene_dimensions(self):
        """Calculate scene width and height based on time range and zoom."""
        if not self._start_time or not self._end_time:
            self._scene_width = 0
            self._scene_height = 0
            return
        
        # Height based on time duration and zoom
        total_seconds = (self._end_time - self._start_time).total_seconds()
        self._scene_height = total_seconds * self._pixels_per_second
        
        # Width based on columns
        column_width = self.get_column_width()
        self._scene_width = (
            self._ui_config.column_count * column_width + 
            (self._ui_config.column_count - 1) * self._ui_config.column_spacing
        )
    
    def _calculate_task_positions(self):
        """Calculate x, y, width, height for all task rectangles."""
        timeline = self._services.get_timeline()
        copied_entry_id = self._get_copied_entry_id()
        editing_entry_id = self._services.get_editing_entry_id()
        
        self._task_display_data = []
        
        for entry in timeline:
            # Handle telescope 0 (all telescopes) - create task for telescopes 1-4
            if entry.telescope == 0:
                for telescope_idx in range(1, 5):
                    # Create a copy of the entry with the specific telescope
                    copied_entry = copy.deepcopy(entry)
                    copied_entry.telescope = telescope_idx
                    
                    display_data = self._create_task_display_data(
                        copied_entry,
                        telescope_idx,
                        copied_entry_id,
                        editing_entry_id
                    )
                    self._task_display_data.append(display_data)
            else:
                display_data = self._create_task_display_data(
                    entry,
                    entry.telescope,
                    copied_entry_id,
                    editing_entry_id
                )
                self._task_display_data.append(display_data)
    
    def _create_task_display_data(
        self,
        entry: TimelineEntry,
        telescope_idx: int,
        copied_entry_id: Optional[str],
        editing_entry_id: Optional[str]
    ) -> TaskDisplayData:
        """Create display data for a single task."""
        x = self._telescope_to_x(telescope_idx)
        y = self._time_to_y(entry.start_time)
        width = self.get_column_width() - 2
        
        duration_seconds = (entry.end_time - entry.start_time).total_seconds()
        height = duration_seconds * self._pixels_per_second
        
        return TaskDisplayData(
            entry_id=entry.id,
            entry=entry,
            x=x,
            y=y,
            width=width,
            height=height,
            is_copied=(entry.id == copied_entry_id),
            is_editing=(entry.id == editing_entry_id),
            telescope_idx=telescope_idx
        )
    
    def _time_to_y(self, dt: datetime) -> float:
        """Convert datetime to Y coordinate."""
        if not self._start_time:
            return 0
        delta_seconds = (dt - self._start_time).total_seconds()
        return delta_seconds * self._pixels_per_second
    
    def _telescope_to_x(self, telescope_idx: int) -> float:
        """Convert telescope index to X coordinate."""
        column_width = self.get_column_width()
        return (telescope_idx - 1) * (column_width + self._ui_config.column_spacing)
    
    def _get_copied_entry_id(self) -> Optional[str]:
        """Get the copied entry ID if clipboard has data."""
        # For now, we don't track the source entry ID in clipboard
        # This could be enhanced in ApplicationServices if needed
        return None
