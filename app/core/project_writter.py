import opentimelineio as otio
from app.config.config_reader import FPS, FORMAT, ID

timeline = False
def get_timeline():
    global timeline
    if timeline : return timeline

    timeline = otio.schema.Timeline(name=f"Project-{ID}")
    return timeline

def ts_to_rational(timestamp: float) -> otio.opentime.RationalTime:
    return otio.opentime.RationalTime((timestamp) * FPS, FPS)

def ts_range(start: float, end: float) -> otio.opentime.TimeRange:
    """Crée un TimeRange depuis deux timestamps."""
    t_start = ts_to_rational(start)
    t_end   = ts_to_rational(end)
    return otio.opentime.TimeRange(
        start_time=t_start,
        duration=t_end - t_start
    )

def create_Track(name: str, kind):
    return otio.schema.Track(
        name=name,
        kind=kind
    )

def create_media_ref(filepath: str, total_duration: str) -> otio.schema.ExternalReference:
    full_duration = ts_to_rational(total_duration)
    
    # Référence vers le fichier source
    return otio.schema.ExternalReference(
        target_url=f"file://{filepath}",
        available_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, FPS),
            duration=full_duration
        )
    )

def create_clip(
    media_ref: otio.schema.ExternalReference,
    clip_name: str,
    source_start: str,   # timestamp 
    source_end: str,     # timestamp 
    ) -> otio.schema.Clip:
    """
    Crée un Clip qui extrait une portion d'une vidéo.

    - available_range : toute la durée du fichier source
    - source_range    : la portion qu'on veut utiliser (le "cut")
    """
    # La portion qu'on découpe
    cut_range = ts_range(source_start, source_end)

    return otio.schema.Clip(
        name=clip_name,
        media_reference=media_ref,
        source_range=cut_range
    )

def write_file(folder):
    try:
        otio.adapters.write_to_file(timeline, f"{folder}/{timeline.name}.{FORMAT}")
        print(f"The project file has been created with success :\n  {folder}/{timeline.name}.{FORMAT}")
    except Exception as e:
        otio.adapters.write_to_file(timeline, f"{folder}/{timeline.name}.otio")     # backup
        print(f"Error while writing the project file : {e}\nWritting project as otio file instead :\n  {folder}/{timeline.name}.otio")
   