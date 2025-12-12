from PyQt6.QtWidgets import QHBoxLayout, QFrame, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal, QSize

import qtawesome as qta

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.views.CalendarPopupDialog import CalendarPopupDialog
from marvel_schedule_maker.views.ClickableLabel import ClickableLabel
from marvel_schedule_maker.views.SolarCycleBar import SolarCycleBar

from marvel_schedule_maker.viewmodels.TopBarViewModel import TopBarViewModel


class TopBarView(QFrame):
    celestial_object_modal_requested = pyqtSignal()
    user_manual_requested = pyqtSignal()

    def __init__(self, services: ApplicationServices):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._services = services
        self._viewmodel = TopBarViewModel(self._services, parent=self)

        self._viewmodel.file_dialog_requested.connect(self._show_file_dialog)

        # Connect to observation date changes
        self._services.signals.observation_date_changed.connect(self._update_date_label)

        self.main_layout = QHBoxLayout()

        buttons_size = QSize(32, 32)

        # File operation buttons
        new_icon = qta.icon('fa6.file')
        new_button = QPushButton()
        new_button.setIcon(new_icon)
        new_button.setIconSize(buttons_size)
        new_button.setToolTip("New schedule")
        new_button.clicked.connect(self._viewmodel.request_new_schedule)

        load_icon = qta.icon('fa6.folder-open')
        load_button = QPushButton()
        load_button.setIcon(load_icon)
        load_button.setIconSize(buttons_size)
        load_button.setToolTip("Open schedule")
        load_button.clicked.connect(self._viewmodel.request_load_schedule)

        save_icon = qta.icon('fa6.floppy-disk')
        save_button = QPushButton()
        save_button.setIcon(save_icon)
        save_button.setIconSize(buttons_size)
        save_button.setToolTip("Save schedule")
        save_button.clicked.connect(self._viewmodel.request_save_schedule)

        celestial_object_icon = qta.icon('fa6s.gear')
        celestial_object_button = QPushButton()
        celestial_object_button.setIcon(celestial_object_icon)
        celestial_object_button.setIconSize(buttons_size)
        celestial_object_button.setToolTip("Celestian Objects")
        celestial_object_button.clicked.connect(self.open_celestial_object_modal)

        user_manual_icon = qta.icon('fa6s.circle-question')
        user_manual_button = QPushButton()
        user_manual_button.setIcon(user_manual_icon)
        user_manual_button.setIconSize(buttons_size)
        user_manual_button.setToolTip("User Manual")
        user_manual_button.clicked.connect(self.open_user_manual)

        self._date_label = ClickableLabel(parent=self)
        self._date_label.setToolTip("Click to change observation date")
        self._date_label.clicked.connect(self._show_calendar_popup)
        self._update_date_label()

        solar_cycle_bar = SolarCycleBar(self._services, parent=self)

        # Layout assembly
        self.main_layout.addWidget(solar_cycle_bar)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self._date_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(new_button)
        self.main_layout.addWidget(load_button)
        self.main_layout.addWidget(save_button)
        self.main_layout.addWidget(celestial_object_button)
        self.main_layout.addWidget(user_manual_button)

        self.setLayout(self.main_layout)

    def _show_calendar_popup(self):
        """Show calendar popup dialog for date selection."""
        dialog = CalendarPopupDialog(self._services, self)
        if dialog.exec():
            if dat:= dialog.selected_date:
                self._services.set_observation_date(dat)

    def _update_date_label(self):
        """Update the date label from ViewModel."""
        new_date = self._services.get_observation_date()
        formatted_date = new_date.strftime('%A, %B %d, %Y')
        self._date_label.setText(formatted_date)

    def _show_file_dialog(self, action: str, suggested_path: str):
        """Show file dialog - View responsibility."""
        if action == "open":
            filepath, _ = QFileDialog.getOpenFileName(
                self,
                "Open CSV",
                "",
                "CSV Files (*.csv)"
            )
            if filepath:
                self._viewmodel.load_schedule(filepath)
        elif action == "save":
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV",
                suggested_path,
                "CSV Files (*.csv)"
            )
            if filepath:
                self._viewmodel.save_schedule(filepath)

    def open_celestial_object_modal(self):
        """Emit signal to request settings modal to open."""
        self.celestial_object_modal_requested.emit()

    def open_user_manual(self):
        """Emit signal to request user manual dialog to open."""
        self.user_manual_requested.emit()

    def paintEvent(self, event):
        """Override to track when TopBarView repaints."""
        super().paintEvent(event)