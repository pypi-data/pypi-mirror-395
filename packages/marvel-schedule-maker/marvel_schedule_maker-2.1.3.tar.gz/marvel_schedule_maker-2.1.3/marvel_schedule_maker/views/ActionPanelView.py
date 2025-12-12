from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QScrollArea
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QIntValidator

from marvel_schedule_maker.models.ActionPanelUIConfig import ActionPanelUIConfig

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices
from marvel_schedule_maker.viewmodels.ActionPanelViewModel import ActionPanelViewModel

from marvel_schedule_maker.views.actionpanelwidgets.ActionDescription import ActionDescription
from marvel_schedule_maker.views.actionpanelwidgets.ActionPickerView import ActionPicker
from marvel_schedule_maker.views.actionpanelwidgets.InputForm import InputForm
from marvel_schedule_maker.views.actionpanelwidgets.ObserveGraph import ObserveGraph


class ActionPanelView(QFrame):
    """View for ActionPanel"""
    
    def __init__(self, services: ApplicationServices):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedWidth(400)

        self._services = services
        self._viewmodel = ActionPanelViewModel(services)

        self._is_refreshing = False  # Prevent re-entrant refresh calls

        # Widget references - PHASE 3: These are child Views
        self.input_form: Optional[InputForm] = None
        self.observe_graph: Optional[ObserveGraph] = None
        self.description_widget: Optional[ActionDescription] = None
        self.content_widget: Optional[QWidget] = None

        # Connect to ViewModel signals - single source of truth
        self._viewmodel.button_visibility_changed.connect(self._update_button_visability)
        self._viewmodel.ui_config_changed.connect(self._on_ui_config_changed)
        self._viewmodel.row_display_updated.connect(self._on_row_display_updated)
        self._viewmodel.child_viewmodels_changed.connect(self._on_child_viewmodels_changed)
        
        # Validation feedback signals
        self._viewmodel.validation_failed.connect(self._on_validation_failed)
        self._viewmodel.validation_succeeded.connect(self._on_validation_succeeded)

        # Setup UI
        self._setup_ui()

        # Initial setup - trigger first refresh
        self._viewmodel._recreate_context_and_viewmodels()

    def _setup_ui(self):
        """Setup the UI layout and widgets."""
        # Scroll area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #5f6368;
                min-height: 30px;
                margin: 2px 2px 2px 2px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #80868b;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                background: none;
            }
        """)
        scroll_content = QWidget()

        # Main Layout
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Action Picker at the top
        self.action_picker = ActionPicker(self._viewmodel.services, self)
        font = self.action_picker.font()
        font.setPointSize(18)
        self.action_picker.setFont(font)
        self.main_layout.addWidget(self.action_picker)

        # Action buttons
        self._setup_buttons()

        scroll_area.setWidget(scroll_content)

        panel_layout = QVBoxLayout(self)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.addWidget(scroll_area)

    def _setup_buttons(self):
        """Setup action buttons layout."""
        self.button_container = QWidget()
        button_layout = QHBoxLayout(self.button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.insert_button = QPushButton("Insert New")
        self.insert_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.insert_button.clicked.connect(self._on_insert_clicked)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.save_button.clicked.connect(self._on_save_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)

        self.btn_up = QPushButton("▲")
        self.btn_down = QPushButton("▼")
        self.btn_down.setFixedWidth(30)
        self.btn_up.setFixedWidth(30)

        self.row_input = QLineEdit()
        self.row_input.setFixedWidth(45)
        onlyAvailableRows = QIntValidator(0, 9999)
        self.row_input.setValidator(onlyAvailableRows)
        self.row_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_up.clicked.connect(self._on_button_up)
        self.btn_down.clicked.connect(self._on_button_down)
        self.row_input.returnPressed.connect(self._on_return_pressed)

        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_up)
        button_layout.addWidget(self.row_input)
        button_layout.addWidget(self.btn_down)
        button_layout.addStretch()
        button_layout.addWidget(self.insert_button)
        button_layout.addWidget(self.save_button)

        self.main_layout.addWidget(self.button_container)

    # ==================== UI Configuration Management ====================
    
    def _on_ui_config_changed(self, config: ActionPanelUIConfig):
        """Respond to UI configuration changes from ViewModel."""
        if self._is_refreshing:
            return
        
        self._is_refreshing = True
        try:
            self._render_ui_from_config(config)
        finally:
            self._is_refreshing = False
    
    def _on_child_viewmodels_changed(self):
        """Respond to ViewModel creating new child ViewModels."""
        pass

    # ==================== UI State Management ====================

    def _update_button_visability(self):
        """Update button visibility based on ViewModel state."""
        self.insert_button.setVisible(self._viewmodel.should_show_insert_button())
        self.save_button.setVisible(self._viewmodel.should_show_save_button())
        self.cancel_button.setVisible(self._viewmodel.should_show_cancel_button())

        move_buttons_visible = self._viewmodel.should_show_move_buttons()
        self.btn_up.setVisible(move_buttons_visible)
        self.btn_down.setVisible(move_buttons_visible)
        self.row_input.setVisible(move_buttons_visible)

    def _on_row_display_updated(self, row_text: str):
        """Update row input display."""
        self.row_input.setText(row_text)
    
    # ==================== Content Rendering from Config ====================

    def _clear_content(self):
        """Safely clear current content widgets."""
        if self.content_widget:
            try:
                self.content_widget.setParent(None)
                self.main_layout.removeWidget(self.content_widget)
            except RuntimeError as e:
                print(f"Warning: Layout already deleted during clear_content: {e}")
            
            self.content_widget.deleteLater()
            self.content_widget = None

        # Clear child View references
        self.input_form = None
        self.description_widget = None
        self.observe_graph = None

    def _render_ui_from_config(self, config: ActionPanelUIConfig):
        """Render UI based purely on configuration."""
        self._clear_content()
        self._update_button_visability()

        # Show empty state
        if config.show_empty_state:
            label = QLabel(config.empty_state_message or "No content to display.")
            label.setStyleSheet("color: #666; font-style: italic; padding: 20px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_widget = label
            self.main_layout.addWidget(self.content_widget)
            return

        # Build content container
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        content.setLayout(content_layout)

        # Show editing banner if configured
        if config.show_editing_banner and config.editing_row_number is not None:
            edit_label = QLabel(f"Editing Entry #{config.editing_row_number}")
            edit_label.setStyleSheet("""
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                border: 1px solid #ffeaa7;
            """)
            content_layout.addWidget(edit_label)
        
        # Show description if configured
        if config.show_description and config.description_text:
            self.description_widget = ActionDescription(config.description_text)
            content_layout.addWidget(self.description_widget)

        # Show input form if configured AND child ViewModel exists
        if config.show_input_form and self._viewmodel.input_form_vm:
            self.input_form = InputForm(self._viewmodel.input_form_vm)
            content_layout.addWidget(self.input_form)

        # Show observe graph if configured AND child ViewModel exists
        if config.show_observe_graph and self._viewmodel.observe_graph_vm:
            self.observe_graph = ObserveGraph(self._viewmodel.observe_graph_vm)
            content_layout.addWidget(self.observe_graph)

        content_layout.addStretch()

        self.content_widget = content
        self.main_layout.addWidget(self.content_widget)

    # ==================== Button Handlers ====================

    def _on_insert_clicked(self):
        """Handle insert button click - delegate to ViewModel."""
        self._viewmodel.attempt_insert()

    def _on_save_clicked(self):
        """Handle save button click - delegate to ViewModel."""
        self._viewmodel.attempt_save()

    def _on_cancel_clicked(self):
        """Cancel editing - delegate to ViewModel."""
        self._viewmodel.cancel_editing()

    def _on_button_up(self):
        """Move entry up - delegate to ViewModel."""
        self._viewmodel.move_entry_up()

    def _on_button_down(self):
        """Move entry down - delegate to ViewModel."""
        self._viewmodel.move_entry_down()

    def _on_return_pressed(self):
        """Handle row input - delegate to ViewModel."""
        row_text = self.row_input.text()
        success = self._viewmodel.move_entry_to_row(row_text)
        self._show_row_validation_feedback(success)
        
    # ==================== Validation Feedback Handlers ====================

    def _on_validation_failed(self, context: str):
        """
        Handle validation failure from ViewModel.
        View decides how to show error based on context.
        """
        if context == "insert":
            self._shake_button(self.insert_button)
        elif context == "save":
            self._shake_button(self.save_button)

    def _on_validation_succeeded(self, context: str):
        """
        Handle validation success from ViewModel.
        """
        pass

    # ==================== Visual Feedback Helpers ====================

    def _shake_button(self, button: QPushButton):
        """Show validation error feedback on button with shake animation."""
        original_text = button.text()
        original_geometry = button.geometry()

        button.setText("Fix Invalid")
        button.adjustSize()
        button.setDisabled(True)

        QTimer.singleShot(1500, lambda: (
            button.setText(original_text),
            button.adjustSize(),
            button.setDisabled(False)
        ))
        
        self._shake_anim = QPropertyAnimation(button, b"geometry")
        self._shake_anim.setDuration(500)
        self._shake_anim.setKeyValueAt(0, original_geometry)
        self._shake_anim.setKeyValueAt(0.1, original_geometry.translated(-10, 0))
        self._shake_anim.setKeyValueAt(0.2, original_geometry.translated(0, 0))
        self._shake_anim.setKeyValueAt(0.3, original_geometry.translated(-10, 0))
        self._shake_anim.setKeyValueAt(0.4, original_geometry.translated(0, 0))
        self._shake_anim.setKeyValueAt(0.5, original_geometry)
        self._shake_anim.setEndValue(original_geometry)
        self._shake_anim.start()

    def _show_row_validation_feedback(self, success: bool):
        """Show visual feedback for row input validation."""
        if success:
            original_style = self.row_input.styleSheet()
            self.row_input.setStyleSheet("background-color: #d4edda; border: 1px solid #28a745;")
            QTimer.singleShot(300, lambda: self.row_input.setStyleSheet(original_style))
        else:
            original_style = self.row_input.styleSheet()
            original_geometry = self.row_input.geometry()
            
            self.row_input.setStyleSheet("background-color: #f8d7da; border: 1px solid #dc3545;")
            QTimer.singleShot(500, lambda: self.row_input.setStyleSheet(original_style))
            
            shake_anim = QPropertyAnimation(self.row_input, b"geometry")
            shake_anim.setDuration(300)
            shake_anim.setKeyValueAt(0.0, original_geometry)
            shake_anim.setKeyValueAt(0.25, original_geometry.translated(-5, 0))
            shake_anim.setKeyValueAt(0.75, original_geometry.translated(5, 0))
            shake_anim.setKeyValueAt(1.0, original_geometry)
            shake_anim.start()
            
            self._row_shake_anim = shake_anim
