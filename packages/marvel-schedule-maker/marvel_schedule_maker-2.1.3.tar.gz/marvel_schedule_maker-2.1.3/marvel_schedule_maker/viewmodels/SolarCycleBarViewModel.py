import random
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices

class SolarCycleBarViewModel(QObject):
    """ViewModel for SolarCycleBar - handles all business logic and data."""
    
    data_changed = pyqtSignal()
    
    def __init__(self, services: ApplicationServices, parent=None):
        super().__init__(parent)
        self._services = services
        
        # Cached twilight times
        self._civil_start: datetime | None = None
        self._civil_end: datetime | None = None
        self._astro_start: datetime | None = None
        self._astro_end: datetime | None = None
        
        # Star positions (x_factor, y_factor, radius)
        self._star_positions: list[tuple[float, float, float]] = self._generate_star_positions()
        
        # Connect to service signals
        self._services.signals.observation_date_changed.connect(self._on_date_changed)
        
        self._on_date_changed()

    # Properties for read-only access
    @property
    def civil_start(self) -> datetime | None:
        return self._civil_start
    
    @property
    def civil_end(self) -> datetime | None:
        return self._civil_end
    
    @property
    def astro_start(self) -> datetime | None:
        return self._astro_start
    
    @property
    def astro_end(self) -> datetime | None:
        return self._astro_end
    
    @property
    def star_positions(self) -> list[tuple[float, float, float]]:
        return self._star_positions
    
    def _on_date_changed(self):
        """Update all cached data when observation date changes."""
        self._civil_start = self._services.dates.civil_twilight_start
        self._civil_end = self._services.dates.civil_twilight_end
        self._astro_start = self._services.dates.astronomical_twilight_start
        self._astro_end = self._services.dates.astronomical_twilight_end

        self.data_changed.emit()
    
    def _calculate_ratio(self, value: datetime, start: datetime, end: datetime) -> float:
        """Calculate ratio of elapsed time between start and end."""
        if start >= end:
            raise ValueError("Start must be earlier than end.")
        
        total = (end - start).total_seconds()
        elapsed = (value - start).total_seconds()
        
        ratio = max(0.0, min(1.0, elapsed / total))
        return ratio
    
    def _generate_star_positions(self) -> list[tuple[float, float, float]]:
        """Generate random star positions within the night zone."""
        num_stars = 25
        star_positions = []
        for _ in range(num_stars):
            x_factor = random.uniform(0.2, 0.8)
            y_factor = random.uniform(0.0, 1.0)
            radius = random.uniform(2, 6)
            star_positions.append((x_factor, y_factor, radius))
        return star_positions