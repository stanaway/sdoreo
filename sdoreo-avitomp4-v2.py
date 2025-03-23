import os
import threading
import time
import subprocess
import signal
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Global variables for pause/resume
process = None
paused = False

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVI to MP4 Converter")
        self.root.geometry("500x400")
        self.root.configure(bg="#1b3d21")

        # Select Folder Button
        self.select_btn = tk.Button(root, text="Select Folder", command=self.start_conversion)
        self.select_btn.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        # Progress Label
        self.progress_label = tk.Label(root, text="", fg="white", bg="#1b3d21")
        self.progress_label.pack()

        # Pause & Resume Buttons
        self.pause_btn = tk.Button(root, text="Pause", command=self.pause_conversion)
        self.pause_btn.pack(pady=5)
        
        self.resume_btn = tk.Button(root, text="Resume", command=self.resume_conversion)
        self.resume_btn.pack(pady=5)

        # Drag-and-Drop support
        root.drop_target_register(DND_FILES)
        root.bind("<<Drop>>", self.drop)

    def drop(self, event):
        folder_path = event.data.strip("{}")
        threading.Thread(target=self.convert_videos, args=(folder_path,), daemon=True).start()

    def start_conversion(self):
        folder = filedialog.askdirectory(title="Select Folder with AVI Files")
        if not folder:
            return

        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            return

        avi_files = [f for f in os.listdir(folder) if f.lower().endswith(".avi")]
        
        if not avi_files:
            messagebox.showinfo("No AVI Files Found", "No AVI files were found in the selected folder.")
            return

        if not messagebox.askyesno("Confirm", f"{len(avi_files)} AVI files detected. Proceed with conversion?"):
            return

        threading.Thread(target=self.convert_videos, args=(folder, output_folder, avi_files), daemon=True).start()

    def convert_videos(self, folder, output_folder, avi_files):
        global process, paused
        
        total_files = len(avi_files)
        for index, avi_file in enumerate(avi_files):
            input_path = os.path.join(folder, avi_file)
            output_path = os.path.join(output_folder, os.path.splitext(avi_file)[0] + ".mp4")
            
            # Skip already converted files
            if os.path.exists(output_path):
                continue

            start_time = time.time()

            ffmpeg_command = [
                "ffmpeg", "-i", input_path,
                "-c:v", "libx265", "-preset", "slow", "-crf", "20",
                "-tag:v", "hvc1", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k",
                "-movflags", "+faststart",
                "-y", output_path
            ]
            
            process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            for line in process.stderr:
                if "frame=" in line:
                    progress = int((index + 1) / total_files * 100)
                    self.progress["value"] = progress
                    elapsed_time = time.time() - start_time
                    remaining_time = elapsed_time * (total_files - index - 1)
                    self.progress_label.config(text=f"Estimated Time Left: {remaining_time:.1f} sec")
                    self.root.update()
            
            process.wait()
            
            if process.returncode != 0:
                messagebox.showerror("Error", f"Conversion failed for {avi_file}")
                return
        
        messagebox.showinfo("Conversion Complete", "All files converted successfully!")

    def pause_conversion(self):
        global process, paused
        if process and not paused:
            process.send_signal(signal.SIGSTOP)
            paused = True

    def resume_conversion(self):
        global process, paused
        if process and paused:
            process.send_signal(signal.SIGCONT)
            paused = False

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
    