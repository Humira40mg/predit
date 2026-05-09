from faster_whisper import WhisperModel
from app.config.config_reader import STT_LANGUAGE, STT_MODEL
from app.utils.timestamps_util import ts_to_rational

model = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")


def transcribe_audio(filepath: str):
    print("Transcribing audio...\n")
    segments, info = model.transcribe(
        filepath,
        word_timestamps=True,
        language=STT_LANGUAGE
    )

    if not STT_LANGUAGE:
        print(f"Language detected : {info.language}")
        
    return list(segments)