from typing import List, Tuple, Optional

from marvel_schedule_maker.repository.CelestialObjectRepository import CelestialObjectRepository
from marvel_schedule_maker.models.ActionFieldModel import Ra, Dec


class CelestialObjectModel:
    """
    MVVM Model for celestial objects.
    Provides validation layer over CelestialObjectRepository.
    """
    
    def __init__(self):
        """Initialize model with repository."""
        self._repo = CelestialObjectRepository()
    
    # ==================== Query Methods ====================
    
    def get_all(self) -> List[Tuple[str, float, float]]:
        """Get all celestials as list of tuples for display."""
        all_celestials = self._repo.get_all()
        result = []
        for name, entry in all_celestials.items():
            result.append((name, entry.ra, entry.dec))
        return result
    
    def get_celestial(self, name: str) -> Optional[Tuple[float, float]]:
        """Get celestial coordinates."""
        entry = self._repo.get(name)
        if not entry:
            return None
        return (entry.ra, entry.dec)
    
    def celestial_count(self) -> int:
        """Get number of celestials in catalog."""
        return len(self._repo)
    
    # ==================== Persistence ====================
    
    def load(self) -> bool:
        """Reload catalog from file."""
        return self._repo.load()
    
    # ==================== CRUD Operations ====================
    
    def add_celestial(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Add celestial with validation (auto-saves)."""
        is_valid, error_msg = self.validate_celestial(name, ra, dec)
        if not is_valid:
            return (False, error_msg)
        
        # Parse validated values
        ra_parsed = Ra.parse(ra)
        dec_parsed = Dec.parse(dec)

        if ra_parsed is None:
            return (False, "Ra is incorrect")
        if dec_parsed is None:
            return (False, "Dec is incorrect")

        success = self._repo.add(name, ra_parsed, dec_parsed)
        return (success, "" if success else "Failed to add celestial to catalog")
    
    def remove_celestial(self, name: str) -> bool:
        """Remove celestial from catalog (auto-saves)."""
        return self._repo.delete(name)
    
    def clear_all(self) -> bool:
        """Clear all celestials from catalog (auto-saves)."""
        return self._repo.clear()
    
    # ==================== Validation ====================
    
    def validate_celestial(self, name: str, ra: str, dec: str) -> Tuple[bool, str]:
        """Validate celestial data using ActionFieldModel validators."""
        if not name or not name.strip():
            return (False, "Celestial name cannot be empty")
        
        ra_parsed = Ra.parse(ra)
        if ra_parsed is None:
            return (False, f"Invalid RA format: '{ra}'. Expected format: 18.072497 or 18:04:20.99")
        
        dec_parsed = Dec.parse(dec)
        if dec_parsed is None:
            return (False, f"Invalid DEC format: '{dec}'. Expected format: 41.268750 or 41:16:07.5")
        
        return (True, "")