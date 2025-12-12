#!/usr/bin/env python3
"""
ytdl - A feature-rich interactive CLI for yt-dlp

An interactive command-line interface for downloading YouTube videos and playlists
with advanced configuration options.

Usage:
    python ytdl.py [YOUTUBE_URL]
    ytdl [YOUTUBE_URL]  (if installed as package)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

import questionary
from questionary import Style
import yt_dlp


# Custom styling for questionary prompts
CUSTOM_STYLE = Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:green bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:green'),
    ('separator', 'fg:gray'),
    ('instruction', 'fg:gray'),
])

# Default configuration constants
DEFAULT_OUTPUT_DIR = "./downloads"
DEFAULT_VIDEO_FORMAT = "bestvideo*+bestaudio/best"
DEFAULT_SINGLE_TEMPLATE = "%(title)s.%(ext)s"
DEFAULT_PLAYLIST_TEMPLATE = "%(playlist)s/%(playlist_index)03d - %(title)s.%(ext)s"

# Naming template presets
NAMING_TEMPLATES = {
    "default": {
        "single": DEFAULT_SINGLE_TEMPLATE,
        "playlist": DEFAULT_PLAYLIST_TEMPLATE,
        "description": "Default (Title-based)"
    },
    "rich_metadata": {
        "single": "%(upload_date)s - %(channel)s - %(title)s.%(ext)s",
        "playlist": "%(playlist)s/%(playlist_index)03d - %(upload_date)s - %(channel)s - %(title)s.%(ext)s",
        "description": "Rich Metadata (Date - Channel - Title)"
    },
    "minimalist": {
        "single": "%(id)s.%(ext)s",
        "playlist": "%(playlist)s/%(playlist_index)03d - %(id)s.%(ext)s",
        "description": "Minimalist (Video ID only)"
    }
}


class DownloadConfig:
    """Configuration container for download options."""

    def __init__(self):
        self.url: str = ""
        self.is_playlist: bool = False
        self.output_dir: str = DEFAULT_OUTPUT_DIR
        self.format: str = DEFAULT_VIDEO_FORMAT
        self.naming_template: str = DEFAULT_SINGLE_TEMPLATE
        self.audio_only: bool = False
        self.embed_thumbnail: bool = False
        self.embed_subs: bool = False
        self.add_metadata: bool = False
        self.sponsorblock: bool = False
        self.proxy: Optional[str] = None
        self.geo_bypass: bool = False

    def get_output_template(self) -> str:
        """Get the full output template path."""
        return str(Path(self.output_dir) / self.naming_template)

    def to_yt_dlp_opts(self) -> dict[str, Any]:
        """Convert config to yt-dlp options dictionary."""
        opts = {
            'format': self.format,
            'outtmpl': self.get_output_template(),
            'progress_hooks': [progress_hook],
            'postprocessor_hooks': [postprocessor_hook],
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
        }

        postprocessors = []

        if self.audio_only:
            opts['format'] = 'bestaudio/best'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        if self.embed_thumbnail:
            opts['writethumbnail'] = True
            postprocessors.append({'key': 'EmbedThumbnail'})

        if self.embed_subs:
            opts['writesubtitles'] = True
            opts['subtitleslangs'] = ['en', 'ar']
            opts['embedsubtitles'] = True
            postprocessors.append({
                'key': 'FFmpegSubtitlesConvertor',
                'format': 'srt',
            })
            postprocessors.append({'key': 'FFmpegEmbedSubtitle'})

        if self.add_metadata:
            postprocessors.append({'key': 'FFmpegMetadata'})

        if self.sponsorblock:
            opts['sponsorblock_remove'] = ['all']
            postprocessors.append({
                'key': 'SponsorBlock',
                'categories': ['all'],
            })
            postprocessors.append({
                'key': 'ModifyChapters',
                'remove_sponsor_segments': ['all'],
            })

        if self.proxy:
            opts['proxy'] = self.proxy

        if self.geo_bypass:
            opts['geo_bypass'] = True

        if postprocessors:
            opts['postprocessors'] = postprocessors

        return opts


def progress_hook(d: dict[str, Any]) -> None:
    """Progress hook for yt-dlp to display download status."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        filename = d.get('filename', 'Unknown')
        # Truncate filename for display
        display_name = Path(filename).name
        if len(display_name) > 50:
            display_name = display_name[:47] + "..."
        print(f"\r  Downloading: {percent} | Speed: {speed} | ETA: {eta} | {display_name}", end='', flush=True)

    elif d['status'] == 'finished':
        print(f"\n  Download complete: {Path(d.get('filename', 'Unknown')).name}")

    elif d['status'] == 'error':
        print(f"\n  Error occurred during download")


