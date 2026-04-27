from moviepy import VideoFileClip, VideoClip, concatenate_videoclips
from datetime import datetime
from os import path, mkdir
from pathlib import Path
from app.config.config_reader import TMP

class Merger:
    full_clip: VideoClip
    sub_clips: list

    def __init__(self, listVideoClips: list):
        print("Merging sources...\n")
        # Concatenate all video clips from the list to form the full clip.
        self.full_clip: VideoClip = concatenate_videoclips(listVideoClips)

    def makeSubClips(self, timestamps_list: list) -> None:
        print("Internal Derushing...\n")
        # Create sub-clips from the full clip based on the provided timestamps.
        self.sub_clips = [self.full_clip.subclipped(timestamp['start'], timestamp['end']) 
            for timestamp in timestamps_list]
        
    def write_concatenated_audio_clips(self):
        print("Merging sub-clips into audio and saving to {TMP}/merged.wav...\n")
        try:
            merged_audio = concatenate_videoclips(self.sub_clips)
            merged_audio.write_audiofile(f"{TMP}/merged.wav", logger=None)
        except Exception as e:
            print(f"Error merging sub-clips into audio: {e}\n")
