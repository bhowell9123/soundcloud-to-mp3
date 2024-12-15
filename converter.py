import os
import subprocess
import shutil
from flask import Flask, request, send_file, jsonify, after_this_request

app = Flask(__name__)

DOWNLOADS_DIR = "./downloads"

# Ensure the downloads directory exists
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)


def download_soundcloud_to_mp3(soundcloud_url):
    """
    Downloads a SoundCloud track and converts it to MP3 format.
    """
    try:
        # Check if yt-dlp and ffmpeg are installed
        if not shutil.which("yt-dlp"):
            return {"error": "yt-dlp is not installed. Install it using 'pip install yt-dlp'."}
        if not shutil.which("ffmpeg"):
            return {"error": "ffmpeg is not installed. Install it to enable audio conversion."}

        # Construct the yt-dlp command
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", f"{DOWNLOADS_DIR}/%(title)s.%(ext)s",
            soundcloud_url
        ]

        # Run the command
        subprocess.run(command, check=True)

        # Find the downloaded file (the most recent file in the directory)
        downloaded_files = sorted(
            [f for f in os.listdir(DOWNLOADS_DIR) if f.endswith(".mp3")],
            key=lambda f: os.path.getmtime(os.path.join(DOWNLOADS_DIR, f)),
            reverse=True
        )
        if downloaded_files:
            return {"success": "Download complete!", "filename": downloaded_files[0]}
        else:
            return {"error": "File not found after download."}

    except subprocess.CalledProcessError as e:
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


@app.route("/", methods=["GET", "POST"])
def download_route():
    """
    Handles GET and POST requests:
    - GET: Serves a simple form for testing.
    - POST: Handles the SoundCloud MP3 download.
    """
    if request.method == "GET":
        # Return an HTML form for user input
        return '''
        <html>
            <head><title>SoundCloud to MP3</title></head>
            <body>
                <h1>SoundCloud to MP3 Converter</h1>
                <form method="POST" action="/">
                    <label for="url">SoundCloud URL:</label>
                    <input type="text" id="url" name="url" required>
                    <button type="submit">Download</button>
                </form>
            </body>
        </html>
        '''

    elif request.method == "POST":
        # Handle POST request for downloading a SoundCloud track
        data = request.form  # Accept form data from HTML
        soundcloud_url = data.get("url")

        if not soundcloud_url:
            return jsonify({"error": "Please provide a SoundCloud URL."}), 400

        # Download the file
        result = download_soundcloud_to_mp3(soundcloud_url)

        if "error" in result:
            return jsonify(result), 500

        # Return the file for download
        filename = result["filename"]
        file_path = os.path.join(DOWNLOADS_DIR, filename)

        @after_this_request
        def remove_file(response):
            """
            Deletes the file after it is sent to the user.
            """
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
