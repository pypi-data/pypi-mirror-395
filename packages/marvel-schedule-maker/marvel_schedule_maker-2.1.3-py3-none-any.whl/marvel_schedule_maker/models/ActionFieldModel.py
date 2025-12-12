from abc import abstractmethod, ABC
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import re
import os
from PyQt6.QtWidgets import QLineEdit, QCheckBox, QWidget, QRadioButton, QHBoxLayout, QButtonGroup, QComboBox, QPushButton
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QIcon
from PyQt6.QtCore import QTimer, QSize
from typing import Any, Dict, List, Optional
import qtawesome as qta

from marvel_schedule_maker.models.ActionContext import ActionContext
from marvel_schedule_maker.utils.TelescopeConfig import TELESCOPESCONFIG, find_config_value


class BaseModel:
    dependencies: List[str] = [] # names of context fields this value depends on

    def __init__(self, name: str, context: ActionContext, initial_value: Any):
        self.name = name
        self.context = context
        self._dependencies = list(self.dependencies)

        # Register dependencies with context
        for dep in self._dependencies:
            self.context.watch(dep, self._on_dependency_changed)

        self.context.watch(self.name, self._on_own_value_changed)

        # register with context
        full_value = None
        if self.validate(initial_value):
            full_value = self.format_full(initial_value)
        self.context.set(self.name, initial_value, full_value, notify=False)

    def _on_own_value_changed(self, name: str, value: Any) -> None:
        """
        Called when this fields value changes in context.
        Override in subclasses to update widgets then context value change.
        """
        pass

    @property
    def value(self) -> Any:
        return self.context.get(self.name)

    @value.setter
    def value(self, new_value: Any) -> None:
        if self.validate(new_value):
            full_value = self.format_full(new_value)
        else:
            full_value = self.context.get_full(self.name)
        self.context.set(self.name, new_value, full_value)

    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Override in subclasses if needed."""
        ...

    @abstractmethod
    def input_widget(self) -> QWidget:
        """Create and return the input widget for this value."""
        ...

    @abstractmethod
    def validate(self, value: Any = None) -> bool:
        """Check if the given value is valid."""
        ...

    def format_full(self, value: Any = None) -> Any:
        """
        Return the value formatted for the scheduler.
        Example: meant to save a time as full datetime using the date from context
        """
        return value if value is not None else self.value

    @abstractmethod
    def expected_format(self) -> str:
        """Return a string describing the expected input format."""
        ...

class BaseCoordinate(BaseModel, ABC):
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    degree_pattern = r'^([+-]?\d{1,3})(?:[:\s]\s*([0-5]?\d)(?:[:\s]\s*([0-5]?\d(?:\.\d+)?))?)?$'

    def input_widget(self) -> QWidget:
        """Create input widget for coordinate."""
        widget = QLineEdit()
        widget.setPlaceholderText(self.expected_format())
        
        if self.value is not None:
            widget.setText(str(self.value))

        def handle_change(text: str):
            parsed_text = text.replace(" ", ":")
            self.value = parsed_text

        widget.textChanged.connect(handle_change)
        self._widget = widget
        return widget
    
    def _on_own_value_changed(self, name: str, value: Any) -> None:
        """Update widget when context value changes."""
        if isinstance(self._widget, QLineEdit) and value is not None:
            self._widget.setText(str(value))

    def validate(self, value: Any = None) -> bool:
        """Check if the value is a valid coordinate."""
        check_value = value if value is not None else self.value
        try:
            value = str(check_value)
            return self._parse(value) is not None
        except:
            return False
        
    @classmethod
    def parse(cls, value: Any) -> Optional[float]:
        try:
            value = str(value).strip()
            min = cls.min_value
            max = cls.max_value
        except:
            return None
        return cls._parse_float(value, min, max) if cls._parse_float(value, min, max) else None or cls._parse_coord_string(value, min, max) if cls._parse_coord_string(value, min, max) else None

    
    def _parse(self, value: Any = None) -> Optional[float]:
        """Attempt both float and string parsing."""
        try:
            value = str(value).strip()
            min = self.min_value
            max = self.max_value
        except:
            return None
        return self._parse_float(value, min, max) if self._parse_float(value, min, max) else None or self._parse_coord_string(value, min, max) if self._parse_coord_string(value, min, max) else None
    
    @classmethod
    def _parse_float(cls, value: str, min: Optional[float], max: Optional[float]) -> Optional[float]:
        try:
            val_float = float(value)
        except:
            return None
        return val_float if cls.min_max_check(val_float, min, max) else None

    @classmethod
    def _parse_coord_string(cls, coord_str: str, min: Optional[float], max: Optional[float]) -> Optional[float]:
        hours = cls._calculate_hours(coord_str)
        if hours is None:
            return None
        return hours if cls.min_max_check(hours, min, max) else None

    @classmethod
    def _calculate_hours(cls, degrees: str) -> Optional[float]:
        match = re.fullmatch(cls.degree_pattern, degrees)
        if match:
            a, b, c = map(float, (match.group(1), match.group(2) or 0, match.group(3) or 0))
            return a + b/60 + c/3600
        return None

    @classmethod
    def min_max_check(cls, value: float, min: Optional[float], max: Optional[float]) -> bool:
        if min is not None and value < min:
            return False
        if max is not None and value > max:
            return False
        return True

    def expected_format(self) -> str:
        """Return expected input description for coordinate."""
        return "18.072497 | 18:04:20.99"

class Ra(BaseCoordinate):
    """Right Ascension coordinate (0-24 hours)."""
    min_value = 0.0
    max_value = 24.0

class Dec(BaseCoordinate):
    """Declination coordinate (-90 to +90 degrees)."""
    min_value = -90.0
    max_value = 90.0

class Azimuth(BaseCoordinate):
    """Azimuth coordinate (0-360 degrees)."""
    min_value = 0.0
    max_value = 360.0

class Altitude(BaseCoordinate):
    """Altitude coordinate (-90 to +90 degrees)."""
    min_value = -90.0
    max_value = 90.0
    dependencies = ['telescope'] # depends on selected telescope

    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Update min/max based on telescope."""
        if name == 'telescope':
            self._update_limits(value)

    def _update_limits(self, telescope: Optional[int]) -> None:
        """Update min/max based on selected telescope."""
        if telescope is None or telescope == 0:
            self.min_value = -90.0
            self.max_value = 90.0
        else:
            self.min_value = TELESCOPESCONFIG[telescope].TELESCOPE.MIN_ALTITUDE
            self.max_value = TELESCOPESCONFIG[telescope].TELESCOPE.MAX_ALTITUDE

        if isinstance(self._widget, QLineEdit):
            self._widget.setPlaceholderText(self.expected_format())

    def expected_format(self) -> str:
        return f"{self.min_value} ≤ altitude ≤ {self.max_value}"

