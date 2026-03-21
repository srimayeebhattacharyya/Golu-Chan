from voice.speech import speak
from audio.music import play_song
import pygame
import threading
from ai.brain import get_ai_response, solve_newton

def run_ai(text):
    try:
        print("AI thread started")
        reply = get_ai_response(text)
        print("AI reply:", reply)
        speak(reply)
    except Exception as e:
        print("Thread error:", e)


def handle_command(text):

    print("Command received:", text)

    text = text.lower()

    # 🔥 MUSIC
    if "play" in text:
        song = text.replace("play", "").strip()

        if song == "":
            speak("Which song should I play?")
        else:
            play_song(song)

    elif "stop" in text:
        pygame.mixer.music.stop()
        speak("Stopping the music")

    # 🔥 TIME
    elif "time" in text:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    # 🔥 NEWTON API (MATH / CALCULUS)

    elif "derivative" in text or "derive" in text:
        expr = text

        # clean text better
        expr = expr.replace("derivative of", "")
        expr = expr.replace("derivative", "")
        expr = expr.replace("derive", "")
        expr = expr.strip()

        result = solve_newton("derive", expr)

        if result:
            speak(f"The derivative is {result}")
        else:
            speak("I couldn't compute that 😅")

    elif "integrate" in text:
        expr = text.replace("integrate", "").strip()
        result = solve_newton("integrate", expr)

        if result:
            speak(f"The integral is {result}")
        else:
            speak("I couldn't compute that 😅")

    elif "factor" in text:
        expr = text.replace("factor", "").strip()
        result = solve_newton("factor", expr)

        if result:
            speak(f"The factors are {result}")
        else:
            speak("I couldn't compute that 😅")

    elif "simplify" in text:
        expr = text.replace("simplify", "").strip()
        result = solve_newton("simplify", expr)

        if result:
            speak(f"The simplified result is {result}")
        else:
            speak("I couldn't compute that 😅")

    elif any(word in text for word in ["sin", "cos", "tan", "log", "^"]):
        expr = text

        expr = expr.replace("what is", "")
        expr = expr.replace("calculate", "")
        expr = expr.strip()

        result = solve_newton("simplify", expr)

        if result:
            speak(f"The answer is {result}")
        else:
            threading.Thread(target=run_ai, args=(text,), daemon=True).start()
            
    # 🔥 AI FALLBACK (main brain)
    else:
        threading.Thread(target=run_ai, args=(text,), daemon=True).start()