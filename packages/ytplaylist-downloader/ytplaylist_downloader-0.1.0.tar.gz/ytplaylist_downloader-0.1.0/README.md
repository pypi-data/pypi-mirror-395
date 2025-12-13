# yt-playlist-dl

A lightweight CLI tool to download audio from YouTube playlists and videos. Perfect for Termux on Android!

## Features

- 🎵 Download audio-only from YouTube playlists and individual videos
- 📦 Lightweight with minimal dependencies (just yt-dlp)
- 🚀 Simple command-line interface
- 📱 Works great on Android via Termux
- 🎚️ Customizable audio format and quality

## Installation

### From PyPI (once published)

```bash
pip install yt-playlist-dl
```

### From source

```bash
git clone https://github.com/yourusername/yt-playlist-dl.git
cd yt-playlist-dl
pip install .
```

### On Termux (Android)

```bash
pkg install python ffmpeg
pip install yt-playlist-dl
```

## Usage

Download a playlist to the current directory:
```bash
yt-playlist-dl "https://www.youtube.com/playlist?list=..."
```

Download to a specific directory:
```bash
yt-playlist-dl -o ~/Music "https://www.youtube.com/playlist?list=..."
```

Download in different format with custom quality:
```bash
yt-playlist-dl -f m4a -q 256 "https://www.youtube.com/playlist?list=..."
```

Download a single video:
```bash
yt-playlist-dl "https://youtu.be/dQw4w9WgXcQ"
```

## Options

```
positional arguments:
  url                   YouTube playlist or video URL

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: current directory)
  -f {mp3,m4a,opus,wav,flac}, --format {mp3,m4a,opus,wav,flac}
                        Audio format (default: mp3)
  -q QUALITY, --quality QUALITY
                        Audio quality in kbps (default: 192)
  -v, --version         show program's version number and exit
```

## Requirements

- Python 3.7+
- yt-dlp
- FFmpeg (for audio conversion)

On Termux, install FFmpeg with:
```bash
pkg install ffmpeg
```

## License

MIT License - feel free to use and modify!

## Contributing

Pull requests welcome! For major changes, please open an issue first.
