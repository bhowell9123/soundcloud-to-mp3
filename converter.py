import os
import subprocess
from flask import Flask, request, render_template_string
import shutil  # For checking dependencies

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <title>SoundCloud to MP3 Downloader</title>
</head>
<body>
    <h1>SoundCloud to MP3 Downloader</h1>
    <form method="POST">
        <label for="url">SoundCloud URL:</label><br>
        <input type="text" id="url" name="url" placeholder="Enter SoundCloud URL" required><br><br>
        <button type="submit">Download</button>
    </form>
    <p>{{ message }}</p>
</body>
</html>
"""

def download_soundcloud_to_mp3(soundcloud_url, output_directory):
    if not shutil.which("yt-dlp"):
        return "Error: yt-dlp is not installed. Install it using 'pip install yt-dlp'."

    if not shutil.which("ffmpeg"):
        return "Error: ffmpeg is not installed. Install it to enable audio conversion."

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", f"{output_directory}/%(title)s.%(ext)s",
        soundcloud_url
    ]

    try:
        subprocess.run(command, check=True)
        return "Download and conversion complete!"
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        soundcloud_url = request.form.get("url")
        output_directory = "./downloads"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if not soundcloud_url:
            message = "Please provide a valid SoundCloud URL."
        else:
            message = download_soundcloud_to_mp3(soundcloud_url, output_directory)

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == "__main__":
    app.run(debug=True)