def postprocessor_hook(d: dict[str, Any]) -> None:
    """Post-processor hook for yt-dlp to display post-processing status."""
    if d['status'] == 'started':
        pp_name = d.get('postprocessor', 'Unknown')
        print(f"  Post-processing: {pp_name}...")
    elif d['status'] == 'finished':
        print(f"  Post-processing complete")


def validate_youtube_url(url: str) -> bool:
    """
    Validate if the provided URL is a plausible YouTube URL.

    Args:
        url: The URL to validate

    Returns:
        True if URL appears to be a valid YouTube URL, False otherwise
    """
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://(www\.)?youtube\.com/playlist\?list=[\w-]+',
        r'^https?://(www\.)?youtube\.com/shorts/[\w-]+',
        r'^https?://(www\.)?youtube\.com/@[\w-]+',
        r'^https?://(www\.)?youtube\.com/channel/[\w-]+',
        r'^https?://(www\.)?youtube\.com/c/[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://music\.youtube\.com/',
    ]

    for pattern in youtube_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


def detect_playlist(url: str) -> tuple[bool, Optional[dict]]:
    """
    Detect if the URL is a playlist or single video using yt-dlp.

    Args:
        url: The YouTube URL to check

    Returns:
        Tuple of (is_playlist, info_dict)
    """
    print("\n  Analyzing URL...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if info is None:
                return False, None

            is_playlist = info.get('_type') == 'playlist' or 'entries' in info

            if is_playlist:
                entry_count = len(info.get('entries', []))
                playlist_title = info.get('title', 'Unknown Playlist')
                print(f"  Detected: Playlist - '{playlist_title}' ({entry_count} videos)")
            else:
                video_title = info.get('title', 'Unknown Video')
                print(f"  Detected: Single Video - '{video_title}'")

            return is_playlist, info

    except yt_dlp.utils.DownloadError as e:
        print(f"\n  Error analyzing URL: {e}")
        return False, None


def list_formats(url: str) -> None:
    """
    List all available formats for the given URL.

    Args:
        url: The YouTube URL to analyze
    """
    print("\n  Fetching available formats...\n")

    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"\n  Error fetching formats: {e}")


def execute_download(config: DownloadConfig) -> bool:
    """
    Execute the download with the given configuration.

    Args:
        config: The download configuration

    Returns:
        True if download was successful, False otherwise
    """
    # Ensure output directory exists
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("  Starting Download")
    print(f"{'='*60}")
    print(f"  URL: {config.url}")
    print(f"  Output Directory: {config.output_dir}")
    print(f"  Format: {'Audio Only (MP3)' if config.audio_only else config.format}")
    print(f"  Template: {config.naming_template}")

    options_list = []
    if config.embed_thumbnail:
        options_list.append("Embed Thumbnail")
    if config.embed_subs:
        options_list.append("Embed Subtitles")
    if config.add_metadata:
        options_list.append("Add Metadata")
    if config.sponsorblock:
        options_list.append("SponsorBlock")
    if config.geo_bypass:
        options_list.append("Geo-Bypass")
    if config.proxy:
        options_list.append(f"Proxy: {config.proxy}")

    if options_list:
        print(f"  Options: {', '.join(options_list)}")

    print(f"{'='*60}\n")

    try:
        opts = config.to_yt_dlp_opts()

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([config.url])

        print(f"\n{'='*60}")
        print("  Download Complete!")
        print(f"{'='*60}\n")
        return True

    except yt_dlp.utils.DownloadError as e:
        print(f"\n  Download Error: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n  Download cancelled by user.")
        return False
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        return False


def show_advanced_menu(config: DownloadConfig) -> Optional[DownloadConfig]:
    """
    Display the advanced settings menu and update configuration.

    Args:
        config: The current download configuration

    Returns:
        Updated configuration or None if user wants to go back
    """
    while True:
        print("\n")
        choice = questionary.select(
            "Advanced Download Settings:",
            choices=[
                "1. Select Download Type/Format",
                "2. Define Output Path and Naming Template",
                "3. Post-Processing Options",
                "4. Networking/Bypass Options",
                "5. Start Download",
                "← Back to Main Menu"
            ],
            style=CUSTOM_STYLE
        ).ask()

        if choice is None or choice == "← Back to Main Menu":
            return None

        if "Select Download Type" in choice:
            config = format_selection_menu(config)

        elif "Output Path" in choice:
            config = output_path_menu(config)

        elif "Post-Processing" in choice:
            config = post_processing_menu(config)

        elif "Networking" in choice:
            config = networking_menu(config)

        elif "Start Download" in choice:
            return config


