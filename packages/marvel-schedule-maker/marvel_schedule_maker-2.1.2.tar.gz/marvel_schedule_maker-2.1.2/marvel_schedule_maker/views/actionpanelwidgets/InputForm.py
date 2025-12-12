
from dataclasses import dataclass

from PyQt6.QtWidgets import QFormLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

from marvel_schedule_maker.models import ActionFieldModel

from marvel_schedule_maker.viewmodels.actionpanelviewmodels.InputFormViewModel import InputFormViewModel


@dataclass
class InputEntry:
    label_widget: QWidget
    icon: QLabel
    input_widget: QWidget
    field_model: ActionFieldModel.BaseModel


class InputForm(QWidget):
    """Manages form fields, validation icons, and input widgets for action parameters."""

    def __init__(self, viewmodel: InputFormViewModel):
        super().__init__()

        self.viewmodel = viewmodel
        self.inputs: dict[str, InputEntry] = {}
        
        self._build_layout()

        self.viewmodel.validation_changed.connect(self._on_validation_changed)
        self.viewmodel.validate_all()

    def _build_layout(self) -> None:
        """Build the form layout with all input fields."""
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setSpacing(10)

        for name in self.viewmodel.get_field_names():
            field_model = self.viewmodel.get_field_model(name)
            if field_model is None:
                continue

            icon = QLabel()
            icon.setFixedWidth(20)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label_widget = self._create_label_widget(name, icon)

            input_widget = field_model.input_widget()

            self.inputs[name] = InputEntry(
                icon=icon,
                field_model=field_model,
                label_widget=label_widget,
                input_widget=input_widget
            )

            label_widget.setFixedWidth(150)
            label_widget.setSizePolicy(
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Preferred
            )

            input_widget.setFixedWidth(250)
            input_widget.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )

            form_layout.addRow(label_widget, input_widget)

            field_model.context.watch(name, lambda field_name, value: self._on_validation_changed(field_name))

        self.setLayout(form_layout)

    def _create_label_widget(self, name: str, icon: QLabel) -> QWidget:
        """Create a label widget with text and an associated icon."""
        label = QLabel(name)
        label.setStyleSheet("font-weight: normal;")

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(icon)

        return container


    def _on_validation_changed(self, name: str) -> None:
        """Update the validation icon for a specific input field."""
        if name not in self.inputs:
            return

        icon = self.inputs[name].icon
        validator = self.inputs[name].field_model
        is_valid = validator.validate()

        if is_valid:
            icon.setStyleSheet("color: #28a745; font-weight: bold;")
            icon.setText("✔")
            icon.setToolTip("Valid input")
        else:
            icon.setStyleSheet("color: #dc3545; font-weight: bold;")
            icon.setText("✖")
            icon.setToolTip(f"Invalid input {validator.expected_format()}")

    def validate_all(self) -> bool:
        return self.viewmodel.validate_all()
