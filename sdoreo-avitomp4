import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Function to convert AVI to MP4 using H.265 (HEVC)
def convert_videos(folder):
    avi_files = [f for f in os.listdir(folder) if f.lower().endswith(".avi")]

    if not avi_files:
        messagebox.showinfo("No AVI Files", "No AVI files found in the selected folder.")
        return

    progress_bar["maximum"] = len(avi_files)
    progress_bar["value"] = 0

    for index, avi_file in enumerate(avi_files, 1):
        input_path = os.path.join(folder, avi_file)
        output_path = os.path.join(folder, os.path.splitext(avi_file)[0] + ".mp4")

        # FFmpeg command for H.265 encoding (visually identical)
        ffmpeg_command = [
            "ffmpeg", "-i", input_path,
            "-c:v", "libx265", "-preset", "slow", "-crf", "20",
            "-tag:v", "hvc1", "-pix_fmt", "yuv420p",  # Ensures Apple compatibility
            "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart",  # Optimizes for streaming (iCloud playback)
            "-y", output_path
        ]


        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        progress_bar["value"] = index
        root.update_idletasks()

    messagebox.showinfo("Conversion Complete", "All AVI files have been converted to MP4.")

# Function to start conversion in a new thread
def start_conversion():
    folder = filedialog.askdirectory()
    if folder:
        threading.Thread(target=convert_videos, args=(folder,), daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("AVI to MP4 Converter")
root.geometry("400x200")
root.configure(bg="#1b3d21")  # Set background color

frame = tk.Frame(root, bg="#1b3d21")
frame.pack(expand=True)

label = tk.Label(frame, text="Select a folder with AVI files:", bg="#1b3d21", fg="white", font=("Arial", 12))
label.pack(pady=10)

select_button = tk.Button(frame, text="Select Folder & Convert", command=start_conversion, bg="white", fg="black", font=("Arial", 10))
select_button.pack(pady=5)

progress_bar = ttk.Progressbar(frame, length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()