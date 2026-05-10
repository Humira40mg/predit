import app.rest_client.ollama as llm
from app.config.config_reader import MEME_FOLDER, LLM_MODEL
from app.utils.path_util import check_if_exist
from app.utils.list_util import is_empty
from .sequence import Sequence

from opentimelineio.schema import TrackKind
from os import listdir
from pathlib import Path

SYSTEM = """
You are a video content analysis assistant.
You are given a list of sentences.
For each sentence, analyze the senses of the words and return the most fitting/fun meme.
You can use multiple media for 1 sentence. If no meme seems to fit the sentence, return an empty JSON response.

You MUST always respond in valid JSON only, with no text before or after, using this structure:
{
"segments": [
    {
    "start": 0.00,
    "end": 1.50,
    "meme": "full_name"
    }
]
}

"""

class Memer(Sequence):

    def __init__(self, speech):
        super().__init__(speech, "Meme")
        self.media_folder = MEME_FOLDER
        self.memelist = [Path(file).stem for file in listdir(self.media_folder) if not file.startswith(".")]

    def do_sequence(self):
        print("\nAsking LLM to choose memes for the video.\nPlease wait...")
        if not check_if_exist(MEME_FOLDER):
            print("\nNo meme folder found, skipping meme sequence...")
            return
        
        if is_empty(self.memelist) :
            print(f"\nNo meme found in your folder [{MEME_FOLDER}], skipping meme sequence...")
            return

        if self.is_segmented_mode_activated():
            self.do_meme_sequence_segmented()
        else:
            self.do_meme_sequence_full()

    def do_meme_sequence_segmented(self):
        total_sentences = len(self.speech)
        segments = []
        for i, s in enumerate(self.speech):
            prompt = f"[{s.start:.2f}s → {s.end:.2f}s] {s.text}"
            segments.extend(llm.generate(system=SYSTEM + "Available memes are: [{}]\nNever use the same meme twice a row.".format(", ".join(self.memelist)),
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

        segments = llm.generate(system=SYSTEM + "Available memes are: [{}]\nNever use the same meme twice a row.".format(", ".join(self.memelist)),
            prompt = prompt,
            model=LLM_MODEL
            )
        print("LLM answered !\nParsing response...")
        self.parse_llm_segments(segments)
        self.save_track_to_timeline()

