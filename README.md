# SoundCloud to MP3 Converter

This project is a simple tool to download SoundCloud tracks and convert them into MP3 format using a graphical user interface (GUI). It leverages `yt-dlp` for downloading and `ffmpeg` for audio conversion.

---

## Features

- Downloads tracks directly from SoundCloud.
- Converts the downloaded audio into MP3 format.
- User-friendly GUI for inputting the SoundCloud URL and selecting the output directory.

---

## Prerequisites

Before running this project, ensure the following tools are installed:

### 1. `yt-dlp`
Install using pip:

```bash
pip install yt-dlp
```

### 2. `ffmpeg`
Install using Homebrew (macOS):

```bash
brew install ffmpeg
```

For Windows, download `ffmpeg` from the [official website](https://ffmpeg.org/download.html) and add it to your system's PATH.

---

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/bhowell9123/soundcloud-to-mp3.git
cd soundcloud-to-mp3
```

2. Create a virtual environment (recommended) and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows

pip install -r requirements.txt
```

3. Ensure `yt-dlp` and `ffmpeg` are installed correctly (see Prerequisites).

---

## Usage

1. Run the script:

```bash
python converter.py
```

2. A GUI window will open:
   - Enter the SoundCloud URL of the track.
   - Select the output directory where you want the MP3 to be saved.
   - Click **Download**.

---

## License

This project is open-source and available under the MIT License.

---

## Acknowledgements

- `yt-dlp` for downloading SoundCloud tracks.
- `ffmpeg` for audio conversion.
