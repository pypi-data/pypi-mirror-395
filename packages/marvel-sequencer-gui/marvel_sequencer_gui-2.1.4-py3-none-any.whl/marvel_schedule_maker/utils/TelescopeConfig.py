from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

PACKAGE_ROOT = Path(__file__).parent.parent


UNITCONFIGS = {
    1: PACKAGE_ROOT / "config/units/unit1.cfg",
    2: PACKAGE_ROOT / "config/units/unit2.cfg",
    3: PACKAGE_ROOT / "config/units/unit3.cfg",
    4: PACKAGE_ROOT / "config/units/unit4.cfg",
}

@dataclass
class CameraConfig:
    GAIN: int
    OFFSET: int
    BINNING: int
    HAS_FILTERWHEEL: bool

@dataclass
class FilterWheelConfig:
    FILTERS: Dict[str, str]

@dataclass
class AutoFocuserConfig:
    FOCALLENGTH: float
    FOCUS_STEPS: int
    FOCUS_STEP_SIZE: float
    EXPOSURE_TIME: int
    DARKMASTER: str
    INNER: bool
    QUANTILE: float

@dataclass
class PlateSolverConfig:
    EXPOSURE_TIME_US: int
    MAX_ITERATIONS: int

@dataclass
class TelescopeDetailsConfig:
    MAX_ALTITUDE: int
    MIN_ALTITUDE: int
    PARK_ALTITUDE: int
    PARK_AZIMUTH: int

@dataclass
class RotatorConfig:
    LIMIT_LOW: int
    LIMIT_HIGH: int

@dataclass
class DefaultsConfig:
    PM_RA: float
    PM_DEC: float
    REF_EPOCH: float

@dataclass
class TelescopeConfig:
    ROTATOR: RotatorConfig
    TELESCOPE: TelescopeDetailsConfig
    CAMERA: CameraConfig
    FILTERWHEEL: FilterWheelConfig
    AUTOFOCUSER: AutoFocuserConfig
    PLATESOLVER: PlateSolverConfig
    DEFAULTS: DefaultsConfig

def getConstants(configfile):
    """Load constants per telescope from a config file."""
    config = ConfigParser()
    config.read(configfile)

    rotator = RotatorConfig(
        LIMIT_LOW=int(config.get("ROTATOR", "limit_low")),
        LIMIT_HIGH=int(config.get("ROTATOR", "limit_high"))
    )
    telescope = TelescopeDetailsConfig(
        MAX_ALTITUDE=int(config.get("TELESCOPE", "max_altitude")),
        MIN_ALTITUDE=int(config.get("TELESCOPE", "min_altitude")),
        PARK_ALTITUDE=int(config.get("TELESCOPE", "park_altitude")),
        PARK_AZIMUTH=int(config.get("TELESCOPE", "park_azimuth")),
    )
    camera = CameraConfig(
        GAIN=int(config.get("CAMERA", "gain")),
        OFFSET=int(config.get("CAMERA", "offset")),
        BINNING=int(config.get("CAMERA", "binning")),
        HAS_FILTERWHEEL=config.getboolean("CAMERA", "has_filterwheel")
    )
    filterwheel = FilterWheelConfig(
        FILTERS={k: v for k, v in config.items("FILTERWHEEL")}
    )
    autofocuser = AutoFocuserConfig(
        FOCALLENGTH=float(config.get("AUTOFOCUSER", "focallength")),
        FOCUS_STEPS=int(config.get("AUTOFOCUSER", "focus_steps")),
        FOCUS_STEP_SIZE=float(config.get("AUTOFOCUSER", "focus_step_size")),
        EXPOSURE_TIME=int(config.get("AUTOFOCUSER", "exposure_time")),
        DARKMASTER=config.get("AUTOFOCUSER", "darkmaster"),
        INNER=config.getboolean("AUTOFOCUSER", "inner"),
        QUANTILE=float(config.get("AUTOFOCUSER", "quantile"))
    )
    platesolver = PlateSolverConfig(
        EXPOSURE_TIME_US=int(config.get("PLATESOLVER", "exposure_time_us")),
        MAX_ITERATIONS=int(config.get("PLATESOLVER", "max_iterations"))
    )
    defaults = DefaultsConfig(
        PM_RA=float(config.get("DEFAULTS", "pm_RA")),
        PM_DEC=float(config.get("DEFAULTS", "pm_DEC")),
        REF_EPOCH=float(config.get("DEFAULTS", "ref_epoch"))
    )

    return TelescopeConfig(
        ROTATOR=rotator,
        TELESCOPE=telescope,
        CAMERA=camera,
        FILTERWHEEL=filterwheel,
        AUTOFOCUSER=autofocuser,
        PLATESOLVER=platesolver,
        DEFAULTS=defaults
    )

# Load all telescope configs
TELESCOPESCONFIG: dict[int, TelescopeConfig] = {t : getConstants(cfg) for t,cfg in UNITCONFIGS.items()}

def find_config_value(config, key):
    for _, section_obj in vars(config).items():
        if hasattr(section_obj, key.upper()):
            return getattr(section_obj, key.upper())
    return None