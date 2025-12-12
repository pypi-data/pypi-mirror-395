#!/usr/bin/env python3
"""
ytmagic - Universal Video & Audio Downloader
Author: Owais Shafi
GitHub: https://github.com/Meowahaha
PyPI: https://pypi.org/project/ytmagic/
License: MIT
"""

# -------------------- METADATA --------------------
__title__ = "ytmagic"
__version__ = "1.3.4"
__author__ = "Owais Shafi"
__license__ = "MIT"
# -------------------------------------------------

import argparse
import os
import sys
from pathlib import Path
from yt_dlp import YoutubeDL
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Console

console = Console()

quality_map = {
    "360": "best[height<=360]/best",
    "480": "best[height<=480]/best",
    "720": "best[height<=720]/best",
    "1080": "best[height<=1080]/best",
    "best": "best"
}

# -------- FALLBACK CLIENT PROFILES --------
# Force a working YouTube client to suppress JS/runtime warnings
CLIENT_PROFILES = [
    {"extractor_args": {"youtube": {"player_client": "android"}}},  # default fallback
    {"extractor_args": {"youtube": {"player_client": "web"}}},
    {"extractor_args": {"youtube": {"player_client": "ios"}}},
]

# -------- SHOW FORMATS FUNCTION --------
def show_formats(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": "android"}},  # suppress warning
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    formats = info.get("formats", [])
    if not formats:
        console.print("[red]No formats found for URL:[/red]", url)
        return

    console.print("\n[bold cyan]Available Formats for:[/bold cyan] " + url + "\n")
    console.print(f"{'format_id':>8}  {'ext':>4}  {'resolution':>9}  {'note':>20}")
    for f in formats:
        fid = f.get("format_id")
        ext = f.get("ext")
        res = f.get("resolution") or f.get("height") or ""
        note = []
        if f.get("vcodec") != "none":
            note.append("video")
        if f.get("acodec") != "none":
            note.append("audio")
        note = "/".join(note)
        console.print(f"{fid:>8}  {ext:>4}  {res:>9}  {note:>20}")

# -------- MAIN DOWNLOAD FUNCTION --------
def download_video(url, quality, download_path, audio_only=False, resume=False):
    os.makedirs(download_path, exist_ok=True)
    output_template = os.path.join(download_path, "%(title)s.%(ext)s")
    primary_format = "bestaudio/best" if audio_only else quality_map.get(quality, "best")
    fallback_format = "best"

    base_opts = {
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "continuedl": resume,
        "nopart": False,
        "addmetadata": True,
        "embedmetadata": True,
        "embedthumbnail": True,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "progress_hooks": [],
    }

    if audio_only:
        base_opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ]
        base_opts["keepvideo"] = False

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:

        task = progress.add_task("Downloading...", start=False)

        def hook(d):
            if d["status"] == "downloading" and not progress.tasks[task].started:
                progress.start_task(task)
            if d["status"] == "finished":
                progress.update(task, description="Processing...")
                console.print(f"\n✅ [bold green]Download complete:[/bold green] {d['filename']}")

        base_opts["progress_hooks"] = [hook]

        # -------- SMART FALLBACK LOOP --------
        for attempt, profile in enumerate(CLIENT_PROFILES, start=1):
            ydl_opts = {**base_opts, **profile, "format": primary_format}
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return
            except Exception:
                if attempt == 1:
                    console.print("⚠️  Normal client failed. Trying fallback clients...")
                elif attempt == len(CLIENT_PROFILES):
                    console.print("⚠️  All clients failed. Using safest fallback format...")

        # -------- FINAL HARD FALLBACK --------
        base_opts["format"] = fallback_format
        try:
            with YoutubeDL(base_opts) as ydl:
                ydl.download([url])
            console.print("⚠️  Downloaded with limited format due to platform restrictions.")
        except Exception as e:
            console.print(f"❌ [bold red]Fatal Download Error:[/bold red] {e}")
            sys.exit(1)

# -------- CLI ENTRY --------
def main():
    parser = argparse.ArgumentParser(
        description="🎥 Download videos or extract audio from YouTube, Instagram, Facebook, TikTok, X (Twitter), and more.",
        epilog=f"""
Examples:

1) Show the version of ytmagic:
  
   yt -v 

2) Download a video in best quality and save to Downloads folder:
  
   yt https://youtu.be/VIDEO_URL 

3) Download multiple videos in best quality to Downloads folder:

   yt URL1 URL2 URL3 

4) Convert to MP3(Audio only) and save to Music folder(user-specified path):
   
   yt -a -p ~/Music URL1 URL2 URL3 

5) Download videos in different Qualities to videos folder(user-specified path):

   yt -q 720 -p ~/Videos URL1 URL2 URL3 
   
   yt -q 360 -p ~/Videos URL1 URL2 URL3 

   yt -q best -p ~/Videos URL1 URL2 URL3

6) Show available Qualities/formats for multiple videos:
   
   yt -f URL1 URL2 URL3 

7) Resume interrupted downloads:
   
   yt -r URL1 URL2 URL3
   
   yt --resume URL1 URL2 URL3

Version: {__version__}
Author: {__author__}
Project: https://pypi.org/project/ytmagic/
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("urls", nargs="+", help="One or more video URLs")
    parser.add_argument("-q", "--quality", default="best", help="Choose Video quality (default: best)")
    parser.add_argument("-p", "--path", default=str(Path.home() / "Downloads"), help="Download to a user-specified path or folder(Default: ~/Downloads)" )
    parser.add_argument("-a", "--audio", action="store_true", help="Download Audio only (MP3)")
    parser.add_argument("-v", "--version", action="version", version=f"{__title__} {__version__}", help="Show program version and exit" )
    parser.add_argument("-r", "--resume", action="store_true", help="Resume interrupted downloads")
    parser.add_argument("-f", "--formats", action="store_true", help="Show available qualities/formats")

    args = parser.parse_args()

    # Format mode
    if args.formats:
        for idx, url in enumerate(args.urls, start=1):
            console.print(f"\n[bold yellow]Formats for ({idx}/{len(args.urls)}):[/bold yellow] {url}")
            show_formats(url)
        sys.exit(0)

    # Download mode
    for idx, url in enumerate(args.urls, start=1):
        console.print(f"\n[bold cyan]({idx}/{len(args.urls)}) Downloading:[/bold cyan] {url}")
        download_video(
            url,
            args.quality,
            args.path,
            audio_only=args.audio,
            resume=args.resume
        )

if __name__ == "__main__":
    main()
