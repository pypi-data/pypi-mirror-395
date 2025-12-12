from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

PACKAGE_ROOT = Path(__file__).parent.parent


UNITCONFIGS = {
    1: PACKAGE_ROOT / "config/units/unit1.cfg",
    2: PACKAGE_ROOT / "config/units/unit2.cfg",
    3: PACKAGE_ROOT / "config/units/unit3.cfg",
    4: PACKAGE_ROOT / "config/units/unit4.cfg",
}

class FilterWheel:
    def __init__(self, filters: Dict[str, str]):
        self.FILTERS = filters


class TelescopeConfig:
    def __init__(self, config: ConfigParser):
        self._config = config
        
        # Load FILTERWHEEL.FILTERS
        if config.has_section("FILTERWHEEL"):
            self.FILTERWHEEL = FilterWheel(dict(config.items("FILTERWHEEL")))
        else:
            self.FILTERWHEEL = FilterWheel({})
    
    def get(self, section_or_key: str, key: Optional[str] = None) -> Optional[str]:
        """Get a config value by section and key, or just key (searches all sections).
        
        Usage:
            config.get('ROTATOR', 'limit_low')  # specific section
            config.get('limit_low')              # search all sections
        """
        # If key is provided, use specific section
        if key is not None:
            section = section_or_key
            if not self._config.has_section(section):
                return None
            if not self._config.has_option(section, key):
                return None
            return self._config.get(section, key)
        
        # Otherwise search all sections for the key
        key = section_or_key
        for section in self._config.sections():
            if self._config.has_option(section, key):
                return self._config.get(section, key)
        
        return None


def getConstants(configfile: Path) -> TelescopeConfig:
    """Load constants per telescope from a config file."""
    config = ConfigParser()
    config.read(configfile)
    return TelescopeConfig(config)


# Load all telescope configs
TELESCOPESCONFIG: Dict[int, TelescopeConfig] = {
    t: getConstants(cfg) for t, cfg in UNITCONFIGS.items()
}