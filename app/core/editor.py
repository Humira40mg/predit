from os import mkdir, path
from moviepy import VideoFileClip

from app.config.config_reader import TEMP_AUDIO_PATH

from app.core.derush import DeRusher
from app.core.merger import Merger
from app.core.ffmpeg import normalize_video_s_audio


class Editor():
    def __init__(self, medias_path: str):
        self.list_path = []
        self.all_clips = []
        self.medias_path = medias_path
        mkdir(medias_path)
        self.derusher = DeRusher(TEMP_AUDIO_PATH)

    def convert_videos_to_mp4_and_normalize_the_sound(self, media_list):
        self.list_path = [
            path.abspath(
                normalize_video_s_audio(media)
            ) for media in media_list
        ]
        self.list_path = [x for x in self.list_path if path.isfile(x)]
        self.list_path.sort()

    def path_to_clip(self):
        self.all_clips = [VideoFileClip(path_to_file) for path_to_file in self.list_path]

    def derush(self):
        for clip, path_to_file in zip(self.all_clips, self.list_path):
            self.derusher.extract_audio(clip) # save temp audio to find timestamps of speechs
            self.derusher.make(clip, path_to_file) # official derush in the project file
        
        self.derusher.end_of_derush()

    def merge_clips_for_stt_model(self):
        merger: Merger = Merger(self.all_clips)
        self.derusher.extract_audio(merger.full_clip)
        merger.makeSubClips(self.derusher.getTimeStamps())
        return merger.write_concatenated_audio_clips()
