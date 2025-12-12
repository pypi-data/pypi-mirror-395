from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Type


@dataclass
class FieldDefinition:
    """Definition of a single form field."""
    name: str
    model_class: Type  # ActionFieldModel.BaseModel subclass
    initial_value: Any = None


@dataclass
class ActionPanelUIConfig:
    """Configuration object that defines what the ActionPanelView should display."""
    
    # Empty state
    show_empty_state: bool = False
    empty_state_message: Optional[str] = None
    
    # Editing state
    show_editing_banner: bool = False
    editing_row_number: Optional[int] = None
    
    # Content visibility flags
    show_input_form: bool = False
    show_description: bool = False
    show_observe_graph: bool = False
    
    description_text: Optional[str] = None
    
    field_definitions: List[FieldDefinition] = field(default_factory=list)
    
    context_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration consistency."""
        if self.show_empty_state and (self.show_input_form or self.show_description or self.show_observe_graph):
            raise ValueError("Empty state cannot coexist with content widgets")
        
        if self.show_editing_banner and not self.show_input_form:
            raise ValueError("Editing banner requires input form to be shown")
        
        if self.show_description and not self.description_text:
            raise ValueError("Description visibility requires description text")
        
        # PHASE 2: Validate field definitions if showing input form
        if self.show_input_form and not self.field_definitions:
            raise ValueError("Input form requires field definitions")