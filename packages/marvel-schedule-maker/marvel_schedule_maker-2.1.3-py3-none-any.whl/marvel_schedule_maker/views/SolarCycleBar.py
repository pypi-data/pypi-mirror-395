from datetime import datetime
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QRectF, QRect
from PyQt6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPen

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.viewmodels.SolarCycleBarViewModel import SolarCycleBarViewModel
from marvel_schedule_maker.utils.svg_renderers import create_star_svg_renderer


class SolarCycleBar(QWidget):
    """View for displaying the solar cycle bar - pure presentation layer."""
    
    def __init__(self, services: ApplicationServices, parent=None):
        super().__init__(parent)
        
        self._services = services
        self._viewmodel = SolarCycleBarViewModel(services, parent=self)
        
        # Local data storage for rendering
        self._civil_start: datetime | None = None
        self._civil_end: datetime | None = None
        self._astro_start: datetime | None = None
        self._astro_end: datetime | None = None
        self._star_positions: list[tuple[float, float, float]] = []
        
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._viewmodel.data_changed.connect(self._on_change)

        self._on_change()
    
    def _on_change(self):
        self._civil_start = self._viewmodel.civil_start
        self._civil_end = self._viewmodel.civil_end
        self._astro_start = self._viewmodel.astro_start
        self._astro_end = self._viewmodel.astro_end
        self._star_positions = self._viewmodel.star_positions.copy()

        self.update()
    
    def paintEvent(self, event):
        """Render the solar cycle bar using data from ViewModel."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Early return if no data
        if not self._civil_start or not self._civil_end or not  self._astro_start or not  self._astro_end:
            painter.end()
            
            return
        
        rect = self.rect()
        
        # Calculate bar dimensions
        bar_height = 20
        bar_y = rect.center().y() - bar_height // 2
        bar_rect = QRectF(rect.left(), bar_y, rect.width(), bar_height)
        
        
        # Create horizontal gradient
        grad = QLinearGradient(bar_rect.topLeft(), bar_rect.topRight())
        grad.setColorAt(0.0, QColor("#FFD580"))
        grad.setColorAt(0.2, QColor("#001030"))
        grad.setColorAt(0.8, QColor("#001030"))
        grad.setColorAt(1.0, QColor("#FFD580"))
        
        
        painter.fillRect(bar_rect, grad)
        
        # Draw border around bar
        painter.setPen(QPen(QColor("#FFFFFF"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(bar_rect.adjusted(0, 0, -1, -1))
        
        # Text settings
        painter.setPen(Qt.GlobalColor.black)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        
        # Draw stars
        star_renderer = create_star_svg_renderer()
        for x_factor, y_factor, radius in self._star_positions:
            x = bar_rect.left() + bar_rect.width() * x_factor
            y = (bar_rect.top() + bar_rect.height() * y_factor) - 2
            star_rect = QRectF(x - radius/2, y - radius/2, radius, radius)
            star_renderer.render(painter, star_rect)
        
        # Draw time labels
        top_y = bar_rect.top() - 10
        bottom_y = bar_rect.bottom() + 12
        
        
        # Top labels (sunrise/sunset)
        self._draw_label(painter, rect, 0.0, self._civil_start, top_y)
        self._draw_label(painter, rect, 1.0, self._civil_end, top_y)
        
        # Bottom labels (night start/end)
        self._draw_label(painter, rect, 0.2, self._astro_start, bottom_y)
        self._draw_label(painter, rect, 0.8, self._astro_end, bottom_y)
        
        painter.end()
    
    def _draw_label(self, painter: QPainter, rect: QRect, x_factor: float, time: datetime, y_pos: float):
        """Draw a time label at the specified position."""
        x = rect.width() * x_factor
        
        # Choose alignment based on x position
        if x_factor <= 0.05:
            align = Qt.AlignmentFlag.AlignLeft
            x_offset = 0
        elif x_factor >= 0.95:
            align = Qt.AlignmentFlag.AlignRight
            x_offset = -60
        else:
            align = Qt.AlignmentFlag.AlignCenter
            x_offset = -30
        
        label_rect = QRectF(x + x_offset, int(y_pos) - 10, 60, 20)
        painter.drawText(label_rect, align, time.strftime('%H:%M'))
