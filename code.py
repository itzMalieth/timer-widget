import tkinter as tk
from datetime import datetime
import json
import os

# === Load Config ===
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError("config.json not found! Please create it with exam_date.")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

exam_date = datetime.strptime(config["exam_date"], "%Y-%m-%d %H:%M:%S")

# === Countdown Logic ===
def update_countdown():
    now = datetime.now()
    remaining = exam_date - now
    if remaining.total_seconds() > 0:
        days = remaining.days
        h, r = divmod(remaining.seconds, 3600)
        m, s = divmod(r, 60)
        text.set(f"⏳ {days}d {h:02}:{m:02}:{s:02}")
        root.after(1000, update_countdown)
    else:
        text.set("⏳ Exam Started!")

# === Dragging ===
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

# === GUI ===
root = tk.Tk()
root.overrideredirect(True)           # borderless
root.wm_attributes("-topmost", True)  # always on top
root.wm_attributes("-alpha", 0.9)     # slight transparency
root.configure(bg="black")

# Frame inside root
frame = tk.Frame(root, bg="black", bd=1, relief="solid")
frame.pack()

text = tk.StringVar()
label = tk.Label(
    frame,
    textvariable=text,
    font=("Arial", 12, "bold"),
    fg="#00ffcc",
    bg="black"
)
label.pack(padx=4, pady=2)

# Bind dragging
for widget in (frame, label):
    widget.bind("<Button-1>", start_move)
    widget.bind("<B1-Motion>", do_move)

# === Right-click to close ===
root.bind("<Button-3>", lambda e: root.destroy())

# (Optional: Esc also closes)
root.bind("<Escape>", lambda e: root.destroy())

update_countdown()
root.mainloop()