class Int(BaseModel):
    """Integer value with optional min/max bounds."""
    default: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    dependencies = ['telescope'] # some of these depend on selected telescope


    def input_widget(self) -> QWidget:
        """Create input widget for integer."""
        widget = QLineEdit()
        widget.setPlaceholderText(self.expected_format())

        if self.value is not None:
            widget.setText(str(self.value))
        elif self.default is not None:
            self.value = self.default
            widget.setText(str(self.default))

        validator = QIntValidator()
        if self.min_value is not None:
            validator.setBottom(self.min_value)
        if self.max_value is not None:
            validator.setTop(self.max_value)
        widget.setValidator(validator)

        def handle_change(text: str):
            valid = self.validate(text) if text else False
            self.value = int(text) if valid else text

        widget.textChanged.connect(handle_change)
        self._widget = widget
        return widget
    
    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Update based on telescope."""
        if name == 'telescope':
            self._update_widget_state(value)

    def _update_widget_state(self, telescope: Optional[int]) -> None:
        """Update widget state based on selected telescope."""
        if telescope is None or telescope == 0:
            return
        config_value = find_config_value(TELESCOPESCONFIG[telescope], self.name)
        if config_value is None or not self.validate(config_value):
            return
        # Update value and UI
        self.value = config_value
        if isinstance(self._widget, QLineEdit):
            self._widget.setPlaceholderText(f"{self.expected_format()} (default: {config_value})")
            self._widget.setText(str(config_value))

    def validate(self, value: Any = None) -> bool:
        """Check if the value is a valid integer within bounds."""
        check_value = value if value is not None else self.value

        try:
        
            int_value = int(check_value)

            if self.min_value is not None and int_value < self.min_value:
                return False
            
            if self.max_value is not None and int_value > self.max_value:
                return False
            
            return True
        
        except:
            return False

    def expected_format(self) -> str:
        """Return expected input description with bounds"""
        if self.min_value is not None and self.max_value is not None:
            return f"{self.min_value} <= int <= {self.max_value}"
        
        elif self.min_value is not None:
            return f"int >= {self.min_value}"
        
        elif self.max_value is not None:
            return f"int <= {self.max_value}"
        
        else:
            return "integer"

class TemperatureSet(Int):
    default = -20

class TemperatureStep(Int):
    default = 2

class TemperatureDelay(Int):
    default = 60

class TemperatureAmbient(Int):
    default = 20

class IntPositive(Int):
    """Positive integer (min 1)"""
    min_value = 1

class FlatMedian(Int):
    """Flat median value between 1 and 90. that updates context on change."""
    min_value = 1
    max_value = 90

class FlatRange(Int):
    min_value = 1
    max_value = 90
    dependencies = ['flat_median'] # depends on flat_median

    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Update max based on flat_median."""
        if name == 'flat_median':
            self._update_limits(value)

    def _update_limits(self, flat_median: Optional[int]) -> None:
        """Update max based on flat_median."""
        if flat_median in (None, ''):
            self.max_value = 90 # back to default
            return

        assert self.min_value is not None

        # flat_median - flat_range mag niet onder nul
        # flat median + flat range mag niet boven 100
        self.max_value = min(flat_median, 100 - flat_median)

        if isinstance(self._widget, QLineEdit):
            self._widget.setValidator(QIntValidator(self.min_value, self.max_value))
            self._widget.setPlaceholderText(self.expected_format())

