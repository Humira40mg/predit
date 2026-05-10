# Import necessary libraries.
# This section handles the speech recognition, audio processing, and speech timestamps.
# The moviepy library is used for creating video clips.
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from moviepy import VideoClip
import app.core.project_writter as proj
from opentimelineio.schema import TrackKind


class DeRusher:

    def __init__(self, output_audio: str):
        # Initialize the path for the output audio.
        self.output_audio = output_audio
        self.timeline = proj.get_timeline()
        self.vid_track = proj.create_Track("MainVideo", TrackKind.Video)
        self.aud_track = proj.create_Track("MainAudio", TrackKind.Audio)


    def extract_audio(self, clip: VideoClip) -> None:
        # Extract the audio from the clip and write it to the specified output file in .wav format.
        clip.audio.write_audiofile(self.output_audio)

    def getTimeStamps(self) -> list:
        # Load the speech recognition model.
        model = load_silero_vad()
        # Read the audio from the specified output file.
        wav = read_audio(self.output_audio)
        # Get the speech timestamps from the audio, using the model, and returning the duration in seconds.
        return get_speech_timestamps(
            wav,
            model,
            return_seconds=True,  # Return speech timestamps in seconds (default is samples)
        )

    def make(self, vidclip, filepath: str) -> None:
        media_ref = proj.create_media_ref(filepath, vidclip.duration)

        # Create clips from the full clip based on the speech timestamps.
        for i, timestamp in enumerate(self.getTimeStamps()):
            clip_vid = proj.create_clip(
                media_ref=media_ref,
                clip_name=filepath,
                source_start=timestamp["start"],
                source_end=timestamp["end"]
            )
            clip_aud = proj.create_clip(
                media_ref=media_ref,
                clip_name=f"clip-{filepath}-{i}",
                source_start=timestamp["start"],
                source_end=timestamp["end"]
            )
            self.vid_track.append(clip_vid)
            self.aud_track.append(clip_aud)
    
    def end_of_derush(self):
        self.timeline.tracks.append(self.vid_track)
        self.timeline.tracks.append(self.aud_track)
    


