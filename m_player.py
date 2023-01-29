import fnmatch
import os
import platform
import shutil
import tkinter as tk
from tkinter import filedialog

from pygame import mixer

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x800")
canvas.config(bg="#6433d6")
if platform.system() == "Windows":
    rootpath = "%USERPROFILE%/Music"  # Windows path
elif platform.system() == "Darwin":
    try:
        rootpath = "~/Music"  # Mac path, I think
    except:
        print("Weird Fucking system Bro")
elif platform.system() == "Linux":
    rootpath = "~/Music"  # Linux path
pattern = "*.mp3"

prev_img = tk.PhotoImage(file="Docs/assets/prev_img.png")
stop_img = tk.PhotoImage(file="Docs/assets/stop_img.png")
play_img = tk.PhotoImage(file="Docs/assets/play_img.png")
pause_img = tk.PhotoImage(file="Docs/assets/pause_img.png")
next_img = tk.PhotoImage(file="Docs/assets/next_img.png")

mixer.init()


def select():
    label.config(text=listBox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
    mixer.music.play()


def stop():
    mixer.music.stop()
    listBox.select_clear("active")


def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text=next_song_name)

    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()

    listBox.select_clear(0, "end")
    listBox.activate(next_song)
    listBox.select_set(next_song)


def play_prev():
    prev_song = listBox.curselection()
    prev_song = prev_song[0] - 1
    prev_song_name = listBox.get(prev_song)
    label.config(text=prev_song_name)

    mixer.music.load(rootpath + "\\" + prev_song_name)
    mixer.music.play()

    listBox.select_clear(0, "end")
    listBox.activate(prev_song)
    listBox.select_set(prev_song)


def pause_song():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        pauseButton["text"] = "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"


def add_song():
    filepath = filedialog.askopenfilename()
    shutil.copy2(filepath, rootpath)


def volume():
    pass


listBox = tk.Listbox(
    canvas, fg="cyan", bg="black", width=100, font=("ds-digital", 15)
)
listBox.pack(padx=15, pady=15)

label = tk.Label(
    canvas, text="", bg="#6433d6", fg="yellow", font=("cantarell", 18)
)
label.pack(pady=15)

top = tk.Frame(canvas, bg="#6433d6")
top.pack(padx=10, pady=5, anchor="center")

prevButton = tk.Button(
    canvas,
    text="Prev",
    image=prev_img,
    bg="#6433d6",
    borderwidth=0,
    command=play_prev,
)
prevButton.pack(pady=15, in_=top, side="left")

stopButton = tk.Button(
    canvas,
    text="Stop",
    image=stop_img,
    bg="#6433d6",
    borderwidth=0,
    command=stop,
)
stopButton.pack(pady=15, in_=top, side="left")

playButton = tk.Button(
    canvas,
    text="Play",
    image=play_img,
    bg="#6433d6",
    borderwidth=0,
    command=select,
)
playButton.pack(pady=15, in_=top, side="left")

pauseButton = tk.Button(
    canvas,
    text="Pause",
    image=pause_img,
    bg="#6433d6",
    borderwidth=0,
    command=pause_song,
)
pauseButton.pack(pady=15, in_=top, side="left")

nextButton = tk.Button(
    canvas,
    text="Next",
    image=next_img,
    bg="#6433d6",
    borderwidth=0,
    command=play_next,
)
nextButton.pack(pady=15, in_=top, side="left")

addButton = tk.Button(
    canvas,
    text="Add song",
    bg="#6433d6",
    borderwidth=0,
    command=add_song,
)
addButton.pack(pady=15, side="left")

for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert("end", filename)

canvas.mainloop()
