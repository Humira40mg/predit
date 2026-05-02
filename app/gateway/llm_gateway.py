import app.rest_client.ollama as llm
from app.config.config_reader import MASCOT_FOLDER, LLM_MODEL
from app.utils.path_util import check_if_exist
from app.core.project_writter import get_timeline, create_Track, create_gap, create_media_ref, create_image_clip, create_image_ref

from opentimelineio.schema import TrackKind
from os import listdir
from pathlib import Path

def mascot_sequence(speech):
    print("\nAsking LLM to chose your character for each sentence.\nPlease wait...")
    if not check_if_exist(MASCOT_FOLDER):
        print("\nNo mascot folder found, skipping mascot sequence...")
        return

    mascot_list = [Path(file).stem for file in listdir(MASCOT_FOLDER) if not file.startswith(".")]
    
    if len(mascot_list) == 0 :
        print(f"\nNo mascot found in your folder [{MASCOT_FOLDER}], skipping mascot sequence...")
        return

    prompt = "\n".join([
        f"[{s.start:.2f}s → {s.end:.2f}s] {s.text}"
        for s in speech
    ])

    segments = llm.generate("""
You are a video content analysis assistant.
You are given a list of sentences with their timestamps.
For each sentence, analyze the dominant emotion and return the most fitting character/image.

You MUST always respond in valid JSON only, with no text before or after, using this structure:
{
  "segments": [
    {
      "start": 0.00,
      "end": 2.50,
      "character": "full_name"
    }
  ]
}

    """ + "Available characters are: [{}]\nTry to not use the same character multiple times a row.".format(", ".join(mascot_list)),
    prompt = prompt,
    model=LLM_MODEL
    )

    print("\nLLM answered !\nParsing response...")

    if not segments or len(segments) == 0: 
        print("No segments returned by the LLM, skipping mascot sequence...")
        return

    track = create_Track("Character", TrackKind.Video)

    last_timestamp = 0
    for i, segment in enumerate(segments):
        start = segment.get("start")
        end = segment.get("end")
        character = segment.get("character")

        if not start or not end or not character: continue
        
        print(f"\n  Creating clip-{i}, using : {character}")
        
        for file in listdir(MASCOT_FOLDER):
            if Path(file).stem == character:
                character = file
                break

        gap_time = start - last_timestamp
        last_timestamp = end
        if gap_time > 0 :
            track.append(create_gap(gap_time))
        
        duration = end-start
        
        track.append(create_image_clip(f"image-{i}", 
            create_image_ref(f"{MASCOT_FOLDER}/{character}", duration),
            duration))

    print("\nSaving the character track to timeline...")
    get_timeline().tracks.append(track)
