"""Command-line interface for YouTube Playlist Downloader."""

import argparse
import sys
from pathlib import Path
from . import __version__
from .downloader import PlaylistDownloader


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Download audio from YouTube playlists or videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  yt-playlist-dl "https://www.youtube.com/playlist?list=..."
  yt-playlist-dl "https://youtu.be/dQw4w9WgXcQ"
  yt-playlist-dl -o ~/Music "https://www.youtube.com/playlist?list=..."
  yt-playlist-dl -f m4a -q 256 "https://www.youtube.com/playlist?list=..."
  yt-playlist-dl --login "https://www.youtube.com/playlist?list=LL"
        """
    )
    
    parser.add_argument(
        'url',
        help='YouTube playlist or video URL'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory for downloaded audio files (default: current directory)'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='mp3',
        choices=['mp3', 'm4a', 'opus', 'wav', 'flac'],
        help='Audio format (default: mp3)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        default='192',
        help='Audio quality in kbps (default: 192)'
    )
    
    parser.add_argument(
        '-c', '--cookies',
        help='Path to cookies.txt file for authentication'
    )
    
    parser.add_argument(
        '--login',
        action='store_true',
        help='Login to YouTube using OAuth (for private playlists like Liked videos). Opens browser or shows URL to authenticate.'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not ('youtube.com' in args.url or 'youtu.be' in args.url):
        print("❌ Error: Please provide a valid YouTube URL", file=sys.stderr)
        sys.exit(1)
    
    # Initialize downloader and start download
    try:
        downloader = PlaylistDownloader(
            output_dir=args.output,
            audio_format=args.format,
            audio_quality=args.quality,
            cookies_file=args.cookies,
            use_oauth=args.login
        )
        downloader.download(args.url)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
