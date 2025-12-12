from datetime import datetime, timedelta
from typing import Any, Optional

from PyQt6.QtCore import pyqtSignal, QObject

from astropy.time import Time as AstroTime

from marvel_schedule_maker.models.ActionContext import ActionContext
from marvel_schedule_maker.models.Timeline import calculate_end_time
from marvel_schedule_maker.models import ActionFieldModel

from marvel_schedule_maker.utils.Astronomy import getMoonAltAz, raDecToAltAz
from marvel_schedule_maker.utils.TelescopeConfig import TELESCOPESCONFIG

from marvel_schedule_maker.services.ApplicationServices import ApplicationServices


class ObserveGraphViewModel(QObject):
    """ViewModel for ObserveGraph"""
    
    # Color constants for curves
    TARGET_CURVE_COLOR = '#3A86FF'
    MOON_CURVE_COLOR = '#516F7B'
    
    target_curve_updated = pyqtSignal(list)  # list of (alt, az) tuples
    moon_curve_updated = pyqtSignal(list)  # list of (alt, az) tuples
    horizon_limits_updated = pyqtSignal(float, float)  # min_alt, max_alt
    time_markers_updated = pyqtSignal(datetime, object)  # start_time, end_time (Optional[datetime])
    observable_regions_updated = pyqtSignal(list)  # list of (start_idx, end_idx) tuples
    sky_view_updated = pyqtSignal(object, object, object, object)  # target_curve, moon_curve, min_alt, max_alt
    legend_items_updated = pyqtSignal(list)  # list of dict {'label': str, 'color': str}
    
    def __init__(self, services: ApplicationServices, context: ActionContext):
        super().__init__()

        self.services = services
        self.context = context
        
        # Cached computed data
        self.time_points: list[datetime] = []
        self.target_curve: Optional[list[tuple[float, float]]] = None
        self.moon_curve: Optional[list[tuple[float, float]]] = None
        self.min_altitude: Optional[float] = None
        self.max_altitude: Optional[float] = None

        # When these change, recompute graphs
        self.context.watch('RA', self.update_all)
        self.context.watch('DEC', self.update_all)
        self.context.watch('telescope', self.update_all)
        self.context.watch('exp_time', self.update_all)
        self.context.watch('exp_number', self.update_all)
        self.context.watch('until_timestamp', self.update_all)
        self.context.watch('object_name', self.update_legend)
        
        # Also watch timeline changes
        self.services.signals.timeline_updated.connect(self.update_all)
    
    # ==================== Validation & Parsing ====================
    
    def _validate_and_parse_ra(self, value: Any) -> Optional[float]:
        """Parse and validate RA value."""
        ra_parsed = ActionFieldModel.Ra.parse(value)
        return float(ra_parsed) if ra_parsed is not None else None
    
    def _validate_and_parse_dec(self, value: Any) -> Optional[float]:
        """Parse and validate DEC value."""
        dec_parsed = ActionFieldModel.Dec.parse(value)
        return float(dec_parsed) if dec_parsed is not None else None
    
    # ==================== Data Generation ====================
    
    def _generate_time_points(self, start: datetime, end: datetime, interval_minutes: int = 5) -> list[datetime]:
        """Generate time points between start and end at specified intervals."""
        step = timedelta(minutes=interval_minutes)
        num_points = int((end - start).total_seconds() / step.total_seconds()) + 1
        return [start + i * step for i in range(num_points)]
    
    def _calculate_target_altazs(self, ra: float, dec: float, times: list[datetime]) -> list[tuple[float, float]]:
        """Calculate altitudes for given RA/DEC at specified times."""
        altitudes = []
        for t in times:
            astro_time = AstroTime(t)
            alt, az = raDecToAltAz(ra, dec, astro_time)
            altitudes.append((alt, az))
        return altitudes
    
    def _calculate_moon_altazs(self, times: list[datetime]) -> list[tuple[float, float]]:
        """Calculate altitudes for moon at specified times."""
        altitudes = []
        for t in times:
            astro_time = AstroTime(t)
            alt, az = getMoonAltAz(astro_time)
            altitudes.append((alt, az))
        return altitudes
    
    # ==================== Calculation Logic ====================
    
    def _calculate_observation_times(self) -> tuple[datetime, Optional[datetime]]:
        """Calculate start and end times for the observation period."""
        start_time = self.services.dates.astronomical_twilight_start
        
        entry_id = self.services.get_editing_entry_id()
        entry = self.services.get_timeline_entry_by_id(entry_id)
        
        if entry:
            start_time = entry.start_time
        else:
            telescope_idx = self.context.telescope
            if telescope_idx:
                timeline = self.services.get_timeline()
                matching_entries = [
                    entry for entry in timeline
                    if entry.telescope == telescope_idx
                ]
                if matching_entries:
                    start_time = max(entry.end_time for entry in matching_entries)
        
        # READ from context to build action data
        action_data = self.context.get_all_full()
        action_data['type'] = "OBSERVE"
        end_time = calculate_end_time(start_time, action_data)
        
        return start_time, end_time
    
    def _calculate_observable_ranges(
        self, 
        ra: float, 
        dec: float, 
        telescope_idx: int
    ) -> list[tuple[int, int]]:
        """Calculate segments where target is observable."""
        min_alt = TELESCOPESCONFIG[telescope_idx].TELESCOPE.MIN_ALTITUDE
        
        start_time = self.services.dates.civil_twilight_start - timedelta(hours=1)
        end_time = self.services.dates.civil_twilight_end + timedelta(hours=1)
        
        timestamps = self._generate_time_points(start_time, end_time)
        altazs = self._calculate_target_altazs(ra, dec, timestamps)
        altitudes = [alt for alt, az in altazs]
        
        observable_segments = []
        segment_start = None
        
        for i, alt in enumerate(altitudes):
            is_observable = min_alt <= alt
            
            if is_observable and segment_start is None:
                segment_start = i
            elif not is_observable and segment_start is not None:
                observable_segments.append((segment_start, i))
                segment_start = None
        
        if segment_start is not None:
            observable_segments.append((segment_start, len(timestamps)))
        
        return observable_segments
    
    # ==================== Update Coordination ====================
    
    def update_target_curve(self) -> None:
        """Recalculate and emit target curve (READ from context)."""
        ra = self.context.get('RA')
        dec = self.context.get('DEC')
        parsed_ra = ActionFieldModel.Ra.parse(ra)
        parsed_dec = ActionFieldModel.Dec.parse(dec)

        if parsed_ra is None or parsed_dec is None:
            self.target_curve = None
            self.target_curve_updated.emit([])
            return
        
        altazs = self._calculate_target_altazs(
            parsed_ra,
            parsed_dec,
            self.time_points
        )
        
        self.target_curve = altazs
        self.target_curve_updated.emit(altazs)
    
    def update_moon_curve(self) -> None:
        """Recalculate and emit moon curve."""
        altazs = self._calculate_moon_altazs(self.time_points)
        
        self.moon_curve = altazs
        self.moon_curve_updated.emit(altazs)
    
    def update_horizon_limits(self) -> None:
        """Update telescope horizon limits (READ from context)."""
        telescope = self.context.telescope
        if telescope is None:
            return
        
        telescope_config = TELESCOPESCONFIG[telescope]
        min_alt = telescope_config.TELESCOPE.MIN_ALTITUDE
        max_alt = telescope_config.TELESCOPE.MAX_ALTITUDE
        
        self.min_altitude = min_alt
        self.max_altitude = max_alt
        
        self.horizon_limits_updated.emit(min_alt, max_alt)
    
    def update_time_markers(self) -> None:
        """Update start and end time markers (READ from context)."""
        start_time, end_time = self._calculate_observation_times()
        
        self.start_time = start_time
        self.end_time = end_time
        
        self.time_markers_updated.emit(start_time, end_time)
    
    def update_observable_ranges(self) -> None:
        """Recalculate observable segments (READ from context)."""
        ra = self.context.get('RA')
        dec = self.context.get('DEC')
        parsed_ra = ActionFieldModel.Ra.parse(ra)
        parsed_dec = ActionFieldModel.Dec.parse(dec)
        telescope = self.context.telescope
        if parsed_ra is None or parsed_dec is None or telescope is None:
            self.observable_regions_updated.emit([])
            return
        
        segments = self._calculate_observable_ranges(
            parsed_ra,
            parsed_dec,
            telescope
        )
        
        self.observable_regions_updated.emit(segments)
    
    def update_legend(self, *args, **kwargs) -> None:
        """Update legend items with current object name."""
        objectname = self.context.get('object_name')
        
        # Use object name if available, otherwise use placeholder
        target_label = objectname if objectname else '(object)'
        
        legend_items = [
            {'label': target_label, 'color': self.TARGET_CURVE_COLOR},
            {'label': 'Moon', 'color': self.MOON_CURVE_COLOR}
        ]
        
        self.legend_items_updated.emit(legend_items)
    
    def update_all(self, *args, **kwargs) -> None:
        """Full recalculation of all data."""
        # Generate time points once at the beginning
        start_time = self.services.dates.civil_twilight_start - timedelta(hours=1)
        end_time = self.services.dates.civil_twilight_end + timedelta(hours=1)
        self.time_points = self._generate_time_points(start_time, end_time)
        
        # Now all other methods can use self.time_points
        self.update_moon_curve()
        self.update_target_curve()
        self.update_horizon_limits()
        self.update_time_markers()
        self.update_observable_ranges()
        self.update_legend()
        self._emit_sky_view_update()
    
    def _emit_sky_view_update(self) -> None:
        """Emit combined signal for sky view."""
        self.sky_view_updated.emit(
            self.target_curve,
            self.moon_curve,
            self.min_altitude,
            self.max_altitude
        )
