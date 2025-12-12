from pathlib import Path
import json
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class CelestialObjectEntry:
    ra: float
    dec: float
    
    @staticmethod
    def from_dict(data: dict) -> 'CelestialObjectEntry':
        """Create entry from dictionary."""
        return CelestialObjectEntry(
            ra=float(data['RA']),
            dec=float(data['DEC'])
        )
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary for JSON serialization."""
        return {'RA': self.ra, 'DEC': self.dec}


class CelestialObjectRepository:
    """Repository for managing celestial object catalog persistence."""
    
    # Hardcoded catalog path
    CATALOG_PATH = Path(__file__).parent.parent / "assets" / "OBJECT_CATALOG.json"
    
    def __init__(self):
        """Initialize repository with default catalog path."""
        self._catalog: Dict[str, CelestialObjectEntry] = {}
        self.load()
    
    def get(self, object_name: str) -> Optional[CelestialObjectEntry]:
        """Get an object's coordinates from the catalog."""
        if not object_name or not isinstance(object_name, str):
            return None
        return self._catalog.get(object_name.strip().lower())
    
    def add(self, object_name: str, ra: float, dec: float) -> bool:
        """Add or update an object in the catalog."""
        if not object_name:
            return False
        
        try:
            self._catalog[object_name.strip().lower()] = CelestialObjectEntry(
                ra=float(ra),
                dec=float(dec)
            )
            return self.save()  # Auto-save immediately
        except (ValueError, TypeError):
            return False
    
    def delete(self, object_name: str) -> bool:
        """Remove an object from the catalog."""
        key = object_name.strip().lower()
        if key in self._catalog:
            del self._catalog[key]
            return self.save()  # Auto-save immediately
        return False
    
    def get_all(self) -> Dict[str, CelestialObjectEntry]:
        """Get all objects in the catalog."""
        return self._catalog.copy()
    
    def clear(self) -> bool:
        """Clear all objects from catalog."""
        self._catalog.clear()
        return self.save()  # Auto-save immediately
    
    def __len__(self) -> int:
        """Return number of objects in catalog."""
        return len(self._catalog)
    
    def load(self) -> bool:
        """Load catalog from JSON file."""
        try:
            if not self.CATALOG_PATH.exists():
                self._catalog = {}
                return self.save()
            
            with self.CATALOG_PATH.open('r') as f:
                data = json.load(f)
                self._catalog = {
                    name.lower(): CelestialObjectEntry.from_dict(coords)
                    for name, coords in data.items()
                }
            return True
        except (json.JSONDecodeError, KeyError, FileNotFoundError, ValueError) as e:
            print(f"Error loading catalog: {e}")
            self._catalog = {}
            return False
    
    def save(self) -> bool:
        """Save catalog to JSON file."""
        try:
            self.CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                name: entry.to_dict()
                for name, entry in self._catalog.items()
            }
            
            with self.CATALOG_PATH.open('w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except (IOError, OSError) as e:
            print(f"Error saving catalog: {e}")
            return False