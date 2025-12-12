from typing import Optional
from PyQt6.QtCore import pyqtSignal, QObject

from marvel_schedule_maker.models.ActionRegistry import ACTION_REGISTRY, AttributeDict
from marvel_schedule_maker.services.ApplicationServices import ApplicationServices

class ActionPickerViewModel(QObject):
    """ViewModel for ActionPicker - manages action selection and organization."""
    
    # Signals
    action_selected = pyqtSignal(str)  # action_key
    
    def __init__(self, services: ApplicationServices):
        super().__init__()

        self.services = services

        self.services.signals.action_type_changed.connect(self.action_selected.emit)
    
    # ==================== Query Methods ====================
    
    def get_categories(self) -> list[str]:
        """Get sorted list of unique categories."""
        categories = set(attr['category'] for attr in ACTION_REGISTRY.values())
        return sorted(categories)
    
    def get_actions_in_category(self, category: str) -> list[tuple[str, AttributeDict]]:
        """Get actions for a category, sorted by position."""
        actions = [
            (key, attr) for key, attr in ACTION_REGISTRY.items()
            if attr['category'] == category
        ]
        return sorted(actions, key=lambda x: x[1]['position'])
    
    def get_display_name(self, action_key: str) -> str:
        """Get display name for action."""
        if action_key in ACTION_REGISTRY:
            return ACTION_REGISTRY[action_key]['display_name']
        return action_key
    
    # ==================== Selection Management ====================
    
    def set_selected_action(self, action_key: Optional[str]):
        """Update selected action and notify AppContext."""
        if action_key and action_key in ACTION_REGISTRY:
            self.services.set_action_type(action_key)
        elif action_key is None:
            self.services.set_action_type(None)
