# predit

> *It's easier to destroy than to build.*

**predit** is a pre-editing tool that automatically rough-cuts your footage and exports a ready-to-trim timeline in multiple formats via [OpenTimelineIO](https://opentimeline.io/).  
Feed it raw media, get back a structured project you can open directly in Kdenlive, DaVinci Resolve, Final Cut Pro, or any OTIO-compatible editor.

---

## How it works

predit currently uses **speech recognition** to detect silence, filler words, and dead air, then cuts around them.

Soon, a **local LLM via [Ollama](https://ollama.com/)** will take this further:
- Deciding which **memes** to insert and when
- Special support for **mascot (images)**, choose the best image of your character for the scene.

The philosophy: pre-editing shouldn't be creative, it should be mechanical. predit handles the boring part so you can focus on the actual edit.

---

## Compatible main input formats

| Type  | Formats            |
|-------|--------------------|
| Video | `.mp4`, `.mkv`     |
| Audio | `.mp3`, `.wav`     |

---

## Installation

```bash
pip install git+https://github.com/Humira40mg/predit.git
```

---

## Usage

```bash
# Single file or directory
predit path/to/file_or_directory

# With a custom output directory
predit path/to/file_or_directory -o path/to/output_directory
```

The output is an `.otio` file (and/or other formats) that you can import directly into your editor of choice.

### Import in DaVinci Resolve

**File → Import Timeline → Import AAF, EDL, XML...** → select the `.otio` file

### Import in Kdenlive

**File → OpenTimelineIO Import** *(requires Kdenlive ≥ 25.04)*

---

## Config File Exemple

Located in `~/.config/predit/config.yaml` after predit first use.

```yaml
fallback_image: "/home/user/Workspace/background.jpg"
directories:
  mascot: 
  memes: "/home/user/Workspace/memes"
ollama:
  url: "http://127.0.0.1:11434"
  model: "gemma4:e2b"
  headers:
  segmented_mode: false # Small context mode (better for weak hardware)
project:
  fps: 60
  format: otio # the project file format, check which one is compatible with your editor.
 # All the preinstalled formats adapters are ['maya_sequencer', 'burnins', 'cmx_3600', 'svg', 'AAF', 'ale', 'xges', 'fcp_xml', 'otio_json', 'otioz', 'otiod'].
 # You can install new adapters with pip (you don't need to edit the code of predit)

speech_to_text:
  model: "medium"
  language:  # en, fr... None == autodetect
```

---

## Roadmap

- [x] Derush via speech recognition (silence & filler removal)
- [x] Ollama integration — local LLM decision making
- [x] Emotion-aware character choosing
- [ ] Meme insertion
- [ ] Specific resources to use in the video
- [ ] Other LLM API compatibility
- [ ] Frontend UI
- [ ] Docker

---

## License

MIT
