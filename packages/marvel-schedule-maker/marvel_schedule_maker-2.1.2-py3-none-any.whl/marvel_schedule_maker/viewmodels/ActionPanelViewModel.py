from typing import Optional
from PyQt6.QtCore import pyqtSignal, QObject

from marvel_schedule_maker.models import ActionFieldModel
from marvel_schedule_maker.models.ActionContext import ActionContext
from marvel_schedule_maker.models.ActionPanelUIConfig import ActionPanelUIConfig, FieldDefinition
from marvel_schedule_maker.models.ActionRegistry import ACTION_REGISTRY, AttributeDict
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices

from marvel_schedule_maker.viewmodels.actionpanelviewmodels.InputFormViewModel import InputFormViewModel
from marvel_schedule_maker.viewmodels.actionpanelviewmodels.ObserveGraphViewModel import ObserveGraphViewModel


class ActionPanelViewModel(QObject):
    """ViewModel for ActionPanel."""

    button_visibility_changed = pyqtSignal()
    row_display_updated = pyqtSignal(str)
    child_viewmodels_changed = pyqtSignal()
    ui_config_changed = pyqtSignal(ActionPanelUIConfig)
    
    validation_failed = pyqtSignal(str)  # context: "insert" or "save"
    validation_succeeded = pyqtSignal(str)  # context: "insert" or "save"

    def __init__(self, services: ApplicationServices):
        super().__init__()

        self.services = services
        
        # Owned resources - TIER 3 responsibilities
        self.context: Optional[ActionContext] = None
        self.input_form_vm: Optional[InputFormViewModel] = None
        self.observe_graph_vm: Optional[ObserveGraphViewModel] = None
        
        # Current UI configuration
        self._current_ui_config: Optional[ActionPanelUIConfig] = None

        # Listen to service signals - ViewModel is the intermediary
        self.services.signals.editing_state_changed.connect(self._on_state_changed)
        self.services.signals.action_type_changed.connect(self._on_state_changed)
        self.services.signals.observation_date_changed.connect(self._on_date_changed)

    # ==================== Properties ====================

    @property
    def is_editing(self) -> bool:
        """Check if currently editing an entry."""
        return self.services.get_editing_entry_id() is not None
    
    @property
    def current_action_type(self) -> Optional[str]:
        """Get currently selected action type."""
        return self.services.get_action_type()
    
    @property
    def current_action_info(self) -> Optional[AttributeDict]:
        """Get action registry info for current action."""
        if self.current_action_type is not None:
            return ACTION_REGISTRY.get(self.current_action_type)
        return None
    
    @property
    def editing_entry_id(self) -> Optional[str]:
        """Get ID of entry being edited."""
        return self.services.get_editing_entry_id()
    
    @property
    def current_ui_config(self) -> Optional[ActionPanelUIConfig]:
        """Get current UI configuration."""
        return self._current_ui_config
    
    # ==================== Context & Child ViewModel Management ====================
    
    def _recreate_context_and_viewmodels(self):
        """Create context and child ViewModels based on current state."""
        action_type = self.current_action_type
        
        # STEP 0: Disconnect old child signals before recreation
        self._disconnect_child_signals()
        
        # Clear if no action selected
        if not action_type:
            self.context = None
            self.input_form_vm = None
            self.observe_graph_vm = None
            self._current_ui_config = ActionPanelUIConfig(
                show_empty_state=True,
                empty_state_message="Select an action from the dropdown above."
            )
            self.child_viewmodels_changed.emit()
            self.ui_config_changed.emit(self._current_ui_config)
            return
        
        # Check if action exists in registry
        action_info = self.current_action_info
        if not action_info:
            self.context = None
            self.input_form_vm = None
            self.observe_graph_vm = None
            self._current_ui_config = ActionPanelUIConfig(
                show_empty_state=True,
                empty_state_message=f"Action '{action_type}' not found in registry."
            )
            self.child_viewmodels_changed.emit()
            self.ui_config_changed.emit(self._current_ui_config)
            return
        
        # STEP 1: Create fresh shared context
        self.context = ActionContext(
            observation_date=self.services.get_observation_date()
        )
        
        # STEP 2: Load entry data into context if editing (INITIAL SETUP - notify=False for batch)
        entry_id = self.editing_entry_id
        editing_row = None
        if entry_id:
            entry_data = self.services.schedule.get_data_entry_by_id(entry_id)
            if entry_data:
                for key, value in entry_data.items():
                    self.context.set(key, value, value, notify=False)
            editing_row = self.services.schedule.get_row_by_id(entry_id)
        
        # STEP 3: Prepare field definitions from ActionRegistry
        field_definitions = self._prepare_field_definitions(action_type)
        
        # STEP 4: Create ALL child ViewModels atomically
        # This ensures children are always created together or not at all
        self.input_form_vm = self._create_input_form_viewmodel()
        self.observe_graph_vm = self._create_observe_graph_viewmodel(action_type)
        
        # STEP 5: Subscribe to child signals for coordination
        self._connect_child_signals()
        
        # STEP 6: Create UI configuration with field definitions
        self._current_ui_config = ActionPanelUIConfig(
            show_empty_state=False,
            show_editing_banner=self.is_editing,
            editing_row_number=editing_row,
            show_input_form=True,
            show_description=True,
            show_observe_graph=(action_type == 'OBSERVE'),
            description_text=action_info.get("description", ""),
            field_definitions=field_definitions,
            context_data={
                'observation_date': self.services.get_observation_date()
            }
        )
        
        # STEP 7: Notify View - order matters: ViewModels first, then config
        self.child_viewmodels_changed.emit()
        self.ui_config_changed.emit(self._current_ui_config)
    
    def _create_input_form_viewmodel(self) -> InputFormViewModel:
        """Create InputFormViewModel."""
        assert self.context is not None
        return InputFormViewModel(self.services, self.context)
    
    def _create_observe_graph_viewmodel(self, action_type: str) -> Optional[ObserveGraphViewModel]:
        """Create ObserveGraphViewModel conditionally."""
        assert self.context is not None
        if action_type == 'OBSERVE':
            return ObserveGraphViewModel(self.services, self.context)
        return None
    
    def _connect_child_signals(self):
        """Subscribe to child ViewModel signals."""
        # InputFormViewModel signals
        if self.input_form_vm:
            # Could subscribe to validation_changed for aggregate status
            # self.input_form_vm.validation_changed.connect(self._on_field_validation_changed)
            pass
        
        # ObserveGraphViewModel signals
        if self.observe_graph_vm:
            # Could subscribe to graph updates for status tracking
            # self.observe_graph_vm.target_curve_updated.connect(self._on_graph_updated)
            pass
    
    def _disconnect_child_signals(self):
        """Disconnect child ViewModel signals before recreation."""
        if self.input_form_vm:
            try:
                # Disconnect all signals from this child
                # PyQt will handle this automatically when object is deleted,
                # but explicit disconnection is cleaner
                self.input_form_vm.validation_changed.disconnect()
            except TypeError:
                # No connections exist
                pass
        
        if self.observe_graph_vm:
            try:
                # Disconnect graph-related signals
                self.observe_graph_vm.target_curve_updated.disconnect()
                self.observe_graph_vm.moon_curve_updated.disconnect()
                self.observe_graph_vm.horizon_limits_updated.disconnect()
                self.observe_graph_vm.time_markers_updated.disconnect()
                self.observe_graph_vm.observable_regions_updated.disconnect()
                self.observe_graph_vm.sky_view_updated.disconnect()
            except TypeError:
                # No connections exist
                pass
    
    def _prepare_field_definitions(self, action_type: str) -> list[FieldDefinition]:
        """Prepare field definitions from ActionRegistry."""
        action_info = ACTION_REGISTRY.get(action_type)
        if not action_info:
            return []
        
        validators_config = action_info.get('validators', {})
        field_definitions = []
        
        for name, field_model_class in validators_config.items():
            # Get initial value from context (already loaded if editing)
            initial_value = self.context.get(name) if self.context else None
            
            field_def = FieldDefinition(
                name=name,
                model_class=field_model_class,
                initial_value=initial_value
            )
            field_definitions.append(field_def)
        
        return field_definitions
    
    def _update_editing_row_in_config(self):
        """
        Update just the editing row number in the config.
        Used when entry moves but everything else stays the same.
        """
        if not self._current_ui_config or not self._current_ui_config.show_editing_banner:
            return
        
        entry_id = self.editing_entry_id
        if entry_id:
            editing_row = self.services.schedule.get_row_by_id(entry_id)
            # Create new config with updated row number (keep all other fields)
            self._current_ui_config = ActionPanelUIConfig(
                show_empty_state=self._current_ui_config.show_empty_state,
                empty_state_message=self._current_ui_config.empty_state_message,
                show_editing_banner=self._current_ui_config.show_editing_banner,
                editing_row_number=editing_row,
                show_input_form=self._current_ui_config.show_input_form,
                show_description=self._current_ui_config.show_description,
                show_observe_graph=self._current_ui_config.show_observe_graph,
                description_text=self._current_ui_config.description_text,
                field_definitions=self._current_ui_config.field_definitions,
                context_data=self._current_ui_config.context_data
            )
            self.ui_config_changed.emit(self._current_ui_config)
    
    # ==================== Button Visibility Logic ====================

    def should_show_insert_button(self) -> bool:
        """Insert button visible when action selected and not editing."""
        return self.current_action_type is not None and not self.is_editing
    
    def should_show_save_button(self) -> bool:
        """Save button visible when editing."""
        return self.current_action_type is not None and self.is_editing
    
    def should_show_cancel_button(self) -> bool:
        """Cancel button visible when editing."""
        return self.current_action_type is not None and self.is_editing
    
    def should_show_move_buttons(self) -> bool:
        """Move buttons visible when editing."""
        return self.current_action_type is not None and self.is_editing

    # ==================== Entry Operations (TIER 3: Read from context, don't write) ====================

    def attempt_insert(self) -> bool:
        """Attempt to insert new entry."""
        action_type = self.current_action_type
        if not action_type:
            return False
        
        # Validate form data (delegates to field models)
        if not self.input_form_vm or not self.input_form_vm.validate_all():
            self.validation_failed.emit("insert")
            return False
        
        # Collect form data from context (READ ONLY)
        form_data = self.input_form_vm.get_form_data()
        
        # Build entry
        new_entry = form_data.copy()
        new_entry['type'] = action_type
        new_entry['done'] = ActionFieldModel.StatusValue.WAITING

        # Add to schedule
        self.services.schedule.add_entry(new_entry)
        self.services.show_success(f"Inserted new {action_type} entry")
        
        # Notify success and reset
        self.validation_succeeded.emit("insert")
        self._reset_to_insert_mode()

        return True

    def attempt_save(self) -> bool:
        """Attempt to save entry changes."""
        entry_id = self.editing_entry_id
        if not entry_id:
            return False
        
        action_info = self.current_action_info
        if not action_info:
            return False
        
        # Validate form data (delegates to field models)
        if not self.input_form_vm or not self.input_form_vm.validate_all():
            self.validation_failed.emit("save")
            return False
        
        # Collect form data from context (READ ONLY)
        form_data = self.input_form_vm.get_form_data()
        
        # Build updated entry
        updated_entry = form_data.copy()
        updated_entry['type'] = self.current_action_type
        updated_entry['done'] = action_info.get('done', ActionFieldModel.StatusValue.WAITING)

        # Update schedule
        self.services.schedule.update_entry(entry_id, updated_entry)

        row = self.services.schedule.get_row_by_id(entry_id)
        self.services.show_success(f"Saved changes to entry #{row}")
        
        # Notify success and reset
        self.validation_succeeded.emit("save")
        self._reset_to_insert_mode()

        return True
    
    def cancel_editing(self):
        """Cancel editing and return to insert mode."""
        self.services.show_success("Edit cancelled")
        self._reset_to_insert_mode()

    def _reset_to_insert_mode(self):
        """Reset to insert mode by clearing editing entry."""
        self.services.clear_editing_entry()

    # ==================== Entry Movement ====================

    def move_entry_up(self):
        """Move currently editing entry up one position."""
        entry_id = self.editing_entry_id
        if entry_id:
            self.services.schedule.move_entry_up(entry_id)
            self._update_row_display(entry_id)
            self._update_editing_row_in_config()

    def move_entry_down(self):
        """Move currently editing entry down one position."""
        entry_id = self.editing_entry_id
        if entry_id:
            self.services.schedule.move_entry_down(entry_id)
            self._update_row_display(entry_id)
            self._update_editing_row_in_config()
    
    def move_entry_to_row(self, row_text: str) -> bool:
        """Move entry to specific row number."""
        entry_id = self.editing_entry_id
        if not entry_id:
            return False
        
        new_index = self._validate_row_input(row_text)
        if new_index is not None:
            self.services.schedule.move_entry_to(entry_id, new_index)
            self._update_row_display(entry_id)
            self._update_editing_row_in_config()
            return True

        return False
    
    def _validate_row_input(self, text: str) -> Optional[int]:
        """Validate and parse row input text."""
        text = text.strip()
        if not text:
            return None
    
        try:
            new_index = int(text)
        except ValueError:
            return None

        max_index = self.services.schedule.get_entry_count() - 1
        if 0 <= new_index <= max_index:
            return new_index
    
        return None
    
    def _update_row_display(self, entry_id: str):
        """Emit signal to update row display."""
        row = self.services.schedule.get_row_by_id(entry_id)
        if row is not None:
            self.row_display_updated.emit(str(row))
    
    def get_current_row_text(self) -> str:
        """Get current row number as text."""
        entry_id = self.editing_entry_id
        if entry_id is None:
            return ""
        
        row = self.services.schedule.get_row_by_id(entry_id)
        if row is None:
            return ""
        
        return str(row)

    # ==================== Signal Handlers ====================

    def _on_state_changed(self):
        """Handle state changes (action type or editing state)."""
        self._recreate_context_and_viewmodels()
        self.button_visibility_changed.emit()
        self.row_display_updated.emit(self.get_current_row_text())

    def _on_date_changed(self):
        """Handle observation date changes."""
        self._recreate_context_and_viewmodels()
