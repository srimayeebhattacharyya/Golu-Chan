import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json

SAMPLE_RATE = 16000
BLOCK_DURATION = 0.2

model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
listening_enabled = True

command_queue = None
mic_volume = 0

stream = None

user_muted = False
bot_speaking = False

# def audio_callback(indata, frames, time, status):

#     global command_queue
#     global mic_volume

#     mic_volume = np.linalg.norm(indata) / len(indata)

#     data = bytes(indata)
#     # data = indata.tobytes()

#     if recognizer.AcceptWaveform(data):

#         result = json.loads(recognizer.Result())
#         text = result.get("text", "")

#         if text != "":
#             print("You said:", text)
#             command_queue = text

def audio_callback(indata, frames, time, status):

    global command_queue
    global mic_volume
    global listening_enabled
    global user_muted
    global bot_speaking

    if not listening_enabled or user_muted or bot_speaking:
        return

    audio_np = np.frombuffer(indata, dtype=np.int16)
    mic_volume = np.linalg.norm(audio_np) / len(audio_np)

    data = bytes(indata)

    if recognizer.AcceptWaveform(data):

        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if text != "":
            print("You said:", text)
            command_queue = text

def start_stream():

    global stream

    stream = sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=int(SAMPLE_RATE * BLOCK_DURATION),
        dtype="int16",
        channels=1,
        device = 1,
        callback=audio_callback
    )

    stream.start()


def get_command():
    global command_queue
    cmd = command_queue
    command_queue = None
    return cmd


def get_volume():
    return mic_volume

# def pause_listening():
#     global stream, recognizer

#     if stream:
#         stream.stop()

#     # Clear Vosk audio buffer
#     recognizer.Reset()


# def resume_listening():
#     global stream
#     if stream:
#         stream.start()

def pause_listening():
    global stream, recognizer, listening_enabled

    listening_enabled = False

    if stream and stream.active:
        stream.stop()

    recognizer.Reset()


def resume_listening():
    global stream, listening_enabled

    listening_enabled = True

    if stream and not stream.active:
        stream.start()