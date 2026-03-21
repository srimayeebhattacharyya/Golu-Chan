import customtkinter as ctk
from voice import recognition

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("420x180")
app.title("Golu Control Panel")

# Title
title = ctk.CTkLabel(app, text="🤖 Golu Controls", font=("Arial", 22))
title.pack(pady=15)

# Center container
button_frame = ctk.CTkFrame(app)
button_frame.pack(expand=True)

mic_state = True

def toggle_mic():
    global mic_state

    mic_state = not mic_state
    recognition.user_muted = not mic_state

    if mic_state:
        mic_button.configure(text="🎤 Mic ON", fg_color="#1f6aa5")
    else:
        mic_button.configure(text="🔇 Mic OFF", fg_color="#c0392b")


def toggle_camera():
    print("Camera toggled (placeholder)")

# Mic button
mic_button = ctk.CTkButton(
    button_frame,
    text="🎤 Mic ON",
    width=140,
    height=50,
    command=toggle_mic
)
mic_button.grid(row=0, column=0, padx=20, pady=20)

# Camera button
camera_button = ctk.CTkButton(
    button_frame,
    text="📷 Camera",
    width=140,
    height=50,
    command=toggle_camera
)
camera_button.grid(row=0, column=1, padx=20, pady=20)

app.mainloop()