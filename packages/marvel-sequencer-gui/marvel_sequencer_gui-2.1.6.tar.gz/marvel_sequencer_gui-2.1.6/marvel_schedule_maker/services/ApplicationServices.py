import os
import re
from datetime import date, datetime, time, timedelta
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
import pandas as pd

from marvel_schedule_maker.models.NotificationTypes import NotificationType
from marvel_schedule_maker.models.ObservationDateModel import ObservationDateModel
from marvel_schedule_maker.models.ScheduleModel import ScheduleModel
from marvel_schedule_maker.models.Timeline import TimelineEntry, calculate_timeline


class ApplicationSignals(QObject):
    """Global application signals"""
    action_type_changed = pyqtSignal(str)
    observation_date_changed = pyqtSignal()
    timeline_updated = pyqtSignal()
    clipboard_updated = pyqtSignal()
    editing_state_changed = pyqtSignal()
    notification_requested = pyqtSignal(str, NotificationType)


class ApplicationServices:
    def __init__(self):
        self.schedule: ScheduleModel = ScheduleModel()
        self.dates: ObservationDateModel = ObservationDateModel()

        self._timeline: list[TimelineEntry] = []

        self._clipboard: Optional[dict] = None
        self._editing_entry_id: Optional[str] = None
        self._selected_action_type: Optional[str] = None

        self.signals = ApplicationSignals()

        self.schedule.data_changed.connect(self._on_schedule_changed)

    # ==================== Notifications ====================
    
    def _show_notification(self, message: str, notification_type: NotificationType) -> None:
        """
        Request a notification to be shown.
        Safe to call even if widget doesn't exist.
        """
        self.signals.notification_requested.emit(message, notification_type)
    
    def show_success(self, message: str) -> None:
        """Show a success notification."""
        self._show_notification(message, NotificationType.SUCCESS)
    
    def show_error(self, message: str) -> None:
        """Show an error notification."""
        self._show_notification(message, NotificationType.ERROR)
    
    def show_warning(self, message: str) -> None:
        """Show a warning notification."""
        self._show_notification(message, NotificationType.WARNING)

    # ==================== Clipboard Management ====================
    
    def set_clipboard(self, data: dict) -> None:
        """Set clipboard data and mark entry as copied."""
        self._clipboard = data.copy()
        self.signals.clipboard_updated.emit()
    
    def get_clipboard(self) -> Optional[dict]:
        """Get clipboard data (returns copy to prevent mutation)."""
        return self._clipboard.copy() if self._clipboard else None
    
    def clear_clipboard(self) -> None:
        """Clear clipboard data."""
        self._clipboard = None
        self.signals.clipboard_updated.emit()
    
    def has_clipboard(self) -> bool:
        """Check if clipboard has data."""
        return self._clipboard is not None

    # ==================== Editing State Management ====================
    
    def set_editing_entry(self, entry_id: str) -> None:
        """Set currently editing entry."""
        self._editing_entry_id = entry_id
        self.signals.editing_state_changed.emit()
    
    def clear_editing_entry(self) -> None:
        """Clear editing state."""
        self._editing_entry_id = None
        self.signals.editing_state_changed.emit()
    
    def get_editing_entry_id(self) -> Optional[str]:
        """Get currently editing entry ID."""
        return self._editing_entry_id

    # ==================== Action Type Selection ====================
    
    def set_action_type(self, action_type: Optional[str]) -> None:
        """Set selected action type."""
        self._selected_action_type = action_type
        self.signals.action_type_changed.emit(action_type)
    
    def get_action_type(self) -> Optional[str]:
        """Get selected action type."""
        return self._selected_action_type

    # ==================== Date Management ====================
    
    def set_observation_date(self, new_date: date) -> None:
        """Set observation date and trigger all dependent updates."""
        # Update the date (and recalculate twilight times)
        self.dates.set_date(new_date)
        
        # Emit signal for UI updates
        self.signals.observation_date_changed.emit()

        # Recalculate timeline with new date
        self.update_timeline()
    
    def get_observation_date(self) -> date:
        """Get current observation date."""
        return self.dates.observation_date

    # ==================== Timeline Management ====================
    
    def update_timeline(self) -> None:
        """Recalculate timeline from schedule data."""
        self._timeline = calculate_timeline(
            self.schedule.get_entries(),
            self.dates
        )
        self.signals.timeline_updated.emit()
    
    def get_timeline(self) -> list[TimelineEntry]:
        """Get current timeline."""
        return self._timeline

    def get_timeline_entry_by_id(self, entry_id: Optional[str]) -> Optional[TimelineEntry]:
        """Get timeline entry by ID."""
        if entry_id is None:
            return None
        for timeline_entry in self._timeline:
            if timeline_entry.id == entry_id:
                return timeline_entry
        return None

    # ==================== Schedule File Operations ====================
    
    def new_schedule(self) -> None:
        """Create a new empty schedule and clear UI state."""
        self.clear_clipboard()
        self.clear_editing_entry()
        self.schedule.clear()
        # data_changed signal emitted by schedule.clear()
    
    def load_schedule(self, filepath: str) -> None:
        """Load schedule from CSV file and update observation date."""
        # Read CSV
        df = pd.read_csv(filepath, index_col=False)
        df = df.replace(["", " ", "nan", "NaN", "None"], pd.NA)
        
        # Convert float columns that are really integers
        for col in df.columns:
            if df[col].dtype == float and all(
                df[col].dropna().apply(lambda x: float(x).is_integer())
            ):
                df[col] = df[col].astype("Int64")
        
        records = [
            {k: v for k, v in row.items() if pd.notna(v)}
            for _, row in df.iterrows()
        ]
        
        # Clear UI state
        self.clear_clipboard()
        self.clear_editing_entry()
        
        # Extract and set observation date (just update the date model, don't trigger timeline update yet)
        extracted_date = self._extract_date_from_filename(filepath)
        if extracted_date:
            self.set_observation_date(extracted_date)
        else:
            first_date = self._find_first_date(records)
            if first_date:
                self.set_observation_date(first_date)
        
        # Load entries without triggering signals per entry
        self.schedule.blockSignals(True)
        self.schedule.clear()
        for record in records:
            self.schedule.add_entry(record)
        self.schedule.blockSignals(False)
        
        # Emit single data_changed signal which triggers timeline recalculation
        self.schedule.data_changed.emit()
    
    def save_schedule(self, filepath: str) -> None:
        """Save schedule to CSV file."""
        if not filepath.lower().endswith('.csv'):
            filepath += '.csv'
        
        try:
            df = pd.DataFrame(self.schedule.get_entries_without_id())
            df.to_csv(filepath, index=False)
            self.show_success(f"Schedule saved to {os.path.basename(filepath)}")
        except Exception as e:
            self.show_error(f"Failed to save CSV: {e}")
    
    def update_schedule_timestamps(self) -> None:
        """Update all timestamps in schedule to match current observation date."""
        observation_date = self.dates.observation_date
        
        def full_datetime(value_str: str) -> str:
            time_object = datetime.strptime(value_str, "%Y-%m-%d %H:%M:%S").time()
            dt = datetime.combine(observation_date, time_object)
            
            # Add a day if time is before noon
            if time_object < time(12, 0, 0):
                dt += timedelta(days=1)
            
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        
        updated_entries = []
        for entry in self.schedule.get_entries():
            copied = entry.copy()
            
            if (wait_ts := copied.get('wait_timestamp')) is not None:
                copied['wait_timestamp'] = full_datetime(wait_ts)
            
            if (until_ts := copied.get('until_timestamp')) is not None:
                copied['until_timestamp'] = full_datetime(until_ts)
            
            updated_entries.append(copied)
        
        # Replace all entries at once
        self.schedule.blockSignals(True)
        self.schedule.clear()
        for entry in updated_entries:
            self.schedule.add_entry(entry)
        self.schedule.blockSignals(False)
        
        self.schedule.data_changed.emit()

    # ==================== Helper Methods ====================
    
    def _extract_date_from_filename(self, filepath: str) -> Optional[date]:
        """Extract date from filename pattern YYYYMMDD."""
        filename = os.path.basename(filepath)
        pattern = r'(\d{8})'
        match = re.search(pattern, filename)
        
        if match:
            date_str = match.group(1)
            try:
                return datetime.strptime(date_str, "%Y%m%d").date()
            except ValueError:
                return None
        return None
    
    def _find_first_date(self, records: list[dict]) -> Optional[date]:
        """Find the first date from wait_timestamp in records."""
        for record in records:
            if (timestamp := record.get('wait_timestamp')) is not None:
                try:
                    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()
                except ValueError:
                    continue
        return None

    # ==================== Internal Signal Handlers ====================
    
    def _on_schedule_changed(self) -> None:
        """Handle schedule data changes - recalculate timeline."""
        self.update_timeline()

