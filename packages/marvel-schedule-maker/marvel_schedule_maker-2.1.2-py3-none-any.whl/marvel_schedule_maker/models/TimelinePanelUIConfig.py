from dataclasses import dataclass
from typing import Tuple


@dataclass
class TimelinePanelUIConfig:
    """UI configuration for TimelinePanel display constants."""
    
    # Column layout
    column_count: int = 5
    column_spacing: int = 10
    telescope_names: Tuple[str, ...] = (
        "Telescope 1", 
        "Telescope 2", 
        "Telescope 3", 
        "Telescope 4", 
        "Sun Telescope"
    )
    
    # Zoom settings (pixels per second)
    min_zoom: float = 0.02  # slider value 2
    max_zoom: float = 1.50  # slider value 150
    default_zoom: float = 0.02
    zoom_slider_min: int = 2
    zoom_slider_max: int = 150
    zoom_slider_default: int = 2
    zoom_step: int = 5
    
    # Time ruler
    ruler_width: int = 80
    ruler_interval_minutes: int = 30
    ruler_background_color: str = "#f8f9fa"
    ruler_border_color: str = "#dee2e6"
    
    # Header
    header_height: int = 40
    header_background_color: str = "#f8f9fa"
    header_border_color: str = "#dee2e6"
    
    # Control bar
    control_bar_height: int = 50
    
    # Time padding
    time_padding_hours: int = 1
    
    # Minimum scene dimensions
    min_scene_width: int = 1000
