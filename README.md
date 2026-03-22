# Golu-chan – AI Assistant Robot

Golu-chan is a Python-based AI assistant robot featuring voice interaction, emotion-driven responses, music playback, and command processing. It runs fully offline and is designed for future deployment on devices like Raspberry Pi, with support for on-device LLMs.

**Project Status:** Under active development

---

## Features

* Voice Recognition (Vosk – offline speech recognition)
* Speech Output (text-to-speech)
* Emotion Simulation (expressive UI using pygame)
* Music Playback (via yt-dlp + pygame)
* Command Processing (math, tasks, system actions)
* Local AI Integration (TinyLLaMA GGUF model)
* Fully offline (no external API dependency)

---

## Tech Stack

* Python 3.11
* pygame
* Vosk (speech recognition)
* yt-dlp (music streaming)
* numpy / sounddevice
* GGUF models (llama.cpp compatible)

---

## Project Structure

```id="g1x4nm"
golu-chan/
│
├── ai/
│   └── brain.py
│
├── audio/
│   └── music.py
│
├── commands/
│   └── handler.py
│
├── voice/
│   ├── recognition.py
│   └── speech.py
│
├── models/
│   └── tinyllama.gguf
│
├── vosk-model-small-en-us-0.15/
│
├── assets/
│   ├── alarm.wav
│   ├── eye.png
│   └── keyboard.png
│
├── control_panel.py
├── emo.py
├── golu                   # Main entry point
├── main.py                # (secondary/older entry if used)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Installation

### 1. Clone the repository

```id="q2p8tq"
git clone https://github.com/srimayeebhattacharyya/golu-chan.git
cd golu-chan
```

### 2. Install dependencies

```id="sz6v58"
pip install -r requirements.txt
```

---

## LLM Model Setup

Download the TinyLLaMA GGUF model:

https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF

From the available files, download:

```id="d0f2zh"
tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

Place it inside:

```id="9b0xsc"
models/
```

---

## Speech Model Setup (Vosk)

Download a Vosk model:

https://alphacephei.com/vosk/models

Recommended model:

```id="my9sp0"
vosk-model-small-en-us-0.15
```

Extract and place it in the root directory:

```id="8ujv1p"
vosk-model-small-en-us-0.15/
```

---

## Run the Project

```id="8rqexm"
python golu
```

---

## Example Commands

* "play song"
* "what is tan 90"
* "open music"
* "stop"
* "hello golu"

---

## Known Limitations

* UI/UX for audio and video buttons is currently not functional
* These features are under development and will be fixed in future updates

---

## Future Improvements

* Upgrade speech recognition (Whisper / Whisper.cpp)
* Add memory system (context awareness)
* Improve personality & emotion system
* Raspberry Pi deployment optimization
* Optional web dashboard

---

## Notes

* Model files are not included due to GitHub size limits
* Ensure the following exist before running:

  * `models/tinyllama.gguf`
  * `vosk-model-small-en-us-0.15/`
* Requires a working microphone and speakers

---

## Authors

**Srimayee Bhattacharyya**
**Srirup Bhattacharyya**

---

## Show Your Support

If you like this project, consider giving it a ⭐ on GitHub!
