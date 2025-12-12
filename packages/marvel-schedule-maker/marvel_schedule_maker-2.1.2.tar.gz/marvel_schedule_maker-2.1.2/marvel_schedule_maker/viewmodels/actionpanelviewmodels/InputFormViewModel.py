from typing import Optional
from PyQt6.QtCore import pyqtSignal, QObject

from marvel_schedule_maker.models.ActionContext import ActionContext
from marvel_schedule_maker.models.ActionRegistry import ACTION_REGISTRY
from marvel_schedule_maker.models import ActionFieldModel

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class InputFormViewModel(QObject):
    """ViewModel for InputForm."""
    
    validation_changed = pyqtSignal(str, bool)  # field_name, is_valid
    
    def __init__(self, services: ApplicationServices, context: ActionContext):
        super().__init__()

        self.services = services
        self.context = context  # TIER 1: Read/Write access (via field models)

        # Get initial data if editing (Note: context already has this data loaded)
        self.entry_data: Optional[dict] = None
        entry_id = self.services.get_editing_entry_id()
        if entry_id is not None:
            self.entry_data = self.services.schedule.get_data_entry_by_id(entry_id)

        # Store field models - these are the actual context writers
        self.field_models: dict[str, ActionFieldModel.BaseModel] = {}
        self._create_field_models()

    def _create_field_models(self) -> None:
        """Create field model instances for each field."""
        action_type = self.services.get_action_type()
        assert action_type is not None

        validators_config = ACTION_REGISTRY.get(action_type, {}).get('validators', {})
        
        for name, field_model_class in validators_config.items():
            # Initial value from context (already loaded by parent ViewModel during editing)
            initial_value = self.context.get(name)
            
            # Create field model instance
            # Field model will:
            # 1. Register itself with context to watch dependencies
            # 2. Write to context when user changes input
            # 3. React to context changes from other fields
            field_model = field_model_class(
                name=name,
                context=self.context,
                initial_value=initial_value
            )
            
            self.field_models[name] = field_model

    def get_field_model(self, name: str) -> Optional[ActionFieldModel.BaseModel]:
        """Get field model by name. Used by View to create widgets."""
        return self.field_models.get(name)
    
    def validate_field(self, name: str) -> bool:
        """Validate a specific field and emit signal."""
        field_model = self.field_models.get(name)
        if field_model is None:
            return False
        
        is_valid = field_model.validate(field_model.value)
        self.validation_changed.emit(name, is_valid)
        return is_valid
    
    def validate_all(self) -> bool:
        """Validate all fields and emit signals for each."""
        all_valid = True
        
        for name in self.field_models.keys():
            is_valid = self.validate_field(name)
            if not is_valid:
                all_valid = False
        
        return all_valid
    
    def get_field_names(self) -> list[str]:
        """Get list of all field names in order."""
        return list(self.field_models.keys())
    
    def get_form_data(self) -> dict:
        """Get all form data with full/formatted values."""
        return self.context.get_all_full()
