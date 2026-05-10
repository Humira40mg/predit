import app.rest_client.ollama as llm
from app.config.config_reader import MASCOT_FOLDER, LLM_MODEL
from app.utils.path_util import check_if_exist
from app.utils.list_util import is_empty
from .sequence import Sequence

from opentimelineio.schema import TrackKind
from os import listdir
from pathlib import Path

MASCOT_SYSTEM = """
You are a video content analysis assistant.
You are given a list of sentences.
For each sentence, analyze the dominant emotion and return the most fitting character(s)/image(s).
Use multiple media for 1 sentence, each for a 0.5 < time < 3s to dynamize the scene.

You MUST always respond in valid JSON only, with no text before or after, using this structure:
{
"segments": [
    {
    "start": 0.00,
    "end": 1.50,
    "character": "full_name"
    }
]
}

"""

class Mascot(Sequence):

    def __init__(self, speech):
        super().__init__(speech, "Character")
        self.media_folder = MASCOT_FOLDER
        self.mascot_list = [Path(file).stem for file in listdir(self.media_folder) if not file.startswith(".")]

    def do_sequence(self):
        print("\nAsking LLM to chose your character for each sentence.\nPlease wait...")
        if not check_if_exist(MASCOT_FOLDER):
            print("\nNo mascot folder found, skipping mascot sequence...")
            return
        
        if is_empty(self.mascot_list) :
            print(f"\nNo mascot found in your folder [{MASCOT_FOLDER}], skipping mascot sequence...")
            return

        if self.is_segmented_mode_activated():
            self.do_mascot_sequence_segmented()
        else:
            self.do_mascot_sequence_full()

    def do_mascot_sequence_segmented(self):
        total_sentences = len(self.speech)
        segments = []
        for i, s in enumerate(self.speech):
            prompt = f"[{s.start:.2f}s → {s.end:.2f}s] {s.text}"
            segments.extend(llm.generate(system=MASCOT_SYSTEM + "Available characters are: [{}]\nNever use the same character multiple times a row.".format(", ".join(self.mascot_list)),
                prompt = prompt,
                model=LLM_MODEL
            ))
            print(f"Parsing LLM response... [{i+1}/{total_sentences}]")
        self.parse_llm_segments(segments)
        self.save_track_to_timeline()
            

    def do_mascot_sequence_full(self):
        prompt = "\n".join([
            f"[{s.start:.2f}s → {s.end:.2f}s] {s.text}"
            for s in self.speech
        ]) + "\n\n"

        segments = llm.generate(MASCOT_SYSTEM + "Available characters are: [{}]\nNever use the same character multiple times a row.".format(", ".join(self.mascot_list)),
            prompt = prompt,
            model=LLM_MODEL
            )
        print("LLM answered !\nParsing response...")
        self.parse_llm_segments(segments)
        self.save_track_to_timeline()