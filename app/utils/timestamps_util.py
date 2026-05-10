import opentimelineio as otio
from app.config.config_reader import FPS
from math import floor

def ts_to_rational(timestamp: float) -> otio.opentime.RationalTime:
    return otio.opentime.RationalTime(floor((timestamp) * FPS), FPS)

def ts_range(start: float, end: float) -> otio.opentime.TimeRange:
    """create a TimeRange with timestamps."""
    t_start = ts_to_rational(start)
    t_end   = ts_to_rational(end)
    return otio.opentime.TimeRange(
        start_time=t_start,
        duration=t_end - t_start
    )