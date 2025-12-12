from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Tuple

from marvel_schedule_maker.models.CelestialObjectModel import CelestialObjectModel


class CelestialObjectViewModel(QObject):
    """
    ViewModel for celestial object catalog.
    Manages UI state and coordinates catalog operations.
    """
    
    # Signals
    catalog_loaded = pyqtSignal(list)  # List[Tuple[str, str, str]] for table display
    validation_error = pyqtSignal(str)  # Error message for invalid data
    
    def __init__(self):
        """Initialize ViewModel with direct model access."""
        super().__init__()
        self.model = CelestialObjectModel()
    
    # ==================== Query Methods ====================
    
    def load_celestials(self) -> List[Tuple[str, str, str]]:
        """Load celestials from catalog for display in table."""
        celestials = self.model.get_all()
        
        # Convert floats to strings for table display
        display_data = [
            (name, str(ra), str(dec))
            for name, ra, dec in celestials
        ]
        
        self.catalog_loaded.emit(display_data)
        return display_data
    
    def get_celestial_count(self) -> int:
        """Get number of celestials in catalog."""
        return self.model.celestial_count()
    
    def add_new_celestial(self) -> Tuple[str, str, str]:
        """Create default data for new celestial row."""
        return ("NEW_CELESTIAL", "0.0", "0.0")
    
    # ==================== Validation ====================
    
    def validate_row(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Validate a single row without adding to catalog."""
        return self.model.validate_celestial(name, ra, dec)
    
    # ==================== Save Operations ====================
    
    def save_all(self, table_data: List[Tuple[str, str, str]]) -> Tuple[bool, str]:
        """
        Save all table data to catalog.
        Replaces entire catalog with table contents (auto-saves).
        """
        # Validate all rows first
        validation_errors = []
        for row_num, (name, ra, dec) in enumerate(table_data, start=1):
            is_valid, error_msg = self.model.validate_celestial(name, ra, dec)
            if not is_valid:
                validation_errors.append(f"Row {row_num}: {error_msg}")
        
        if validation_errors:
            error_message = "\n".join(validation_errors)
            self.validation_error.emit(error_message)
            return (False, error_message)
        
        # Clear existing catalog
        if not self.model.clear_all():
            error_msg = "Failed to clear catalog"
            self.validation_error.emit(error_msg)
            return (False, error_msg)
        
        # Add all validated rows
        for name, ra, dec in table_data:
            success, error_msg = self.model.add_celestial(name, ra, dec)
            if not success:
                self.validation_error.emit(error_msg)
                return (False, f"Failed to add {name}: {error_msg}")
        
        return (True, f"Successfully saved {len(table_data)} celestial(s)")
    
    def reload(self) -> bool:
        """Reload catalog from disk."""
        return self.model.load()