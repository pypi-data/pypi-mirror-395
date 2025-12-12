# Stubbed sequencer.py for schedule maker package
from functools import wraps
from typing import Dict, Type, Optional
from marvel_schedule_maker.models import ActionFieldModel as Validator

def action_method(
        type: str,
        category: str,
        description: str,
        position: int,
        display_name: str,
        duration: str,
        validators: dict[str, Type[Validator.BaseModel]],
        timeline_name: Optional[str] = None
):
    def decorator(func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            return func(*args, **kwargs)
        setattr(wrapper, '__is_action_method__', True)
        setattr(wrapper, 'category', category)
        setattr(wrapper, 'type', type)
        setattr(wrapper, 'description', description)
        setattr(wrapper, 'position', position)
        setattr(wrapper, 'display_name', display_name or func.__name__)
        setattr(wrapper, 'duration', duration)
        setattr(wrapper, 'validators', validators)
        setattr(wrapper, 'timeline_name', timeline_name or display_name or func.__name__)
        return wrapper
    return decorator

class Sequencer:

    @action_method(
        category="TIME",
        position=2,
        display_name="Wait Timestamp",
        type="WAIT_TIMESTAMP",
        description="Waits till the given timestamp in UTC is reached.",
        duration="",
        validators={
            "wait_timestamp": Validator.Timestamp,
            "telescope": Validator.TelescopeWithNone
        }
    )
    def wait_timestamp(self, wait_timestamp, telescope):
        pass

    @action_method(
        category="DOME",
        position=3,
        display_name="Dome Track Start",
        type="DOME_TRACK_START",
        description="Starts the dome tracking for a given telescope.",
        duration="60",
        validators={
            "telescope": Validator.Telescope
        }
    )
    def dome_start_tracking_telescope(self, telescope):
        pass

    @action_method(
        category="DOME",
        position=4,
        display_name="Dome Track Stop",
        type="DOME_TRACK_STOP",
        description="Stops the dome tracking for a given telescope.",
        duration="60",
        validators={
            "telescope": Validator.Telescope
        }
    )
    def dome_stop_tracking_telescope(self, telescope):
        pass

    @action_method(
        category="TELESCOPE",
        position=6,
        display_name="Move Nasmyth Port",
        type="MOVE_NASMYTH",
        description="Changes the Nasmyth port of a given telescope.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "nasmyth_port": Validator.NasmythPort
        }
    )
    def move_nasmyth(self, telescope, nasmyth_port):
        pass

    @action_method(
        category="FOCUSER",
        position=1,
        display_name="Move Focus",
        type="MOVE_FOCUS",
        description="Moves the secondary mirror of the telescope to the desired position.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "focallength": Validator.FocalLength
        }
    )
    def move_focus(self, telescope, focallength):
        pass

    @action_method(
        category="CAMERA",
        position=1,
        display_name="Get Camera Temperature",
        type="GET_CAMERA_TEMPERATURE",
        description="Gets the current temperature of the camera for a given telescope.",
        duration="60",
        validators={
            "telescope": Validator.Telescope
        }
    )
    def get_camera_temperature (self, telescope):
        pass

    @action_method(
        category="CAMERA",
        position=2,
        display_name="Set Camera Temperature",
        type="SET_CAMERA_TEMPERATURE",
        description="Sets the target temperature of the camera for a given telescope.",
        duration="60",
        validators={
            "telescope": Validator.Telescope,
            "temperature": Validator.TemperatureSet
        }
    )
    def set_camera_temperature (self, telescope, temperature):
        pass

    @action_method(
        category="START/END",
        position=1,
        display_name="Night Start",
        type="NIGHT_START",
        description="Activates the telescope and the dome at a certain time.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "wait_timestamp": Validator.Timestamp,
            "nasmyth_port": Validator.NasmythPort
        }
    )
    def night_start (self,telescope, wait_timestamp, nasmyth_port):
        pass

    @action_method(
        category="START/END",
        position=2,
        display_name="Night End",
        type="NIGHT_END",
        description="Disactivates the telescope and the dome, and eventually warms the camera.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "temperature": Validator.TemperatureAmbient,
            "temperature_step": Validator.TemperatureStep,
            "temperature_delay": Validator.TemperatureDelay
        }
    )
    def night_end (
        self,
        telescope,
        temperature,
        temperature_step,
        temperature_delay
        ):
        pass

    @action_method(
        category="TELESCOPE",
        position=1,
        display_name="Move Telescope",
        type="MOVE_TELESCOPE",
        description="Moves a given telescope to the desired RA and DEC coordinates, including proper motion effects.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "RA": Validator.Ra,
            "DEC": Validator.Dec,
            "pm_ra": Validator.Float,
            "pm_dec": Validator.Float,
            "ref_epoch": Validator.Float,
            "filter_slot": Validator.FilterWheel,
        }
    )
    def move_telescope (
        self,
        telescope,
        RA,
        DEC,
        pm_ra,
        pm_dec,
        ref_epoch,
        filter_slot
        ):
        pass

    @action_method(
        category="FLATS",
        position=1,
        display_name="Take Flats",
        type="TAKE_FLATS",
        description="Takes a series of flat images to create a flat master.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "exp_time": Validator.IntPositive,
            "exp_number": Validator.IntPositive,
            "alt": Validator.Altitude,
            "azi": Validator.Azimuth,
            "binning": Validator.Binning,
            "gain": Validator.Int,
            "offset": Validator.Int,
            "filter_slot": Validator.FilterWheel,
            "flat_median": Validator.FlatMedian,
            "flat_range": Validator.FlatRange,
            "focallength": Validator.FocalLength
        }
    )
    def take_flats(
        self,
        telescope,
        exp_time,
        exp_number,
        alt,
        azi,
        binning,
        gain,
        offset,
        filter_slot,
        flat_median,
        flat_range,
        focallength
    ):
        pass

    @action_method(
        category="AUTOFOCUSER",
        position=1,
        display_name="Focus",
        type="FOCUS",
        description="Finds the best focus position by taking a series of images with different focus positions and analyzing the resulting images.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "object_name": Validator.ObjectName,
            "RA": Validator.Ra,
            "DEC": Validator.Dec,
            "pm_ra": Validator.Float,
            "pm_dec": Validator.Float,
            "ref_epoch": Validator.Float,
            "filter_slot": Validator.FilterWheel,
            "testing": Validator.Bool
        }
    )
    def autofocuser(
        self,
        telescope,
        object_name,
        RA,
        DEC,
        pm_RA,
        pm_DEC,
        ref_epoch,
        filter_slot,
        testing
    ):
        pass

    @action_method(
        category="MODEL_VERIFICATION",
        position=2,
        display_name="Model Verification",
        type="MODEL_VERIFICATION",
        description="Verifies the pointing model of the telescope by taking images at a series of points on the sky and analyzing the pointing accuracy.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "points": Validator.Int,
            "circles": Validator.Int,
            "exp_time": Validator.IntPositive,
            "gain": Validator.Int,
            "offset": Validator.Int,
            "binning": Validator.Binning,
            "filter_slot": Validator.FilterWheel
        }
    )
    def model_verification(
        self,
        telescope,
        points,
        circles,
        exp_time,
        gain,
        offset,
        binning,
        filter_slot
    ):
        pass

    @action_method(
        category="OBSERVING",
        position=1,
        display_name="Observe",
        timeline_name="Observe <object_name> for <exp_number>x <exp_time>s",
        type="OBSERVE",
        description="Takes a series of images of a given object, including moving the telescope and filterwheel, and running the platesolver to ensure accurate pointing.",
        duration="exp_time * exp_number",
        validators={
            "telescope": Validator.Telescope,
            "object_name": Validator.ObjectName,
            "exp_time": Validator.IntPositive,
            "exp_number": Validator.IntPositive,
            "until_timestamp": Validator.Timestamp,
            "RA": Validator.Ra,
            "DEC": Validator.Dec,
            "continue_bad_solve" : Validator.Bool,
            "equatorial_angle" : Validator.EquatorialAngle,
            "pm_ra": Validator.Float,
            "pm_dec": Validator.Float,
            "ref_epoch": Validator.Float,
            "filter_slot": Validator.FilterWheel,
            "gain": Validator.Int,
            "offset": Validator.Int,
            "binning": Validator.Binning
        }
    )
    def observe (
        self,
        telescope,
        object_name,
        exp_time,
        exp_number,
        until_timestamp,
        RA,
        DEC,
        continue_bad_solve,
        equatorial_angle,
        pm_ra,
        pm_dec,
        ref_epoch,
        filter_slot,
        gain,
        offset,
        binning
    ):
        pass

    @action_method(
        category="OBSERVING",
        position=2,
        display_name="Take Darks",
        type="TAKE_DARKS",
        description="Takes a series of dark images with the camera.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "exp_time": Validator.IntPositive,
            "exp_number": Validator.IntPositive,
            "gain": Validator.Int,
            "offset": Validator.Int,
            "binning": Validator.Binning
        }
    )
    def take_darks (
        self,
        telescope,
        exp_time,
        exp_number,
        gain,
        offset,
        binning
    ):
        pass

    @action_method(
        category="OBSERVING",
        position=3,
        display_name="Take Exposures",
        type="TAKE_EXPOSURES",
        description="Takes a series of images of a given object, including moving the telescope and filterwheel, but without running the platesolver.",
        duration="90",
        validators={
            "telescope": Validator.Telescope,
            "object_name": Validator.ObjectName,
            "exp_time": Validator.IntPositive,
            "exp_number": Validator.IntPositive,
            "until_timestamp": Validator.Timestamp,
            "RA": Validator.Ra,
            "DEC": Validator.Dec,
            "equatorial_angle": Validator.EquatorialAngle,
            "pm_RA": Validator.Float,
            "pm_DEC": Validator.Float,
            "ref_epoch": Validator.Float,
            "filter_slot": Validator.FilterWheel,
            "gain": Validator.Int,
            "offset": Validator.Int,
            "binning": Validator.Binning
        }
    )
    def take_exposures(
        self,
        telescope,
        object_name,
        exp_time,
        exp_number,
        until_timestamp,
        RA,
        DEC,
        equatorial_angle ,
        pm_RA,
        pm_DEC,
        ref_epoch,
        filter_slot,
        gain,
        offset,
        binning
    ):
        pass
