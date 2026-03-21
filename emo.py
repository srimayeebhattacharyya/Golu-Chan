import pygame
import random
import sys
import math
from datetime import datetime
import pytz
import sounddevice as sd
import numpy as np
import yt_dlp
import os
import uuid
import pyttsx3
from vosk import Model, KaldiRecognizer
import json

pygame.init()
pygame.mixer.init()

# ---------------- SPEECH ----------------
engine = pyttsx3.init()

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# ---------------- DISPLAY ----------------
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EMO")

clock = pygame.time.Clock()

BLACK = (0,0,0)
BLUE = (0,170,255)

# ---------------- LOAD ASSETS ----------------
eye_img = pygame.image.load("eye.png").convert_alpha()
eye_width, eye_height = eye_img.get_size()

alarm_sound = pygame.mixer.Sound("alarm.wav")

# ---------------- MUSIC ----------------
current_song_file = None

def download_song(song_name):

    unique_id = uuid.uuid4().hex
    filename = f"song_{unique_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{filename}.%(ext)s",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{song_name}"])

    return f"{filename}.mp3"

def speak(text):
    print("EMO:", text)
    engine.say(text)
    engine.runAndWait()

def play_song(song_name):

    global current_song_file
    global current_state

    speak(f"Ok, I will now play {song_name}")

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    current_song_file = download_song(song_name)

    pygame.mixer.music.load(current_song_file)
    pygame.mixer.music.play()

    current_state = "PLAYING"

def handle_command(text):

    text = text.lower()

    if "play" in text:

        song = text.replace("play", "").strip()

        if song == "":
            speak("Which song should I play?")
        else:
            speak(f"Ok, I will now play {song}")
            play_song(song)

    elif "stop" in text:

        pygame.mixer.music.stop()
        speak("Stopping the music")

    elif "hello" in text:

        speak("Hello, I am EMO")
# ---------------- TIMEZONE ----------------
ist = pytz.timezone("Asia/Kolkata")
alarm_hour = 5
alarm_minute = 0

# ---------------- STATE ----------------
current_state = "IDLE"

alarm_playing = False
alarm_start_time = 0
alarm_duration_seconds = 10

alarm_today_triggered = False
last_checked_date = None

sleep_delay_seconds = 60
last_active_time = pygame.time.get_ticks()

listening_timeout = 2000
last_sound_time = 0

# ---------------- MICROPHONE ----------------
SAMPLE_RATE = 16000
BLOCK_DURATION = 0.2
THRESHOLD = 0.01

mic_volume = 0

# ---------------- SPEECH RECOGNITION ----------------
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("Voice recognition ready")
# ---------------- POSITION ----------------
left_eye_x = 70
right_eye_x = 270
eye_y = 105

# ---------------- BLINK ----------------
blink_timer = 0
blink_duration = random.randint(6,12)
next_blink = random.randint(240,480)
blinking = False

# ---------------- SLEEP Z ----------------
z_x = right_eye_x + 80
z_y = eye_y - 10
z_size = 20

# ---------------- MUSIC NOTES ----------------
note_x = WIDTH//2 + 40
note_y = eye_y - 10
note_size = 20
note_symbol = "♪"

command_queue = None

def audio_callback(indata, frames, time, status):

    global command_queue

    data = bytes(indata)

    if recognizer.AcceptWaveform(data):

        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if text != "":
            print("You said:", text)
            command_queue = text

stream = sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize = int(SAMPLE_RATE * BLOCK_DURATION),
    dtype = "int16",
    channels = 1,
    device = 1,
    callback = audio_callback
)

stream.start()

# ---------------- HEADPHONES DRAW ----------------
def draw_headphones(shake_offset=0):

    gap = 12
    cup_width = int(eye_width * 0.3)
    cup_height = eye_height

    left_cup_x = left_eye_x - cup_width - gap + shake_offset
    right_cup_x = right_eye_x + eye_width + gap + shake_offset

    cup_y = eye_y

    pygame.draw.rect(screen,(0,170,255),(left_cup_x,cup_y,cup_width,cup_height),border_radius=18)
    pygame.draw.rect(screen,(0,170,255),(right_cup_x,cup_y,cup_width,cup_height),border_radius=18)

    pad = 6

    pygame.draw.rect(screen,(0,220,255),(left_cup_x+pad,cup_y+pad,cup_width-pad*2,cup_height-pad*2),border_radius=14)
    pygame.draw.rect(screen,(0,220,255),(right_cup_x+pad,cup_y+pad,cup_width-pad*2,cup_height-pad*2),border_radius=14)

    band_top = 10
    band_width = WIDTH * 0.87
    band_height = 190

    band_x = (WIDTH - band_width) // 2

    band_rect = pygame.Rect(band_x,band_top,band_width,band_height)

    pygame.draw.arc(screen,(0,170,255),band_rect,0,math.pi,8)


def draw_microphone():

    head_x = WIDTH // 2
    head_y = eye_y + eye_height + 10

    angle = math.radians(135)

    handle_length = 80
    head_radius = 16

    end_x = head_x + handle_length * math.cos(angle)
    end_y = head_y + handle_length * math.sin(angle)

    # handle
    pygame.draw.line(
        screen,
        (200,200,200),
        (head_x, head_y),
        (end_x, end_y),
        12
    )

    # mic head outer
    pygame.draw.circle(
        screen,
        (130,130,130),
        (head_x, head_y),
        head_radius
    )

    # mic grille
    pygame.draw.circle(
        screen,
        (80,80,80),
        (head_x, head_y),
        head_radius-5
    )

    # highlight
    pygame.draw.circle(
        screen,
        (180,180,180),
        (head_x-4, head_y-4),
        4
    )
# ---------------- MAIN LOOP ----------------
running = True

