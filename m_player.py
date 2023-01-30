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
if platform.system() == "Windows": # Windows path
    rootpath = os.path.join(os.path.expanduser("%USERPROFILE%"), "Music")
elif platform.system() == "Darwin":  # Mac path, I think
    try:
        rootpath = os.path.join(os.path.expanduser("~"), "Music")
    except:
        print("Weird Fucking system Bro")
elif platform.system() == "Linux":  # Linux path
    rootpath = os.path.join(os.path.expanduser("~"), "Music")
pattern = "*.mp3"

prev_img = tk.PhotoImage(file="Docs/assets/prev_img.png")
stop_img = tk.PhotoImage(file="Docs/assets/stop_img.png")
play_img = tk.PhotoImage(file="Docs/assets/play_img.png")
pause_img = tk.PhotoImage(file="Docs/assets/pause_img.png")
next_img = tk.PhotoImage(file="Docs/assets/next_img.png")

mixer.init()

#This function is the Blood of the music player
#It plays the selected music, and if pressed again while playing
#It plays the music from the start
def select(): 
    text_d=listBox.get("anchor")
    text_d = text_d.rsplit(".", 1)[0]
    label.config(text=text_d)
    mixer.music.load(rootpath + "/" + listBox.get("anchor"))
    mixer.music.play()
    mixer.music.set_volume(Volumelevel.get() /100)

#As the name suggests, this function stops the music from playing
#And it clears the name of the previous song
def stop():
    mixer.music.fadeout(1250)
    listBox.select_clear("active")
    label.config(text="")

#This function plays the next song of the listed songs
def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    next_song_name = next_song_name.rsplit(".", 1)[0]
    label.config(text=next_song_name)
    next_song_name = listBox.get(next_song)

    mixer.music.load(rootpath + "/" + next_song_name)
    mixer.music.play()
    mixer.music.set_volume(Volumelevel.get() /100)

    listBox.select_clear(0, "end")
    listBox.activate(next_song)
    listBox.select_set(next_song)

#This function plays the previous song of the listed songs
def play_prev():
    prev_song = listBox.curselection()
    prev_song = prev_song[0] - 1
    prev_song_name = listBox.get(prev_song)
    prev_song_name = prev_song_name.rsplit(".", 1)[0]
    label.config(text=prev_song_name)
    prev_song_name = listBox.get(prev_song)

    mixer.music.load(rootpath + "/" + prev_song_name)
    mixer.music.play()
    mixer.music.set_volume(Volumelevel.get() /100)

    listBox.select_clear(0, "end")
    listBox.activate(prev_song)
    listBox.select_set(prev_song)

#This function pauses the music and when pressed again
#Resumes the music from where it was paused
def pause_song():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        pauseButton["text"] = "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"

#This function is still a work in progress
#But i intend to make it possible to download music
#To add it to the list
def add_song():
    filepath = filedialog.askopenfilename()
    shutil.copy2(filepath, rootpath)

#This function is also a work in progress
#I intend to make it a slider that controls the volume
def volume(x):
    mixer.music.set_volume(Volumelevel.get() /100)
    curent_volume = mixer.music.get_volume()


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

#adds the prev Button to the music player
prevButton = tk.Button(
    canvas,
    text="Prev",
    image=prev_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=play_prev,
)
prevButton.pack(pady=15, in_=top, side="left")

#adds the stop Button to the music player
stopButton = tk.Button(
    canvas,
    text="Stop",
    image=stop_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=stop,
)
stopButton.pack(pady=15, in_=top, side="left")

#adds the play Button to the music player
playButton = tk.Button(
    canvas,
    text="Play",
    image=play_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=select,
)
playButton.pack(pady=15, in_=top, side="left")

#adds the pause Button to the music player
pauseButton = tk.Button(
    canvas,
    text="Pause",
    image=pause_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=pause_song,
)
pauseButton.pack(pady=15, in_=top, side="left")

#adds the next Button to the music player
nextButton = tk.Button(
    canvas,
    text="Next",
    image=next_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=play_next,
)
nextButton.pack(pady=15, in_=top, side="left")

#adds the volume slider
Volumelevel = tk.Scale(canvas,from_= 0, to_=100,
                        orient= tk.HORIZONTAL,
                        bg="#6433d6",
                        borderwidth=0,
                        resolution=1,
                        length=225,
                        command=volume
                        )
Volumelevel.set(50) #puts defalt value of slider to 50
Volumelevel.pack(pady=15)
#adds the add Button to the music player
addButton = tk.Button(
    canvas,
    text="Add song",
    bg="#6433d6",
    borderwidth=0,
    command=add_song,
)
addButton.pack(pady=15, side="left")

#Generates the list of song
#Reads the file name and format(mp3)
#Inserts the songs with the correct format to the list of songs
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert("end", filename)

#Loops the code so the Music Player can function                  
canvas.mainloop()
