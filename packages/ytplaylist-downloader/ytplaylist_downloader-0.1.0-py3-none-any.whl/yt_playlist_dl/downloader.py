"""Core download functionality using yt-dlp."""

import os
import sys
from pathlib import Path
import yt_dlp


class PlaylistDownloader:
    """Handle YouTube playlist audio downloads."""
    
    def __init__(self, output_dir=None, audio_format='mp3', audio_quality='192'):
        """
        Initialize the downloader.
        
        Args:
            output_dir: Directory to save downloaded audio files (default: current directory)
            audio_format: Audio format (mp3, m4a, opus, etc.)
            audio_quality: Audio quality in kbps (default: 192)
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.audio_format = audio_format
        self.audio_quality = audio_quality
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download(self, url):
        """
        Download audio from a YouTube playlist or single video.
        
        Args:
            url: YouTube playlist or video URL
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': self.audio_quality,
            }],
            'outtmpl': str(self.output_dir / '%(playlist_index)s - %(title)s.%(ext)s'),
            'ignoreerrors': True,  # Continue on errors
            'no_warnings': False,
            'quiet': False,
            'progress_hooks': [self._progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n📥 Starting download to: {self.output_dir}\n")
                info = ydl.extract_info(url, download=True)
                
                # Check if it's a playlist or single video
                if 'entries' in info:
                    total = len([e for e in info['entries'] if e is not None])
                    print(f"\n✅ Successfully processed playlist with {total} tracks!")
                else:
                    print(f"\n✅ Successfully downloaded: {info.get('title', 'Unknown')}")
                    
        except Exception as e:
            print(f"\n❌ Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def _progress_hook(self, d):
        """Display download progress."""
        if d['status'] == 'downloading':
            # Clear line and show progress
            filename = os.path.basename(d['filename'])
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\r⏬ {filename} | {percent} | {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            filename = os.path.basename(d['filename'])
            print(f"\r✓ Downloaded: {filename}" + " " * 20)