class Choice(BaseModel, ABC):
    """Abstract class for choices. Do not instantiate directly. You will get a TypeError."""
    _allowed_values: List[Any] = []
    dependencies = ['telescope'] # some of these depend on selected telescope

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if type(self) is Choice:
            raise TypeError("Choice is an abstract class and cannot be instantiated directly.")
        if not self._allowed_values:
            raise ValueError("Subclasses of Choice must define _allowed_values.")
        self._button_group: Optional[QButtonGroup] = None

    def input_widget(self) -> QWidget:
        """Create a horizontal group of radio buttons for the allowed choices."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self._button_group = QButtonGroup(container)
        self._button_group.setExclusive(True)

        for idx, choice_value in enumerate(self._allowed_values):
            radio_btn = QRadioButton(str(choice_value))
            layout.addWidget(radio_btn)
            self._button_group.addButton(radio_btn, idx)

            # Check if this should be the selected button
            if self.value == choice_value:
                radio_btn.setChecked(True)

        def handle_selection(button_id: int):
            self.value = self._allowed_values[button_id]

        self._button_group.idClicked.connect(handle_selection)
        self._widget = container
        return container

    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Update based on telescope."""
        if name == 'telescope':
            self._update_widget_state(value)

    def _update_widget_state(self, telescope: Optional[int]) -> None:
        """Update widget state based on selected telescope."""
        if telescope is None or telescope == 0:
            return
        config_value = find_config_value(TELESCOPESCONFIG[telescope], self.name)
        if config_value is None or not self.validate(config_value):
            return
        # Update value and UI
        self.value = config_value
        if self._button_group is not None:
            idx = self._allowed_values.index(config_value)
            button = self._button_group.button(idx)
            if button is not None:
                button.setChecked(True)
    
    def validate(self, value: Any = None) -> bool:
        check_value = value if value is not None else self.value
        return check_value in self._allowed_values
        
    def expected_format(self) -> str:
        return f"One of: {', '.join(map(str, self._allowed_values))}"

