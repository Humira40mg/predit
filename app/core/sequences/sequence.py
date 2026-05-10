import app.rest_client.ollama as llm
from app.config.config_reader import SEGMENTED_MODE
from app.core.project_writter import get_timeline, create_Track, create_gap, create_media_ref, create_clip, create_image_clip, create_image_ref
from app.utils.list_util import is_empty
from app.utils.media_files_util import is_video, is_image, get_video_duration

from opentimelineio.schema import TrackKind
from os import listdir
from pathlib import Path

class Sequence:
    def __init__(self, speech, name = "Blank"):
        self.name = name
        self.speech = speech
        self.track = create_Track(name, TrackKind.Video)
        self.media_folder = None

    def is_segmented_mode_activated(self):
        return SEGMENTED_MODE

    def do_sequence(self):
        print("This sequence is not doing anything. You must overwrite it in your child class.")
        

    def parse_llm_segments(self, segments):
        if not segments or is_empty(segments): 
            print(f"No segments returned by the LLM, skipping {self.name} sequence...")
            return

        track_name = self.name.lower()
        last_timestamp = 0
        for i, segment in enumerate(segments):
            success, start, end, media = self.get_segment_data(segment, track_name)
            if not success: continue
            
            print(f"  Creating clip-{i}, using : {media}")
            
            media = self.get_path_to_media_file(media)
            if not media :
                continue

            if not self.add_gap(start, last_timestamp):
                continue
            last_timestamp = end

            if is_image(media):
                self.add_image(i, media, end-start)
            elif is_video(media): 
                self.add_video(i, media, end-start)
            else:
                self.track.append(create_gap(end-start))

    def get_segment_data(self, segment, key):
        start = segment.get("start")
        end = segment.get("end")
        media = segment.get(key)

        if start is None or end is None or media is None: return False, None, None, None
        return True, start, end, media

    def get_path_to_media_file(self, media:str) -> str:
        for file in listdir(self.media_folder):
            if Path(file).stem == media:
                return file
        print(f"Can't find '{media}', skipping that one.")
        return False

    def add_gap(self, start, last_timestamp):
        gap_time = round(start - last_timestamp, 2)
        if gap_time > 0 :
            self.track.append(create_gap(gap_time))
            return True
        elif gap_time < 0:
            return False
        return True
    
    def add_image(self, i, media, duration):
        self.track.append(create_image_clip(f"image-{self.name}-{i}", 
                create_image_ref(f"{self.media_folder}/{media}", duration),
                duration))
    
    def add_video(self, i, media, duration):
        filepath = f"{self.media_folder}/{media}"
        full_duration = get_video_duration(filepath)
        self.track.append(create_clip(
                clip_name=f"video-{self.name}-{i}",
                media_ref=create_media_ref(filpath, full_duration),
                source_start=0,
                source_end=min(full_duration, duration)
                )
            )

    def save_track_to_timeline(self):
        print("\nSaving the character track to timeline...")
        get_timeline().tracks.append(self.track)
