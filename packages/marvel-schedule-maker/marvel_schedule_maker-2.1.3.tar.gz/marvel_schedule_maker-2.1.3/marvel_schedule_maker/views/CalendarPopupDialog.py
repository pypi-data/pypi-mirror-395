from typing import Optional
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QGraphicsEffect, QGraphicsDropShadowEffect
from PyQt6.QtCore import QDate, Qt


from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class CalendarPopupDialog(QDialog):
    """Popup dialog for date selection."""
    
    def __init__(self, services: Optional[ApplicationServices] = None, parent=None):
        super().__init__(parent)

        self._services = services
        self.selected_date = None

        
        self.setWindowTitle("Select Date")
        self.setModal(True)
        self.setFixedSize(400, 360)

        self.setStyleSheet("""
            QDialog {
                border: 2px solid #3498db;
                background-color: #f0f0f0;
            }
        """)
        
        self._setup_ui()
        
        self.calendar.activated.connect(self._on_date_activated)
    
    def _setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        
        # Style the calendar
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: #f0f0f0;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #2c3e50;
                background-color: white;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #95a5a6;
            }
        """)
        
        # Set initial date from ViewModel
        if (self._services):
            initial_date = self._services.get_observation_date()
            qdate = QDate(initial_date.year, initial_date.month, initial_date.day)
            self.calendar.setSelectedDate(qdate)
                
        layout.addWidget(self.calendar)
    
    def _on_date_activated(self, qdate: QDate):
        """Handle date activation (double-click or Enter)."""
        # Store the selected date but don't update services yet
        self.selected_date = qdate.toPyDate()
        self.accept()

