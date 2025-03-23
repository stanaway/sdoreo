import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_var.set(folder_selected)

def extract_camera_metadata(file_path):
    try:
        result = subprocess.run([
            "exiftool", "-Make", "-Model", "-s", file_path
        ], capture_output=True, text=True)
        
        make, model = "", ""
        for line in result.stdout.split("\n"):
            if line.startswith("Make:"):
                make = line.split("Make:")[1].strip()
            elif line.startswith("Model:"):
                model = line.split("Model:")[1].strip()
        
        return f"{make} {model}".strip() or "Unknown"
    except Exception as e:
        return "Unknown"

def organize_files():
    folder_path = entry_var.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder.")
        return
    
    for file in os.listdir(folder_path):
        if file.lower().endswith((".jpg", ".avi", ".mp4")):
            file_path = os.path.join(folder_path, file)
            camera_name = extract_camera_metadata(file_path)
            camera_folder = os.path.join(folder_path, camera_name)
            os.makedirs(camera_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(camera_folder, file))
    
    messagebox.showinfo("Success", "Files sorted successfully!")

# GUI Setup
root = tk.Tk()
root.title("Metadata Sorter")
root.configure(bg="#1b3d21")
root.geometry("400x200")

tk.Label(root, text="Select Folder:", bg="#1b3d21", fg="white").pack(pady=5)
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, width=40)
entry.pack(pady=5)

tk.Button(root, text="Browse", command=select_folder).pack(pady=5)
tk.Button(root, text="Sort Files", command=organize_files).pack(pady=10)

root.mainloop()
