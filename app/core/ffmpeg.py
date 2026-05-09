from subprocess import run, CalledProcessError
from os import remove, mkdir
from pathlib import Path
from app.config.config_reader import FPS, ID


def normalize_video_s_audio(input_path: str) -> str:
    path = Path(input_path)
    output_dir = path.parent / f"Predit_Enhanced_({ID})"
    output_dir.mkdir(parents=True, exist_ok=True)  # create the directory if needed.
    output_path = output_dir / f"{path.stem}.mp4"

    path_suffix = path.suffix.lower()

    cmd = ["ffmpeg", "-y", "-i", str(path)]

    if path_suffix in [".mp3", ".wav"]:
        cmd.extend([
            "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11"
        ])
    elif path_suffix in [".mp4", ".mkv"]:
        cmd.extend([
            "-r", str(FPS),
            "-c:v", "copy",       # copy the video (fast)
            "-c:a", "aac",        # reencode the audio (needed for loudnorm)
            "-b:a", "192k",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11"
        ])
    else:
        print(f"Format not supported : '{path_suffix}'\n    in '{input_path}'\n")
        return None

    cmd.append(str(output_path))

    try:
        print(f"  Normalizing {input_path} to {output_path}...")
        run(cmd, check=True, capture_output=True)
        return str(output_path)
    except CalledProcessError as e:
        print(f"Error during conversion : {e}")
        print(e.stderr.decode())  # print the actual error message from ffmpeg
        return input_path