while running:

    clock.tick(60)
    screen.fill(BLACK)

    if command_queue:
        handle_command(command_queue)
        command_queue = None

    # ---------- EVENTS ----------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            last_active_time = pygame.time.get_ticks()

            if current_state == "SLEEP":
                current_state = "IDLE"

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_a:
                current_state = "ALARM"
                alarm_start_time = pygame.time.get_ticks()

            if event.key == pygame.K_i:
                current_state = "IDLE"

            if event.key == pygame.K_m:
                play_song("Dhurandhar official song")

    # ---------- DELETE SONG AFTER PLAY ----------
    if current_song_file:
        if not pygame.mixer.music.get_busy():
            try:
                os.remove(current_song_file)
                print("Song deleted")
            except:
                pass
            current_song_file = None
            current_state = "IDLE"

    # ---------- REAL CLOCK ALARM ----------
    now = datetime.now(ist)
    today_date = now.date()

    if last_checked_date != today_date:
        alarm_today_triggered = False
        last_checked_date = today_date

    if (now.hour == alarm_hour and
        now.minute == alarm_minute and
        not alarm_today_triggered):

        current_state = "ALARM"
        alarm_start_time = pygame.time.get_ticks()
        alarm_today_triggered = True

    # ---------- ALARM SOUND ----------
    if current_state == "ALARM" and not alarm_playing:
        alarm_sound.play(-1)
        alarm_playing = True

    if current_state != "ALARM" and alarm_playing:
        alarm_sound.stop()
        alarm_playing = False

    # ---------- AUTO STOP ALARM ----------
    if current_state == "ALARM":
        elapsed_alarm = (pygame.time.get_ticks() - alarm_start_time)/1000
        if elapsed_alarm >= alarm_duration_seconds:
            current_state = "IDLE"

    # ---------- AUTO SLEEP ----------
    if current_state == "IDLE":
        idle_elapsed = (pygame.time.get_ticks()-last_active_time)/1000
        if idle_elapsed >= sleep_delay_seconds:
            current_state = "SLEEP"

    # ---------- MIC WAKE ----------
    if current_state == "SLEEP":
        if mic_volume > THRESHOLD:
            current_state = "IDLE"
            last_active_time = pygame.time.get_ticks()

    # ---------- LISTENING ----------
    if current_state not in ["ALARM","SLEEP","PLAYING"]:

        if mic_volume > THRESHOLD:
            current_state = "LISTENING"
            last_sound_time = pygame.time.get_ticks()

        if current_state == "LISTENING":
            if pygame.time.get_ticks()-last_sound_time > listening_timeout:
                current_state = "IDLE"

    # ---------- SHAKE EFFECT ----------
    shake_offset = 0

    if current_state == "ALARM":

        elapsed = (pygame.time.get_ticks() - alarm_start_time)/1000

        if elapsed < 2:
            shake_offset = 0
        elif elapsed < 5:
            shake_offset = math.sin(pygame.time.get_ticks()*0.04)*4
        else:
            shake_offset = math.sin(pygame.time.get_ticks()*0.08)*8

    # ---------- BLINK ----------
    blink_timer += 1

    if (not blinking and
        blink_timer > next_blink and
        current_state not in ["ALARM","SLEEP","PLAYING"]):

        blinking = True
        blink_timer = 0

    if blinking:

        progress = blink_timer/blink_duration
        eased = 0.5 - 0.5*math.cos(progress*math.pi)

        lid_height = eye_height * eased

        if blink_timer > blink_duration:
            blinking = False
            blink_timer = 0

            if random.random() < 0.2:
                next_blink = random.randint(60,120)
            else:
                next_blink = random.randint(360,600)

    else:
        lid_height = 0

    # ---------- MUSIC NOTE ANIMATION ----------
    if current_state == "PLAYING":

        note_x += 0.6
        note_y -= 0.6
        note_size += 0.03

        if note_y < -20:

            note_x = WIDTH//2 + random.randint(-30,30)
            note_y = eye_y - 10
            note_size = 22

            note_symbol = random.choice(["♪","♫","♬"])

    # ---------- DRAW ----------
    if current_state == "SLEEP":

        arc_rect_left = pygame.Rect(left_eye_x, eye_y+40, eye_width,40)
        arc_rect_right = pygame.Rect(right_eye_x, eye_y+40, eye_width,40)

        pygame.draw.arc(screen,BLUE,arc_rect_left,math.pi,2*math.pi,6)
        pygame.draw.arc(screen,BLUE,arc_rect_right,math.pi,2*math.pi,6)

        font = pygame.font.SysFont(None,int(z_size))
        z_surface = font.render("Z",True,BLUE)

        screen.blit(z_surface,(z_x,z_y))

        z_x += 0.5
        z_y -= 0.5
        z_size += 0.05

        if z_y < -20:
            z_x = right_eye_x + 80
            z_y = eye_y - 10
            z_size = 20

    else:

        if current_state == "LISTENING":
            draw_headphones(shake_offset)

        if current_state == "PLAYING":
            draw_microphone()
            font = pygame.font.SysFont("Segoe UI Symbol", int(note_size))
            note_surface = font.render(note_symbol, True, BLUE)

            screen.blit(note_surface, (note_x, note_y))

        screen.blit(eye_img,(left_eye_x + shake_offset, eye_y))
        screen.blit(eye_img,(right_eye_x + shake_offset, eye_y))

        if blinking:
            pygame.draw.rect(screen,BLACK,(left_eye_x + shake_offset, eye_y, eye_width, lid_height))
            pygame.draw.rect(screen,BLACK,(right_eye_x + shake_offset, eye_y, eye_width, lid_height))

    pygame.display.flip()

stream.stop()
stream.close()

pygame.quit()
sys.exit()