import pygame
import sys
import math
import random
from datetime import datetime
import pytz

from voice.speech import speak
from voice.recognition import start_stream, get_command, get_volume
from audio.music import play_song
from commands.handler import handle_command
from voice.speech import speak
from voice import recognition

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

audio_ok = True

try:
    pygame.mixer.init()
except pygame.error as e:
    print("Audio init failed:", e)
    audio_ok = False

WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EMO")

clock = pygame.time.Clock()

BLACK = (0,0,0)
BLUE = (0,170,255)
WHITE = (255,255,255)

eye_img = pygame.image.load("assets/eye.png").convert_alpha()
eye_width, eye_height = eye_img.get_size()

keyboard_icon = pygame.image.load("assets/keyboard.png").convert_alpha()
keyboard_icon = pygame.transform.scale(keyboard_icon, (30,30))

if audio_ok:
    alarm_sound = pygame.mixer.Sound("assets/alarm.wav")
else:
    alarm_sound = None

ist = pytz.timezone("Asia/Kolkata")

current_state = "IDLE"

left_eye_x = 70
right_eye_x = 270
eye_y = 105

blink_timer = 0
blink_duration = random.randint(6,12)
next_blink = random.randint(240,480)
blinking = False

sleep_delay_seconds = 60
last_active_time = pygame.time.get_ticks()

keyboard_button = pygame.Rect(WIDTH-60, HEIGHT-60, 40, 40)
typing_mode = False
typed_text = ""

# Mic / Video toggles (centered)
mic_on = True
video_on = True

mic_on = True
video_on = True

BUTTON_RADIUS = 22

mic_center = (WIDTH//2 - 40, HEIGHT - 40)
video_center = (WIDTH//2 + 40, HEIGHT - 40)

THRESHOLD = 0.01

start_stream()

running = True

while running:

    clock.tick(60)
    screen.fill(BLACK)

    cmd = get_command()

    if cmd:
        handle_command(cmd)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if keyboard_button.collidepoint(pos):
                typing_mode = not typing_mode
            
            mx, my = pygame.mouse.get_pos()

            if (mx-mic_center[0])**2 + (my-mic_center[1])**2 < BUTTON_RADIUS**2:
                mic_on = not mic_on
                recognition.user_muted = not mic_on

            if (mx-video_center[0])**2 + (my-video_center[1])**2 < BUTTON_RADIUS**2:
                video_on = not video_on

        if event.type == pygame.KEYDOWN:

            last_active_time = pygame.time.get_ticks()

            if event.key == pygame.K_ESCAPE:
                running = False

            # if event.key == pygame.K_m:
            #     play_song("Dhurandhar official song")      

            if event.type == pygame.KEYDOWN:

                if typing_mode:

                    if event.key == pygame.K_RETURN:
                        handle_command(typed_text)
                        typed_text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        typed_text = typed_text[:-1]

                    else:
                        typed_text += event.unicode

    if current_state == "IDLE":

        idle_elapsed = (pygame.time.get_ticks()-last_active_time)/1000

        if idle_elapsed >= sleep_delay_seconds:
            current_state = "SLEEP"

    if current_state == "SLEEP":

        if get_volume() > THRESHOLD:
            current_state = "IDLE"
            last_active_time = pygame.time.get_ticks()

    blink_timer += 1

    if not blinking and blink_timer > next_blink:

        blinking = True
        blink_timer = 0

    if blinking:

        progress = blink_timer/blink_duration
        eased = 0.5 - 0.5*math.cos(progress*math.pi)

        lid_height = eye_height * eased

        if blink_timer > blink_duration:

            blinking = False
            blink_timer = 0
            next_blink = random.randint(360,600)

    else:
        lid_height = 0

    screen.blit(eye_img,(left_eye_x,eye_y))
    screen.blit(eye_img,(right_eye_x,eye_y))

    if blinking:

        pygame.draw.rect(screen,BLACK,(left_eye_x,eye_y,eye_width,lid_height))
        pygame.draw.rect(screen,BLACK,(right_eye_x,eye_y,eye_width,lid_height))

    pygame.draw.rect(screen, BLUE, keyboard_button, border_radius=10)

    font = pygame.font.SysFont("Segoe UI Symbol",24)
    icon = font.render("⌨", True, BLACK)

    screen.blit(icon, (keyboard_button.x+8, keyboard_button.y+8))

    # draw keyboard button
    pygame.draw.rect(screen, WHITE, keyboard_button, border_radius=10)

    screen.blit(keyboard_icon, (keyboard_button.x+5, keyboard_button.y+5))

    # draw typing box
    if typing_mode:

        input_box = pygame.Rect(20, HEIGHT-60, WIDTH-100, 40)
        pygame.draw.rect(screen, BLUE, input_box, 2, border_radius=10)

        font = pygame.font.SysFont(None, 28)
        text_surface = font.render(typed_text, True, BLUE)

        screen.blit(text_surface, (input_box.x+10, input_box.y+8))

    # --- MIC BUTTON ---
    if mic_on:
        pygame.draw.circle(screen, (50,50,50), mic_center, BUTTON_RADIUS)
    else:
        pygame.draw.circle(screen, (200,0,0), mic_center, BUTTON_RADIUS)

    # mic icon
    pygame.draw.circle(screen, WHITE, mic_center, 6)
    pygame.draw.rect(screen, WHITE, (mic_center[0]-2, mic_center[1]-12, 4, 12))

    # strike when muted
    if not mic_on:
        pygame.draw.line(screen, WHITE,
                        (mic_center[0]-12, mic_center[1]-12),
                        (mic_center[0]+12, mic_center[1]+12), 3)


    # --- VIDEO BUTTON ---
    if video_on:
        pygame.draw.circle(screen, (50,50,50), video_center, BUTTON_RADIUS)
    else:
        pygame.draw.circle(screen, (200,0,0), video_center, BUTTON_RADIUS)

    # camera icon
    pygame.draw.rect(screen, WHITE,
                    (video_center[0]-8, video_center[1]-6, 16, 12), 2)

    pygame.draw.polygon(screen, WHITE, [
        (video_center[0]+8, video_center[1]-4),
        (video_center[0]+14, video_center[1]),
        (video_center[0]+8, video_center[1]+4)
    ], 2)

    # strike when off
    if not video_on:
        pygame.draw.line(screen, WHITE,
                        (video_center[0]-12, video_center[1]-12),
                        (video_center[0]+12, video_center[1]+12), 3)
    pygame.display.flip()

pygame.quit()
sys.exit()