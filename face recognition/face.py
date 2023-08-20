import cv2
from deepface import DeepFace
import subprocess
import tkinter as tk
from tkinter import Button, Frame
from tkinter import ttk  # Importing ttk for Treeview
import threading
import json
import os

process_time_spent = {}
cap = None

# Load previous ratings from file
def load_ratings():
    if os.path.exists("ratings.txt"):
        with open("ratings.txt", "r") as f:
            return json.load(f)
    return {}

# Save ratings to file
def save_ratings(ratings):
    with open("ratings.txt", "w") as f:
        json.dump(ratings, f)

# Update the rating for a given process
def set_rating(process, rating):
    process = process.replace(' [fun]', '')
    process = process.replace(' [productive]', '')
    process = process.replace(' [neutral]', '')
    ratings[process] = rating
    save_ratings(ratings)
    update_emotion_stat_labels()  # Refresh the display

# Add the rating next to the process name when displaying in the tree
def format_process_name(process):
    rating = ratings.get(process)
    if rating:
        return f"{process} [{rating}]"
    return process
def get_active_window_mac():
    script = '''
        tell application "System Events"
            name of application processes whose frontmost is true
        end tell
    '''
    return subprocess.check_output(["osascript", "-e", script]).strip().decode('utf-8')

def update_emotion_stat_labels():
    for process, emotions in process_emotion_counts.items():
        total_frames = sum(emotions.values())
        if process not in tree_process_ids:
            tree_process_ids[process] = tree.insert("", "end", values=(format_process_name(process),)) 
        else:
            # Update the process name in case the rating changed
            tree.item(tree_process_ids[process], values=(format_process_name(process),) + tuple(emotions[e] for e in emotions))

        for emotion, count in emotions.items():
            if total_frames == 0:
                percentage = 0
            else:
                percentage = (count / total_frames) * 100
            emotion_string = f"{percentage:.2f}%"
            tree.set(tree_process_ids[process], emotion, emotion_string)

def capture_process():
    global running
    while running:
        process_name = get_active_window_mac()
        process_time_spent[process_name] = process_time_spent.get(process_name, 0) + 1
        if process_name not in process_emotion_counts:
            print("novi process " + process_name)
            process_emotion_counts[process_name] = {"happy": 0, "sad": 0, "angry": 0, "neutral": 0, "fear": 0, "disgust": 0, "surprise": 0}
            update_emotion_stat_labels()
            window.update()

def capture_video():
    global running
    while running:
        ret, frame = cap.read()
        if not ret:
            continue 
        
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]["dominant_emotion"]
        process_name = get_active_window_mac()

        # Update the emotion counts for the process
        if process_name not in process_emotion_counts:
            process_emotion_counts[process_name] = {"happy": 0, "sad": 0, "angry": 0, "neutral": 0, "fear": 0, "disgust": 0, "surprise": 0}
        
        if dominant_emotion in process_emotion_counts[process_name]:
            process_emotion_counts[process_name][dominant_emotion] += 1

        update_emotion_stat_labels()
        window.update()
        process_time_spent[process_name] = process_time_spent.get(process_name, 0) + 1

def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def display_summary():
    summary_window = tk.Toplevel(window)
    summary_window.title("Time Summary")

    for rating, label in [("productive", "Productive"), ("fun", "Fun"), ("neutral", "Neutral")]:
        # Use a generator comprehension to ensure only the processes present in both dictionaries are considered.
        total_seconds = sum(process_time_spent[process] for process, process_rating in ratings.items() if process_rating == rating and process in process_time_spent)
        
        h, m, s = seconds_to_hms(total_seconds)
        
        processes = [process for process, process_rating in ratings.items() if process_rating == rating and process in process_time_spent]
        
        # Check if there are any processes for the current rating
        if processes:
            processes_str = ", ".join(processes)
            label_text = f"Time spent being {label}: {h} hours {m} minutes {s} seconds\nApps: {processes_str}\n\n"
            tk.Label(summary_window, text=label_text).pack()
        else:
            label_text = f"No time recorded for being {label}\n\n"
            tk.Label(summary_window, text=label_text).pack()

    summary_window.mainloop()

def start_camera():
    global running, cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Disable start buttons and enable stop button
    start_button.config(state=tk.DISABLED)
    start_process_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    
    running = True
    threading.Thread(target=capture_video).start()

def start_process():
    global running
    running = True
    
    # Disable start buttons and enable stop button
    start_button.config(state=tk.DISABLED)
    start_process_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    threading.Thread(target=capture_process).start()

def stop_camera():
    global running, cap
    running = False
    if cap and cap.isOpened():
        cap.release()
    
    # Re-enable start buttons and disable stop button
    start_button.config(state=tk.NORMAL)
    start_process_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Emotion Detection")

# Buttons at the top
button_frame = Frame(window)
button_frame.pack(pady=20)

start_button = Button(button_frame, text="Start with camera", command=start_camera)
start_button.pack(padx=10, side=tk.LEFT)

start_process_button = Button(button_frame, text="Start no camera", command=start_process)
start_process_button.pack(padx=10, side=tk.LEFT)

stop_button = Button(button_frame, text="Stop", command=stop_camera, state=tk.DISABLED)
stop_button.pack(padx=10, side=tk.LEFT)

summary_button = Button(button_frame, text="Display Summary", command=display_summary)
summary_button.pack(padx=10, side=tk.LEFT)

# Stats frame
stats_frame = Frame(window)
stats_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(stats_frame, columns=("process", "happy", "sad", "angry", "neutral", "fear", "disgust", "surprise"), show="headings")
tree.heading("process", text="Process")
tree.heading("happy", text="Happy")
tree.heading("sad", text="Sad")
tree.heading("angry", text="Angry")
tree.heading("neutral", text="Neutral")
tree.heading("fear", text="Fear")
tree.heading("disgust", text="Disgust")
tree.heading("surprise", text="Surprise")

# Adjusting column width for better visibility (feel free to adjust as needed)
tree.column("process", width=150)
for emotion in ["happy", "sad", "angry", "neutral", "fear", "disgust", "surprise"]:
    tree.column(emotion, width=100)

tree.pack(fill=tk.BOTH, expand=True)

process_emotion_counts = {}
tree_process_ids = {}  # Storing Treeview IDs for each process

menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Rate as Fun", command=lambda: set_rating(tree.item(tree.selection())["values"][0], "fun"))
menu.add_command(label="Rate as Neutral", command=lambda: set_rating(tree.item(tree.selection())["values"][0], "neutral"))
menu.add_command(label="Rate as Productive", command=lambda: set_rating(tree.item(tree.selection())["values"][0], "productive"))

def on_right_click(event):
    # Select the row under the mouse pointer
    tree.selection_set(tree.identify_row(event.y))
    
    if tree.selection():
        menu.post(event.x_root, event.y_root)


tree.bind("<Button-2>", on_right_click)
tree.bind("<Control-Button-1>", on_right_click)

ratings = load_ratings()  # Load ratings at the start of the app

window.mainloop()
