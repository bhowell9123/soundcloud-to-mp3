import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil  # For checking dependencies

def download_soundcloud_to_mp3(soundcloud_url, output_directory):
    """
    Downloads a SoundCloud track and converts it to MP3 format.

    :param soundcloud_url: The URL of the SoundCloud track to download.
    :param output_directory: The directory where the MP3 file will be saved.
    """
    try:
        # Check if yt-dlp is installed
        if not shutil.which("yt-dlp"):
            messagebox.showerror("Error", "yt-dlp is not installed. Install it using 'pip install yt-dlp'.")
            return

        # Check if ffmpeg is installed
        if not shutil.which("ffmpeg"):
            messagebox.showerror("Error", "ffmpeg is not installed. Install it to enable audio conversion.")
            return

        # Update status
        status_label.config(text="Downloading... Please wait.")
        root.update_idletasks()

        # Construct the command for yt-dlp
        command = [
    "yt-dlp",
    "--extract-audio",
    "--audio-format", "mp3",
    "--ffmpeg-location", "/opt/homebrew/bin/ffmpeg",
    "--output", f"{output_directory}/%(title)s.%(ext)s",
    soundcloud_url
]
        # Execute the command
        subprocess.run(command, check=True)

        # Update status to success
        status_label.config(text="Download and conversion complete!")
        messagebox.showinfo("Success", "Download and conversion complete!")
    except subprocess.CalledProcessError as e:
        status_label.config(text="Error occurred.")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        status_label.config(text="Unexpected error occurred.")
        messagebox.showerror("Error", f"Unexpected error: {e}")

def browse_directory():
    """
    Opens a dialog to select the output directory.
    """
    directory = filedialog.askdirectory()
    if directory:
        output_dir_var.set(directory)

def start_download():
    """
    Starts the download process when the button is clicked.
    """
    soundcloud_url = url_entry.get()
    output_directory = output_dir_var.get()

    if not soundcloud_url:
        messagebox.showwarning("Input Error", "Please enter a SoundCloud URL.")
        return

    if not output_directory:
        messagebox.showwarning("Input Error", "Please select an output directory.")
        return

    download_soundcloud_to_mp3(soundcloud_url, output_directory)

# Create the Tkinter GUI
root = tk.Tk()
root.title("SoundCloud to MP3 Downloader")

# Create the input frame
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# SoundCloud URL label and entry
tk.Label(frame, text="SoundCloud URL:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Output directory label, entry, and browse button
tk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w")
output_dir_var = tk.StringVar()
output_dir_entry = tk.Entry(frame, textvariable=output_dir_var, width=50)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
browse_button = tk.Button(frame, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# Status label
status_label = tk.Label(frame, text="")
status_label.grid(row=2, column=0, columnspan=3, pady=5)

# Download button
download_button = tk.Button(frame, text="Download", command=start_download)
download_button.grid(row=3, column=0, columnspan=3, pady=10)

# Run the GUI
root.mainloop()
