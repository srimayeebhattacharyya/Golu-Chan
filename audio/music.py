import pygame
import yt_dlp
import uuid

def play_song(song):

    if not pygame.mixer.get_init():
        pygame.mixer.init()

def download_song(song_name):

    unique_id = uuid.uuid4().hex
    filename = f"song_{unique_id}"

    ydl_opts = {
        "format":"bestaudio/best",
        "outtmpl":f"{filename}.%(ext)s",
        "quiet":True,
        "postprocessors":[{
            "key":"FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":"192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{song_name}"])

    return f"{filename}.mp3"

def play_song(song_name):

    file = download_song(song_name)

    pygame.mixer.music.load(file)
    pygame.mixer.music.play()