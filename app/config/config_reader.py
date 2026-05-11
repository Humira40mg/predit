import yaml
import os
import sys
from datetime import datetime
from math import floor
from pathlib import Path

from .create_config import create_config_file

CONF_FOLDER = os.path.expanduser("~/.config/predit")
CONFIG_PATH = (f"{CONF_FOLDER}/config.yml")

if os.path.exists(CONFIG_PATH):
    print(f"Config file found.")
else:
    create_config_file()

try:
    with open(CONFIG_PATH, 'r') as file:
        config_data: dict = yaml.safe_load(file)
        print("Successfully loaded the configuration file.")
        
except yaml.YAMLError as e:
    print(f"Error loading the YAML file: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)

FALLBACK_IMAGE = config_data.get("fallback_image")
if FALLBACK_IMAGE:
    FALLBACK_IMAGE = Path(FALLBACK_IMAGE)

MASCOT_FOLDER = config_data.get("directories").get("mascot")
MEME_FOLDER = config_data.get("directories").get("memes")

OLLAMA_URL = config_data["ollama"].get("url")
LLM_MODEL = config_data["ollama"].get("model")
OLLAMA_HEADERS = config_data["ollama"].get("headers")
SEGMENTED_MODE = config_data["ollama"].get("segmented_mode")

FPS = config_data.get("project").get("fps")
FORMAT = config_data.get("project").get("format")

# Define the base directory for the project.
ROOT_DIR = Path(__file__).parent.parent.parent
TMP = f"{ROOT_DIR}/tmp"
ID = floor(datetime.now().timestamp())
ACCEPT_LIST = ['', 'y', 'yes', 'o', 'oui']
COMPATIBLE = ['mp4', 'mkv', 'mp3', 'wav']
TEMP_AUDIO_PATH = f"{TMP}/audio.wav"

if "speech_to_text" in config_data.keys():
    STT_MODEL = config_data.get("STT").get("model") or "medium"
    STT_LANGUAGE = config_data.get("STT").get("language")
else:
    STT_MODEL = "medium"
    STT_LANGUAGE = None