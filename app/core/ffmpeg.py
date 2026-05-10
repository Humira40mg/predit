from subprocess import run, CalledProcessError
from os import remove, mkdir
from pathlib import Path
from app.config.config_reader import FPS, ID, FALLBACK_IMAGE


def normalize_video_s_audio(input_path: str) -> str:
    path = Path(input_path)
    output_dir = path.parent / f"Predit_Enhanced_({ID})"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{path.stem}.mp4"
    path_suffix = path.suffix.lower()

    if path_suffix in [".mp3", ".wav"]:
        if FALLBACK_IMAGE.exists():
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(FALLBACK_IMAGE),
                "-i", str(path),                        
                "-r", str(FPS),
                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-shortest",                               
                str(output_path)
            ]
        else:
            # fallback : blackscreen lavfi
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r={FPS}",
                "-i", str(path),
                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-shortest",
                str(output_path)
            ]

    elif path_suffix in [".mp4", ".mkv"]:
        cmd = [
            "ffmpeg", "-y", "-i", str(path),
            "-r", str(FPS),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            str(output_path)
        ]

    else:
        print(f"Format not supported : '{path_suffix}'\n    in '{input_path}'\n")
        return None

    try:
        print(f"  Normalizing {input_path} to {output_path}...")
        run(cmd, check=True, capture_output=True)
        return str(output_path)
    except CalledProcessError as e:
        print(f"Error during conversion : {e}")
        print(e.stderr.decode())
        return input_path