class Bool(Choice):
    _allowed_values = [True, False]

    def __init__(self, *args, **kwargs) -> None:
        # Bool is a bit special, since it cant be None but solely False or True
        # We turn the value into False from the start if it is None
        if kwargs['initial_value'] is None:
            kwargs['initial_value'] = False
        super().__init__(*args, **kwargs)

    def input_widget(self) -> QWidget:
        """Create a checkbox for boolean input."""
        widget = QCheckBox()

        widget.setChecked(bool(self.value))

        def handle_toggle(checked: bool):
            self.value = checked

        widget.toggled.connect(handle_toggle)
        self._widget = widget
        return widget
    
    def expected_format(self) -> str:
        """Return expected input description for boolean."""
        return "True or False"

class Binning(Choice):
    """Binning options for the camera."""
    _allowed_values = [1, 2, 3, 4]

class NasmythPort(Choice):
    """Nasmyth port options."""
    _allowed_values = [1, 2]

class StatusValue(str, Enum):
    """Enumeration for status values."""
    WAITING = "WAITING"
    BUSY = "BUSY"
    DONE = "DONE"
    FAILED = "FAILED"

    def __str__(self):
        return self.value

class Status(Choice):
    """Status options."""
    _allowed_values = [s.value for s in StatusValue]

class Telescope(Choice):
    """Telescope selection."""
    _allowed_values = [1, 2, 3, 4]
    dependencies = []

    def input_widget(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self._button_group = QButtonGroup(container)
        self._button_group.setExclusive(True)

        # Create radio buttons for each telescope
        for telescope_id in self._allowed_values:
            radio_btn = QRadioButton(str(telescope_id))
            layout.addWidget(radio_btn)
            self._button_group.addButton(radio_btn, telescope_id)

            # Check if this should be the selected button
            if self.value == telescope_id:
                radio_btn.setChecked(True)
                
        def handle_selection(telescope_id: int):
            self.value = telescope_id

        self._button_group.idClicked.connect(handle_selection)
        self._widget = container
        return container

class TelescopeWithNone(Telescope):
    """Telescope selection including 'None' option."""
    _allowed_values = [0, 1, 2, 3, 4]

class Float(BaseModel):
    """Floating-point number with optional min/max bounds."""
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    dependencies = ['telescope'] # some of these depend on selected telescope

    def input_widget(self) -> QWidget:
        widget = QLineEdit()
        widget.setPlaceholderText(self.expected_format())

        if self.value is not None:
            widget.setText(str(self.value))
        
        validator = QDoubleValidator()
        if self.min_value is not None:
            validator.setBottom(self.min_value)
        if self.max_value is not None:
            validator.setTop(self.max_value)
        widget.setValidator(validator)

        def handle_change(text: str):
            is_valid = self.validate(text) if text else False
            self.value = float(text) if is_valid else text

        widget.textChanged.connect(handle_change)
        self._widget = widget
        return widget
    
    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when a dependency changes. Update based on telescope."""
        if name == 'telescope':
            self._update_widget_state(value)

    def _update_widget_state(self, telescope: Optional[int]) -> None:
        """Update widget state based on selected telescope."""
        if telescope is None or telescope == 0:
            return
        config_value = find_config_value(TELESCOPESCONFIG[telescope], self.name)
        if config_value is None or not self.validate(config_value):
            return
        # Update value and UI
        self.value = config_value
        if isinstance(self._widget, QLineEdit):
            self._widget.setPlaceholderText(f"{self.expected_format()} (default: {config_value})")
            self._widget.setText(str(config_value))

    def validate(self, value: Any = None) -> bool:
        """Check if the value is a valid float within bounds."""
        check_value = value if value is not None else self.value

        try:
            float_value = float(check_value)
            if self.min_value is not None and float_value < self.min_value:
                return False
            
            if self.max_value is not None and float_value > self.max_value:
                return False
            
            return True
        except:
            return False

    def expected_format(self) -> str:
        if self.min_value is not None and self.max_value is not None:
            return f"{self.min_value} <= float <= {self.max_value}"
        elif self.min_value is not None:
            return f"float >= {self.min_value}"
        elif self.max_value is not None:
            return f"float <= {self.max_value}"
        else:
            return "float"

class FocalLength(Float):
    """Focal length"""
    min_value = 0.0
    max_value = 28.0

class String(BaseModel):
    """String value validator."""
       
    def input_widget(self) -> QWidget:
        widget = QLineEdit()
        widget.setPlaceholderText(self.expected_format())

        if self.value is not None:
            widget.setText(str(self.value))

        def handle_change(text: str):
            self.value = text

        widget.textChanged.connect(handle_change)
        self._widget = widget
        return widget

    def validate(self, value: Any = None) -> bool:
        check_value = value if value is not None else self.value
        try:
            str(check_value)
            return True
        except:
            return False

    def expected_format(self) -> str:
        """Return expected input description"""
        return "string"

class ObjectName(String):
    """String value with object catalog search functionality."""

    ICON_SIZE = QSize(24, 24)

    def input_widget(self) -> QWidget:
        """Create input widget with search button for object lookup."""
        # Create horizontal widget
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Create text input
        text_input = QLineEdit()
        text_input.setPlaceholderText(self.expected_format())
        
        if self.value is not None:
            text_input.setText(str(self.value))
        
        def handle_text_change(text: str):
            stripped_text = text.strip()
            self.value = stripped_text if stripped_text else None
            # Enable/disable search button based on text
            has_valid_text = bool(stripped_text)
            search_button.setEnabled(has_valid_text)
            add_button.setEnabled(has_valid_text)
        
        text_input.textChanged.connect(handle_text_change)
        
        # Create search button magnifying-glass
        search_button = QPushButton()
        search_button.setIcon(qta.icon('fa6s.magnifying-glass'))
        search_button.setIconSize(self.ICON_SIZE)
        search_button.setToolTip("Search object coordinates")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        search_button.setEnabled(bool(self.value))
        search_button.clicked.connect(lambda: self._search_object(search_button))
        
        # Create add button plus
        add_button = QPushButton()
        add_button.setIcon(qta.icon('fa6s.plus'))
        add_button.setIconSize(self.ICON_SIZE)
        add_button.setToolTip("add object coordinates")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        add_button.setEnabled(bool(self.value))
        add_button.clicked.connect(lambda: self._add_object(add_button))

        layout.addWidget(text_input)
        layout.addWidget(search_button)
        layout.addWidget(add_button)
        
        self._widget = widget
        return widget
    
    def _add_object(self, button: QPushButton) -> None:
        """Add object into catalog (if) with the written RA/DEC"""
        # Validate object name
        if not self.value or not self.value.strip():
            self._show_feedback(button, False)
            return

        object_name = self.value.strip()
        ra = self.context.get('RA', None)
        dec = self.context.get('DEC', None)

        if not (ra and dec):
            self._show_feedback(button, False)
            return
        
        catalog = ObjectCatalog()

        if catalog.exists(object_name):
            self._show_feedback(button, False)
            return
        
        success = catalog.add(object_name, ra, dec)
        
        self._show_feedback(button, success)

    def _search_object(self, button: QPushButton) -> None:
        """Search for object in catalog and update RA/DEC in context."""
        if not self.value or not self.value.strip():
            self._show_feedback(button, False)
            return
        
        # Get and normalize object name
        object_name = self.value.strip()
        
        if not object_name:
            self._show_feedback(button, False)
            return
        
        catalog = ObjectCatalog()
        coords = catalog.get(object_name)
        
        if not coords:
            self._show_feedback(button, False)
            return
        
        
        # Check if context has RA and DEC fields
        try:
            # Try to update RA
            if 'RA' not in self.context._values.keys():
                self._show_feedback(button, False)
                return
            
            # Try to update DEC
            if 'DEC' not in self.context._values.keys():
                self._show_feedback(button, False)
                return
            
            # Update both values
            self.context.set('RA', coords.RA)
            self.context.set('DEC', coords.DEC)
            
            # Show success feedback
            self._show_feedback(button, True)

            
        except Exception as e:
            self._show_feedback(button, False)
    
    def _show_feedback(self, button: QPushButton, success: bool) -> None:
        """Show visual feedback on the button."""
        # Store original style
        original_style = button.styleSheet()
        original_icon = button.icon()
        original_iconsize = button.iconSize()
        original_tooltip = button.toolTip()
        
        # Update button appearance
        if success:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)
            icon = qta.icon('fa6s.check')
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)
            icon = qta.icon('fa6s.xmark')
        
        button.setIcon(icon)
        button.setIconSize(self.ICON_SIZE)
        
        # Reset after 500 milliseconds
        QTimer.singleShot(500, lambda: self._reset_button(button, original_style, original_icon, original_iconsize, original_tooltip))
    
    def _reset_button(self, button: QPushButton, original_style: str, original_icon: QIcon, original_iconsize: QSize, original_tooltip: str) -> None:
        """Reset button to original state."""
        button.setStyleSheet(original_style)
        button.setIcon(original_icon)
        button.setIconSize(original_iconsize)
        button.setToolTip(original_tooltip)
    
    def validate(self, value: Any = None) -> bool:
        """Check if the value is a valid non-empty string."""
        check_value = value if value is not None else self.value
        
        # Reject None or empty strings
        if check_value is None:
            return False
        
        try:
            str_value = str(check_value).strip()
            return len(str_value) > 0
        except:
            return False

    def expected_format(self) -> str:
        """Return expected input description."""
        return "(e.g., M31, NGC 253)"

class Timestamp(String):
    """Timestamp validator supporting HH, HH:MM, HH:MM:SS, and full YYYY-MM-DD HH:MM:SS formats."""

    # Time format patterns
    _HOUR_FORMAT = r"^\d{2}$"
    _TIME_FORMAT = r"^\d{2}:\d{2}$"
    _TIME_WITH_SECONDS_FORMAT = r"^\d{2}:\d{2}:\d{2}$"
    _FULL_DATETIME_FORMAT = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    
    # Noon threshold for day rollover
    _NOON_HOUR = 12
    _NOON_TIME = datetime.strptime("12:00", "%H:%M").time()
    _NOON_TIME_WITH_SECONDS = datetime.strptime("12:00:00", "%H:%M:%S").time()

    def validate(self, value: Any = None) -> bool:
        check_value = value if value is not None else self.value

        if check_value is None:
            return False

        try:
            check_value = str(check_value)

            # Check HH format
            if re.match(self._HOUR_FORMAT, check_value):
                hour = int(check_value)
                return 0 <= hour <= 23
            
            # Check HH:MM format
            if re.match(self._TIME_FORMAT, check_value):
                datetime.strptime(check_value, "%H:%M")
                return True
            
            # Check HH:MM:SS format
            if re.match(self._TIME_WITH_SECONDS_FORMAT, check_value):
                datetime.strptime(check_value, "%H:%M:%S")
                return True
            
            # Check full YYYY-MM-DD HH:MM:SS format
            datetime.strptime(check_value, "%Y-%m-%d %H:%M:%S")
            return True

        except:
            return False

    def format_full(self, value: Any = None) -> str:
        """
        Format the timestamp to full 'YYYY-MM-DD HH:MM:SS' using context date for partial times.
        Raises ValueError if the timestamp is invalid or if context date is not set.
        Which should never happen as validate is called first.        
        """

        value = value if value is not None else self.value

        base_date = self.context.observation_date
        if base_date is None:
            raise ValueError("Cannot convert to full timestamp without a base date.")
        
        if not self.validate(value):
            raise ValueError("Invalid timestamp format.")

        value_str = str(value)

        # Handle HH format
        if re.match(self._HOUR_FORMAT, value_str):
            hour = int(value_str)
            time_object = datetime.strptime(f"{hour:02d}:00:00", "%H:%M:%S").time()
            dt = datetime.combine(base_date, time_object)

            # Add a day if hour is before noon
            if hour < self._NOON_HOUR:
                dt += timedelta(days=1)

            return dt.strftime("%Y-%m-%d %H:%M:%S")

        # Handle HH:MM format
        if re.match(self._TIME_FORMAT, value_str):
            time_object = datetime.strptime(value_str, "%H:%M").time()
            dt = datetime.combine(base_date, time_object)

            # Add a day if time is before noon
            if time_object < self._NOON_TIME:
                dt += timedelta(days=1)

            return dt.strftime("%Y-%m-%d %H:%M:%S")

        # Handle HH:MM:SS format
        if re.match(self._TIME_WITH_SECONDS_FORMAT, value_str):
            time_object = datetime.strptime(value_str, "%H:%M:%S").time()
            dt = datetime.combine(base_date, time_object)

            # Add a day if time is before noon
            if time_object < self._NOON_TIME_WITH_SECONDS:
                dt += timedelta(days=1)

            return dt.strftime("%Y-%m-%d %H:%M:%S")

        # Already in full datetime format
        return value_str

    def expected_format(self) -> str:
        """Return expected input description"""
        return "HH | HH:MM | HH:MM:SS"

class EquatorialAngle(Int):
    """Mechanical angle validator with telescope-dependent bounds."""
    default = 180
    min_value = 0
    max_value = 360
    dependencies = ['telescope'] # depends on selected telescope
    
    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """Called when dependency changes. Updates when telescope changes."""
        if name == 'telescope':
            self.update_limits(value)
            self._update_widget_state(value)

    def _update_widget_state(self, telescope: Optional[int]) -> None:
        """Update widget state based on selected telescope."""
        if isinstance(self._widget, QLineEdit):
            self._widget.setPlaceholderText(self.expected_format())

    def update_limits(self, telescope: Optional[int]) -> None:
        """Update limits based on selected telescope."""
        if telescope is None or telescope == 0:
            self.min_value = 0
            self.max_value = 360
        else:
            self.min_value = TELESCOPESCONFIG[telescope].ROTATOR.LIMIT_LOW
            self.max_value = TELESCOPESCONFIG[telescope].ROTATOR.LIMIT_HIGH

class FilterWheel(BaseModel):
    """Filter wheel selection based on selected telescope."""
    dependencies = ['telescope'] # depends on selected telescope

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.options = {}

    def input_widget(self) -> QWidget:
        widget = QComboBox()
        widget.setStyleSheet("QComboBox { combobox-popup: 0; }")
        
        self._widget = widget

        self._update_widget_state()

        def handle_change(index):
            # Filter positions are 1-based
            self.value = index + 1

        # Set initial selection if value is set
        if self.value is not None and 1 <= self.value <= len(self.options):
            widget.setCurrentIndex(self.value - 1)

        widget.currentIndexChanged.connect(handle_change)
        return widget
    
    def _on_dependency_changed(self, name: str, value: Any) -> None:
        """React to telescoep changes."""
        if name == 'telescope':
            self._update_widget_state()

    def _update_widget_state(self) -> None:
        """Populate the combo box with filter options based on the selected telescope."""

        if not isinstance(self._widget, QComboBox):
            return

        self._widget.clear()

        telescope = self.context.telescope
        
        if telescope is None or telescope == 0:
            self._widget.addItems(["Select telescope first"])
            self._widget.setEnabled(False)
            self.options = {}
            self.value = None
            return
        
        has_filterwheel = TELESCOPESCONFIG[telescope].CAMERA.HAS_FILTERWHEEL
        self.options = TELESCOPESCONFIG[telescope].FILTERWHEEL.FILTERS
        
        if has_filterwheel and self.options:
            self._widget.addItems(self.options.values())
            self._widget.setEnabled(True)
            self.value = 1
        else:
            self._widget.addItems(["N/A"])
            self._widget.setEnabled(False)
            self.value = None

    def format(self) -> Any:
        """
        Return the selected filter key
        If not filterwheel available, return 0
        """
        telescope = self.context.telescope
        
        if telescope is None or telescope == 0:
            return 0
        
        has_filterwheel = TELESCOPESCONFIG[telescope].CAMERA.HAS_FILTERWHEEL
        
        if not has_filterwheel:
            return 0
        
        if self.value is None:
            return 0

        return self.value

    def validate(self, value: Any = None) -> bool:
        check_value = value if value is not None else self.value

        try:
            telescope = self.context.telescope
            
            if telescope is None or telescope == 0:
                return False
            
            has_filterwheel = TELESCOPESCONFIG[telescope].CAMERA.HAS_FILTERWHEEL
            
            if not has_filterwheel:
                return True
            
            return 1 <= int(check_value) <= len(TELESCOPESCONFIG[telescope].FILTERWHEEL.FILTERS)
        except:
            return False

    def expected_format(self) -> str:
        """Return expected input description based on selected telescope."""
        telescope = self.context.telescope

        if telescope is None or telescope == 0:
            return "Select telescope first"
        
        has_filterwheel = TELESCOPESCONFIG[telescope].CAMERA.HAS_FILTERWHEEL
        
        if not has_filterwheel:
            return "No filter wheel available"
        
        return "Select filter"



@dataclass
class ObjectCatalogEntry:
    """Data class for object catalog entries"""
    RA: str
    DEC: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ObjectCatalogEntry':
        return cls(RA=data['RA'], DEC=data['DEC'])

class ObjectCatalog:
    """Manages the object catalog for storing and retrieving celestial object coordinates."""
    def __init__(self, catalog_path: Optional[str] = None):
        if catalog_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            catalog_path = os.path.join(current_dir, "object_catalog.json")

        self.catalog_path = catalog_path
        self._catalog: Dict[str, ObjectCatalogEntry] = {}
        self.load()

    def load(self) -> bool:
        """Load catalog from JSON."""
        try:
            if not os.path.exists(self.catalog_path):
                self._catalog = {}
                self.save()
                return True
        
            with open(self.catalog_path, 'r') as f:
                data = json.load(f)
                self._catalog = {
                    name: ObjectCatalogEntry.from_dict(coords)
                    for name, coords in data.items()
                }
            return True
        except Exception as e:
            print(f"Error loading catalog: {e}")
            self._catalog = {}
            return False
        
    def save(self) -> bool:
        """Save catalog to JSON file."""
        try:
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
    
    def add(self, object_name: str, ra: str, dec: str) -> bool:
        """Add or update an object in the catalog."""
        try:
            ra_parsed = Ra.parse(ra)
            dec_parsed = Dec.parse(dec)
            if ra_parsed is None or dec_parsed is None:
                raise ValueError("Ra or Dec invalid")
            self._catalog[object_name] = ObjectCatalogEntry(RA=ra, DEC=dec)
            return self.save()
        except Exception as e:
            print(f"Error adding object: {e}")
            return False
    
    def delete(self, object_name: str) -> bool:
        """Delete an object from the catalog."""
        if object_name not in self._catalog:
            return False
        
        try:
            del self._catalog[object_name]
            return self.save()
        except Exception as e:
            print(f"Error deleting object: {e}")
            return False
    
    def get(self, object_name: str) -> Optional[ObjectCatalogEntry]:
        """Get an object's coordinates from the catalog."""
        return self._catalog.get(object_name)
    
    def exists(self, object_name: str) -> bool:
        """Check if an object exists in the catalog."""
        return object_name in self._catalog
    
    def get_all(self) -> Dict[str, ObjectCatalogEntry]:
        """Get all objects in the catalog."""
        return self._catalog.copy()
    
    def get_names(self) -> list[str]:
        """Get all object names in the catalog."""
        return sorted(self._catalog.keys())
    
    def clear(self) -> bool:
        """Clear all entries from the catalog."""
        self._catalog = {}
        return self.save()
    
    def __len__(self) -> int:
        """Return number of objects in catalog."""
        return len(self._catalog)
    
    def __contains__(self, object_name: str) -> bool:
        """Check if object exists using 'in' operator."""
        return object_name in self._catalog
    
    def __getitem__(self, object_name: str) -> ObjectCatalogEntry:
        """Get object using bracket notation."""
        return self._catalog[object_name]
    
    def __repr__(self) -> str:
        """String representation of catalog."""
        return f"ObjectCatalog({len(self._catalog)} objects)"