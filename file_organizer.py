#!/usr/local/bin/python3
import os
from pathlib import Path
import shutil 
import tkinter as tk
from tkinter import filedialog, messagebox

audio = (".3ga", ".aac", ".ac3", ".aif", ".aiff",
         ".alac", ".amr", ".ape", ".au", ".dss",
         ".flac", ".flv", ".m4a", ".m4b", ".m4p",
         ".mp3", ".mpga", ".ogg", ".oga", ".mogg",
         ".opus", ".qcp", ".tta", ".voc", ".wav",
         ".wma", ".wv", ".aiff", ".m3u", ".mp2", 
         ".spx")

video = (".webm", ".MTS", ".M2TS", ".TS", ".mov",
         ".mp4", ".m4p", ".m4v", ".mxf", ".mkv", 
         ".avi", ".flv", ".wmv", ".3gp", ".asf", 
         ".f4v", ".mpg", ".mpeg", ".rm", ".vob")

img = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png",
       ".gif", ".webp", ".svg", ".apng", ".avif", ".bmp", 
       ".tif", ".tiff", ".ico", ".jfif", ".heic", ".raw")

document = (".pdf", ".doc", ".docx", ".xls", ".xlsx", 
            ".ppt", ".pptx", ".odt", ".ods", ".odp", 
            ".txt", ".rtf", ".csv", ".xml", ".html", 
            ".htm", ".tex", ".md", ".epub", ".mobi", 
            ".azw", ".azw3", ".pages", ".key", ".numbers", 
            ".ps", ".psd", ".xd", ".ai", ".indd", ".dxf", 
            ".dwg", ".sketch")

zip_files = (".zip", ".rar", ".7z", ".tar", ".gz", 
            ".bz2", ".iso", ".jar", ".war", ".cab", 
            ".s7z", ".ace", ".z")

code = (".py", ".js", ".java", ".cpp", ".c", ".cs", 
        ".html", ".css", ".php", ".rb", ".swift", 
        ".go", ".sh", ".bat")

database = (".sql", ".db", ".dbf", ".mdb", ".accdb", 
            ".sqlite", ".sav", ".log", ".dat")

font = (".ttf", ".otf", ".woff", ".woff2", ".eot", 
        ".fon")

executable = (".exe", ".msi", ".apk", ".dmg", ".bin", 
              ".out", ".run")

def is_audio(file):
    return os.path.splitext(file)[1] in audio

def is_video(file):
    return os.path.splitext(file)[1] in video

def is_image(file):
    return os.path.splitext(file)[1] in img

def is_screenshot(file):
    name, ext = os.path.splitext(file)
    return (ext in img) and "screenshot" in name.lower()

def is_document(file):
    return os.path.splitext(file)[1] in document

def is_zip(file):
    return os.path.splitext(file)[1] in zip_files

def is_code(file):
    return os.path.splitext(file)[1] in code

def is_database(file):
    return os.path.splitext(file)[1] in database

def is_font(file):
    return os.path.splitext(file)[1] in font

def is_executable(file):
    return os.path.splitext(file)[1] in executable


os.chdir('/Users/ariel/Downloads')

base_path = "/Users/ariel/Documents"
audio_path = os.path.join(base_path, "audio")
video_path = os.path.join(base_path, "video")
image_path = os.path.join(base_path, "images")
screenshot_path = os.path.join(base_path, "screenshots")
document_path = os.path.join(base_path, "docuemnts")
zip_path = os.path.join(base_path, "zips")
code_path = os.path.join(base_path, "codes")
font_path = os.path.join(base_path, "fonts")
executable_path = os.path.join(base_path, "executables")
database_path = os.path.join(base_path, "database")

for folder_path in [audio_path, video_path, image_path, screenshot_path, document_path, 
                    zip_path, code_path, font_path, executable_path]:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_new_name(base_path, filename):
    """
    Generate a new filename if a file with the same name already exists.
    """
    new_name = filename
    counter = 1
    while os.path.exists(os.path.join(base_path, new_name)):
        name, extension = os.path.splitext(filename)
        new_name = f"{name}_{counter}{extension}"
        counter += 1
    return new_name
def organize_files():
    for file in os.listdir():
        if file.startswith(".") or os.path.isdir(file):
            continue
        
        destination_path = None

        if is_audio(file):
            destination_path = audio_path
        elif is_video(file):
            destination_path = video_path
        elif is_image(file):
            if is_screenshot(file):
                destination_path = screenshot_path
            else:
                destination_path = image_path
        elif is_document(file):
            destination_path = document_path
        elif is_zip(file):
            destination_path = zip_path
        elif is_database(file):
            destination_path = database_path
        elif is_code(file):
            destination_path = code_path
        elif is_executable(file):
            destination_path = executable_path
        elif is_font(file):
            destination_path = font_path
        else:
            destination_path = base_path
        
        # Check if file with same name exists in the destination and get a new name if necessary
        new_filename = get_new_name(destination_path, file)
        shutil.move(file, os.path.join(destination_path, new_filename))
        messagebox.showinfo("Success", "Files have been organized!")
        
def set_directory():
    directory = filedialog.askdirectory()
    if directory:
        os.chdir(directory)
        # Update the label with the selected directory
        selected_directory_label.config(text=directory)
    
# GUI Initialization
root = tk.Tk()
root.title("File Organizer")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_set_directory = tk.Button(frame, text="Choose Directory", command=set_directory)
btn_set_directory.pack(pady=5)

# Label to display the selected directory
selected_directory_label = tk.Label(frame, text="No directory selected", wraplength=300)
selected_directory_label.pack(pady=5)

btn_organize = tk.Button(frame, text="Organize Files", command=organize_files)
btn_organize.pack(pady=5)

root.mainloop()





