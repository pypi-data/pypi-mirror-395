from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Optional

from marvel_schedule_maker.models.ObservationDateModel import ObservationDateModel
from marvel_schedule_maker.models.ActionRegistry import ACTION_DURATIONS


@dataclass
class TimelineEntry:
    id: str
    action_data: dict
    telescope: int
    start_time: datetime
    end_time: datetime



def calculate_timeline(
    entries: list[dict],
    dates: ObservationDateModel
) -> list[TimelineEntry]:
    """
    Pure function to calculate timeline from schedule entries.
    
    Args:
        entries: List of action data dictionaries
        dates: DateTimes instance for time calculations
        
    Returns:
        List of TimelineEntry objects with calculated start/end times
    """
    timeline = []
    current_start_per_telescope: dict[int, datetime] = {
        i: datetime.combine(dates.observation_date, time(12, 0, 0)) 
        for i in range(1,5)
    }
    
    for action_data in entries:
        telescope = action_data.get('telescope', 0)
        
        # Determine start time
        if telescope == 0:
            start_time = max(current_start_per_telescope.values())
        else:
            start_time = current_start_per_telescope[telescope]

        # Calculate end time
        end_time = calculate_end_time(start_time, action_data)
        
        if end_time:
            timeline.append(TimelineEntry(
                id=action_data['id'],
                action_data=action_data,
                telescope=telescope,
                start_time=start_time,
                end_time=end_time
            ))
            
            # Update start times
            if telescope == 0:
                for t in current_start_per_telescope.keys():
                    current_start_per_telescope[t] = end_time
            else:
                current_start_per_telescope[telescope] = end_time
        else:
            print(f"Problem calculating end time for {action_data.get('type')}")
    
    return timeline

def calculate_end_time(
    start_time: datetime,
    action_data: dict
) -> Optional[datetime]:
    """Calculate end time for an action."""
    if not action_data or 'type' not in action_data:
        return start_time + timedelta(seconds=300)
    
    action_type = action_data['type']
    if action_type not in ACTION_DURATIONS:
        return None
    
    # Evaluate duration expression
    duration_expr = ACTION_DURATIONS[action_type]
    for key, value in action_data.items():
        duration_expr = duration_expr.replace(key, str(value))
    duration_expr = duration_expr.strip() or '0'

    try:
        duration_seconds = float(eval(duration_expr))
    except Exception:
        return None

    # Handle timestamp constraints
    if 'until_timestamp' in action_data and action_data['until_timestamp']:
        until_time = datetime.strptime(action_data['until_timestamp'], "%Y-%m-%d %H:%M:%S")
        return min(
            start_time + timedelta(seconds=duration_seconds),
            max(start_time, until_time)
        )
    
    if 'wait_timestamp' in action_data and action_data['wait_timestamp']:
        wait_time = datetime.strptime(action_data['wait_timestamp'], "%Y-%m-%d %H:%M:%S")
        actual_start = max(start_time, wait_time)
        return actual_start + timedelta(seconds=duration_seconds)
    
    return start_time + timedelta(seconds=duration_seconds)
