import random
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
    
    
audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma', '.aac', '.alac', '.aiff', '.opus']

def is_audio_file(file):
    return os.path.splitext(file)[1] in audio_extensions

def load_songs():
    for root, dirnames, filenames in os.walk(rootpath):
        for filename in filenames:
            if is_audio_file(filename):
                listBox.insert(tk.END, filename)

prev_img = tk.PhotoImage(file="Docs/assets/prev_img.png")
stop_img = tk.PhotoImage(file="Docs/assets/stop_img.png")
play_img = tk.PhotoImage(file="Docs/assets/play_img.png")
pause_img = tk.PhotoImage(file="Docs/assets/pause_img.png")
next_img = tk.PhotoImage(file="Docs/assets/next_img.png")
shuffle_img = tk.PhotoImage(file="Docs/assets/shuffle_img.png")
repeat_img = tk.PhotoImage(file="Docs/assets/repeat_img.png")
wipe_img = tk.PhotoImage(file="Docs/assets/wipe_img.png")
load_img = tk.PhotoImage(file="Docs/assets/load_img.png")

mixer.init()

#This function is the Blood of the music player
#It plays the selected music, and if pressed again while playing
#It plays the music from the start
def select(): 
    global playlist
    if shuffleButton['text'] == 'Shuffle':
        selected_song = rootpath + '/' + listBox.get("anchor")
    else:
        if not playlist:
            playlist = list(listBox.get(0, tk.END))
        selected_song = rootpath + '/' + playlist.pop(0)
        listBox.delete(0)
        listBox.insert(tk.END, *playlist)

    mixer.music.load(selected_song)
    mixer.music.play()
    mixer.music.set_volume(Volumelevel.get() / 100)
    label.config(text=listBox.get("anchor").rsplit(".", 1)[0])

#As the name suggests, this function stops the music from playing
#And it clears the name of the previous song
def stop():
    mixer.music.fadeout(1250)
    listBox.select_clear("active")
    label.config(text="")

def clear_playlist():
    stop()
    listBox.delete(0, tk.END)
    
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

playlist = []

def shuffle_playlist():
    global playlist
    playlist = list(listBox.get(0, tk.END))
    random.shuffle(playlist)
    listBox.delete(0, tk.END)
    for song in playlist:
        listBox.insert(tk.END, song)

def toggle_repeat():
    if mixer.music.get_busy():
        mixer.music.stop()
    mixer.music.play(-1 if mixer.music.get_volume() else 0, 0)
    

#This function pauses the music and when pressed again
#Resumes the music from where it was paused
def pause_song():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        pauseButton["text"] = "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"

def add_song():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg;*.flac;*.m4a;*.wma;*.aac;*.alac;*.aiff;*.opus")])
    if file_path:
        # Check if the selected file is an audio file
        if not is_audio_file(file_path):
            messagebox.showerror("Error", "Selected file is not an audio file.")
            return
        # Add the selected file to the listbox
        filename = os.path.basename(file_path)
        listBox.insert(tk.END, filename)


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


clearButton = tk.Button(
    canvas,
    text="Clear Playlist",
    image=wipe_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=clear_playlist,
)
clearButton.pack(pady=15, in_=top, side="left")


loadButton = tk.Button(
    canvas,
    text="Load Music",
    image=load_img,
    bg="#6433d6",
    borderwidth=0,
    height= 70,
    command=load_songs,
)
loadButton.pack(pady=15, in_=top, side="left")


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

shuffleButton = tk.Button(
    canvas,
    text="Shuffle",
    image=shuffle_img,
    bg="#6433d6",
    borderwidth=0,
    height=70,
    command=shuffle_playlist,
)
shuffleButton.pack(pady=15, in_=top, side="left")

repeatButton = tk.Button(
    canvas,
    text="Repeat",
    image=repeat_img,
    bg="#6433d6",
    borderwidth=0,
    height=70,
    command=toggle_repeat,
)
repeatButton.pack(pady=15, in_=top, side="left")

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
load_songs()

#Loops the code so the Music Player can function                  
canvas.mainloop()