def format_selection_menu(config: DownloadConfig) -> DownloadConfig:
    """Format selection submenu."""
    choice = questionary.select(
        "Select Download Type/Format:",
        choices=[
            "Video (Default - best quality)",
            "Audio Only (MP3)",
            "List Available Formats",
            "← Back"
        ],
        style=CUSTOM_STYLE
    ).ask()

    if choice is None or "Back" in choice:
        return config

    if "Video" in choice:
        config.audio_only = False
        config.format = DEFAULT_VIDEO_FORMAT
        print("  Selected: Best quality video + audio")

    elif "Audio Only" in choice:
        config.audio_only = True
        print("  Selected: Audio only (MP3)")

    elif "List Available" in choice:
        list_formats(config.url)
        # After listing, ask for custom format
        custom = questionary.confirm(
            "Would you like to specify a custom format code?",
            default=False,
            style=CUSTOM_STYLE
        ).ask()

        if custom:
            format_code = questionary.text(
                "Enter format code (e.g., '137+140' or 'best'):",
                style=CUSTOM_STYLE
            ).ask()
            if format_code:
                config.format = format_code
                config.audio_only = False
                print(f"  Custom format set: {format_code}")

    return config


def output_path_menu(config: DownloadConfig) -> DownloadConfig:
    """Output path and naming template submenu."""
    # Output directory
    new_dir = questionary.text(
        "Enter output directory:",
        default=config.output_dir,
        style=CUSTOM_STYLE
    ).ask()

    if new_dir:
        config.output_dir = new_dir

    # Naming template selection
    template_choices = [
        f"A. {NAMING_TEMPLATES['default']['description']}",
        f"B. {NAMING_TEMPLATES['rich_metadata']['description']}",
        f"C. {NAMING_TEMPLATES['minimalist']['description']}",
        "D. Custom Template",
        "← Back"
    ]

    choice = questionary.select(
        "Select Naming Template:",
        choices=template_choices,
        style=CUSTOM_STYLE
    ).ask()

    if choice is None or "Back" in choice:
        return config

    if "A." in choice:
        template_key = "default"
    elif "B." in choice:
        template_key = "rich_metadata"
    elif "C." in choice:
        template_key = "minimalist"
    elif "D." in choice:
        custom_template = questionary.text(
            "Enter custom template (use yt-dlp template syntax):",
            default="%(title)s.%(ext)s",
            style=CUSTOM_STYLE
        ).ask()

        if custom_template:
            if config.is_playlist and "%(playlist)s" not in custom_template:
                # Automatically add playlist folder for playlists
                config.naming_template = f"%(playlist)s/{custom_template}"
                print(f"  Template (with playlist folder): {config.naming_template}")
            else:
                config.naming_template = custom_template
                print(f"  Template set: {config.naming_template}")
        return config
    else:
        return config

    # Set the template based on playlist detection
    if config.is_playlist:
        config.naming_template = NAMING_TEMPLATES[template_key]['playlist']
    else:
        config.naming_template = NAMING_TEMPLATES[template_key]['single']

    print(f"  Template set: {config.naming_template}")
    return config


def post_processing_menu(config: DownloadConfig) -> DownloadConfig:
    """Post-processing options submenu."""
    selected = questionary.checkbox(
        "Select Post-Processing Options:",
        choices=[
            questionary.Choice("Embed Thumbnail", checked=config.embed_thumbnail),
            questionary.Choice("Embed Subtitles", checked=config.embed_subs),
            questionary.Choice("Add Metadata", checked=config.add_metadata),
            questionary.Choice("SponsorBlock (Remove Sponsors/Ads)", checked=config.sponsorblock),
        ],
        style=CUSTOM_STYLE
    ).ask()

    if selected is not None:
        config.embed_thumbnail = "Embed Thumbnail" in selected
        config.embed_subs = "Embed Subtitles" in selected
        config.add_metadata = "Add Metadata" in selected
        config.sponsorblock = "SponsorBlock (Remove Sponsors/Ads)" in selected

        enabled = [opt for opt in selected] if selected else ["None"]
        print(f"  Post-processing options: {', '.join(enabled)}")

    return config


