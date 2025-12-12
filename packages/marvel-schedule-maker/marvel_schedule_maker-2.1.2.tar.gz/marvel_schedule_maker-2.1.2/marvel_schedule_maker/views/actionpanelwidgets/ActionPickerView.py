
from typing import Optional
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices

from marvel_schedule_maker.viewmodels.actionpanelviewmodels.ActionPickerViewModel import ActionPickerViewModel


class ActionPicker(QComboBox):
    """Dropdown where you can pick the action."""
    
    def __init__(self, services: ApplicationServices, parent=None):
        super().__init__(parent)
        
        # Create ViewModel
        self.viewmodel = ActionPickerViewModel(services)
        
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setPlaceholderText("Select Action...")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        model = QStandardItemModel()
        self.setModel(model)
        self._populate(model)

        self.currentIndexChanged.connect(self._on_selection_changed)

        self.viewmodel.action_selected.connect(self.setCurrentAction)

    def wheelEvent(self, event):
        """Block wheel events to prevent accidental changes."""
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()

    def current_action(self) -> Optional[str]:
        """Get currently selected action key."""
        return self.currentData(Qt.ItemDataRole.UserRole)

    def setCurrentAction(self, action_key: Optional[str]) -> None:
        """Set current action by key."""
        self.blockSignals(True)
        if action_key is None:
            self.setCurrentIndex(0)
        else:
            for i in range(self.count()):
                if self.itemData(i, Qt.ItemDataRole.UserRole) == action_key:
                    self.setCurrentIndex(i)
                    break
        self.blockSignals(False)

    def _on_selection_changed(self, _):
        """Handle selection change."""
        action_key = self.current_action()
        self.viewmodel.set_selected_action(action_key)

    def _populate(self, model: QStandardItemModel):
        """Populate combo box from ViewModel data."""
        categories = self.viewmodel.get_categories()
        
        for category in categories:
            # Header item (not selectable)
            header = QStandardItem(category)
            header.setFlags(Qt.ItemFlag.NoItemFlags)
            header.setForeground(Qt.GlobalColor.gray)
            model.appendRow(header)

            # Get actions for this category
            actions = self.viewmodel.get_actions_in_category(category)

            for key, attr in actions:
                child_item = QStandardItem(f"    {attr['display_name']}")
                child_item.setData(key, Qt.ItemDataRole.UserRole)
                model.appendRow(child_item)

    def showPopup(self):
        """Show popup with custom positioning."""
        super().showPopup()

        view = self.view()
        if not view:
            return
        
        popup = view.window()
        if not popup:
            return

        popup_rect = popup.geometry()
        window = self.window()
        if not window:
            return
        
        below = self.mapToGlobal(self.rect().bottomLeft())
        window_height = window.height()
        widget_bottom_y = self.mapTo(window, self.rect().bottomLeft()).y()
        space_below = window_height - widget_bottom_y
        popup.resize(popup_rect.width(), space_below - 10) 
        popup.move(below)
