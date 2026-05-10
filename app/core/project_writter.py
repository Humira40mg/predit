import opentimelineio as otio
from app.config.config_reader import FPS, FORMAT, ID
from app.utils.timestamps_util import ts_to_rational, ts_range

from pathlib import Path

timeline = False
def get_timeline():
    global timeline
    if timeline : return timeline

    timeline = otio.schema.Timeline(name=f"Project-{ID}")
    return timeline


def create_Track(name: str, kind):
    return otio.schema.Track(
        name=name,
        kind=kind
    )

def create_media_ref(filepath: str, total_duration: str) -> otio.schema.ExternalReference:
    return otio.schema.ExternalReference(
        target_url=filepath,
        available_range=otio.opentime.TimeRange(
            start_time=ts_to_rational(0),
            duration=ts_to_rational(total_duration)
        )
    )

def create_image_ref(filepath: str, total_duration: str) -> otio.schema.ExternalReference:
    return otio.schema.ExternalReference(
        target_url=filepath,
        available_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0,0),
            duration=otio.opentime.RationalTime(total_duration*FPS, 0)
        )
    )

def create_gap(seconds):
    return otio.schema.Gap(
        duration=ts_to_rational(seconds)
)

def create_clip(
    media_ref: otio.schema.ExternalReference,
    clip_name: str,
    source_start: str,   # timestamp 
    source_end: str,     # timestamp 
    ) -> otio.schema.Clip:
    return otio.schema.Clip(
        name=clip_name,
        media_reference=media_ref,
        source_range=ts_range(source_start, source_end)
    )

def create_image_clip(
    clip_name: str,
    media_ref,
    display_duration_seconds: float) -> otio.schema.Clip:
    return otio.schema.Clip(
        name=clip_name,
        media_reference=media_ref,
        source_range=otio.opentime.TimeRange(
            start_time=ts_to_rational(0),
            duration=ts_to_rational(display_duration_seconds)
        )
    )

def write_file(folder):
    try:
        otio.adapters.write_to_file(timeline, f"{folder}/{timeline.name}.{FORMAT}")
        print(f"The project file has been created with success :\n  {folder}/{timeline.name}.{FORMAT}")
    except Exception as e:
        otio.adapters.write_to_file(timeline, f"{folder}/{timeline.name}.otio")     # backup
        print(f"Error while writing the project file : {e}\nWritting project as otio file instead :\n  {folder}/{timeline.name}.otio")
   