def networking_menu(config: DownloadConfig) -> DownloadConfig:
    """Networking and bypass options submenu."""
    # Proxy input
    proxy_input = questionary.text(
        "Enter proxy URL (leave empty for none):",
        default=config.proxy or "",
        style=CUSTOM_STYLE
    ).ask()

    config.proxy = proxy_input if proxy_input else None

    # Geo-bypass toggle
    config.geo_bypass = questionary.confirm(
        "Enable Geo-Bypass?",
        default=config.geo_bypass,
        style=CUSTOM_STYLE
    ).ask()

    settings = []
    if config.proxy:
        settings.append(f"Proxy: {config.proxy}")
    if config.geo_bypass:
        settings.append("Geo-Bypass: Enabled")

    if settings:
        print(f"  Network settings: {', '.join(settings)}")
    else:
        print("  Network settings: Default (no proxy, no geo-bypass)")

    return config


def show_main_menu(config: DownloadConfig) -> Optional[str]:
    """
    Display the main menu.

    Args:
        config: The current download configuration

    Returns:
        Selected action or None
    """
    print("\n")
    return questionary.select(
        "What would you like to do?",
        choices=[
            "1. Quick Default Download (Recommended)",
            "2. Advanced Download Settings",
            "3. Exit"
        ],
        style=CUSTOM_STYLE
    ).ask()


def main():
    """Main entry point for the ytdl CLI application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="ytdl - Interactive YouTube Downloader powered by yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ
  ytdl "https://www.youtube.com/playlist?list=PLxxxxxx"
  python ytdl.py https://youtu.be/dQw4w9WgXcQ
        """
    )
    parser.add_argument(
        "url",
        help="YouTube video or playlist URL to download"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="ytdl 1.0.0"
    )

    args = parser.parse_args()

    # Display banner
    print("\n" + "="*60)
    print("  ytdl - Interactive YouTube Downloader")
    print("  Powered by yt-dlp")
    print("="*60)

    # Validate URL
    if not validate_youtube_url(args.url):
        print(f"\n  Warning: URL may not be a valid YouTube URL: {args.url}")
        proceed = questionary.confirm(
            "Do you want to proceed anyway?",
            default=False,
            style=CUSTOM_STYLE
        ).ask()
        if not proceed:
            print("  Exiting.")
            sys.exit(0)

    # Create configuration
    config = DownloadConfig()
    config.url = args.url

    # Detect if URL is a playlist
    is_playlist, info = detect_playlist(args.url)
    config.is_playlist = is_playlist

    # Set appropriate default naming template
    if is_playlist:
        config.naming_template = DEFAULT_PLAYLIST_TEMPLATE
    else:
        config.naming_template = DEFAULT_SINGLE_TEMPLATE

    # Main menu loop
    while True:
        choice = show_main_menu(config)

        if choice is None or "Exit" in choice:
            print("\n  Goodbye!\n")
            sys.exit(0)

        elif "Quick Default" in choice:
            # Use default settings and download
            execute_download(config)

            # Ask if user wants to download another
            again = questionary.confirm(
                "Download another video?",
                default=False,
                style=CUSTOM_STYLE
            ).ask()

            if not again:
                print("\n  Goodbye!\n")
                sys.exit(0)
            else:
                new_url = questionary.text(
                    "Enter new YouTube URL:",
                    style=CUSTOM_STYLE
                ).ask()

                if new_url and validate_youtube_url(new_url):
                    config = DownloadConfig()
                    config.url = new_url
                    is_playlist, _ = detect_playlist(new_url)
                    config.is_playlist = is_playlist
                    if is_playlist:
                        config.naming_template = DEFAULT_PLAYLIST_TEMPLATE
                    else:
                        config.naming_template = DEFAULT_SINGLE_TEMPLATE
                elif new_url:
                    print("  Invalid URL. Returning to main menu.")
                    config.url = new_url

        elif "Advanced" in choice:
            updated_config = show_advanced_menu(config)
            if updated_config:
                config = updated_config
                execute_download(config)

                # Ask if user wants to download another
                again = questionary.confirm(
                    "Download another video?",
                    default=False,
                    style=CUSTOM_STYLE
                ).ask()

                if not again:
                    print("\n  Goodbye!\n")
                    sys.exit(0)
                else:
                    new_url = questionary.text(
                        "Enter new YouTube URL:",
                        style=CUSTOM_STYLE
                    ).ask()

                    if new_url:
                        config = DownloadConfig()
                        config.url = new_url
                        is_playlist, _ = detect_playlist(new_url)
                        config.is_playlist = is_playlist
                        if is_playlist:
                            config.naming_template = DEFAULT_PLAYLIST_TEMPLATE
                        else:
                            config.naming_template = DEFAULT_SINGLE_TEMPLATE


if __name__ == "__main__":
    main()
