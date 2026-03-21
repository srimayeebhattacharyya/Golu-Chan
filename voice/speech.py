# import subprocess
# import recognition

# ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

# def speak(text):
#     print("Golu-Chan:", text)

#     subprocess.Popen([
#         ESPEAK_PATH,
#         "-v", "en",   # voice
#         "-s", "140",  # speed (lower = slower)
#         "-p", "40",   # pitch (lower = deeper voice)
#         text
#     ])

import subprocess
from . import recognition
import time

ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

def speak(text):

    print("Golu-Chan:", text)

    # STOP microphone
    recognition.pause_listening()

    process = subprocess.Popen([
        ESPEAK_PATH,
        "-v", "en",
        "-s", "140",
        "-p", "40",
        text
    ])

    process.wait()  # wait until speech finishes

    time.sleep(0.3)  # small buffer

    # RESUME microphone
    recognition.resume_listening()