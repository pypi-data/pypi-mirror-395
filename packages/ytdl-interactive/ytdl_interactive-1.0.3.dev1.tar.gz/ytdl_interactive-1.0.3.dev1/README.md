<div align="center">

# ytdl - Interactive YouTube Downloader

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/ytdl-interactive.svg)](https://pypi.org/project/ytdl-interactive/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/ytdl-interactive.svg)](https://pypi.org/project/ytdl-interactive/)
[![GitHub stars](https://img.shields.io/github/stars/abd3lraouf/ytdl.svg)](https://github.com/abd3lraouf/ytdl/stargazers)
[![CI](https://img.shields.io/github/actions/workflow/status/abd3lraouf/ytdl/ci.yml?branch=main&label=CI)](https://github.com/abd3lraouf/ytdl/actions)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

**A feature-rich, interactive CLI for downloading YouTube videos and playlists with ease.**

Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) with an intuitive menu system powered by [questionary](https://github.com/tmbo/questionary).

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-usage-guide) • [Contributing](CONTRIBUTING.md)

</div>

## ✨ Features

- 🎯 **Interactive Menu System** - Easy-to-use interface with questionary
- 📋 **Playlist Auto-Detection** - Automatically detects and organizes playlists
- ⚡ **Quick Default Download** - One-click download with optimal settings
- 🎨 **Advanced Configuration** - Fine-tune every aspect of your downloads
- 📁 **Smart Naming Templates** - Multiple presets + custom template support
- 🎵 **Audio Extraction** - Download and convert to MP3
- 🖼️ **Rich Post-Processing** - Thumbnails, subtitles, metadata embedding
- 🚀 **SponsorBlock Integration** - Automatically remove sponsors and ads
- 🌍 **Geo-Bypass & Proxy Support** - Download region-restricted content
- 📊 **Real-time Progress** - Live download progress and speed display

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install ytdl-interactive
```

### From Source

```bash
# Clone the repository
git clone https://github.com/abd3lraouf/ytdl.git
cd ytdl

# Install in development mode
pip install -e .
```

### Requirements

- Python 3.9 or higher
- FFmpeg (for video/audio processing)

#### Installing FFmpeg

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

## 🚀 Quick Start

### Basic Usage

```bash
# Download a single video
ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Download a playlist
ytdl "https://www.youtube.com/playlist?list=PLxxxxxx"

# Download from a channel
ytdl https://www.youtube.com/@channelname
```

### Command-line Options

```bash
ytdl [URL]                    # Start interactive mode with URL
ytdl --version                # Show version information
ytdl --help                   # Display help message
```

## 📖 Usage Guide

### Main Menu

After providing a URL, you'll see the main menu:

```
1. Quick Default Download (Recommended)
   └─ Downloads with optimal settings:
      - Best quality video + audio
      - Saved to ./downloads/
      - Auto-organized playlists

2. Advanced Download Settings
   └─ Customize every aspect:
      - Format selection
      - Output paths and naming
      - Post-processing options
      - Network settings

3. Exit
```

### Quick Default Download

The quickest way to download with optimal settings:

- **Format:** Best quality video + audio (automatically merged)
- **Output:** `./downloads/`
- **Single videos:** `Title.ext`
- **Playlists:** `PlaylistName/001 - VideoTitle.ext`

Example output structure:
```
downloads/
├── My Awesome Playlist/
│   ├── 001 - First Video.mp4
│   ├── 002 - Second Video.mp4
│   └── 003 - Third Video.mp4
└── Single Video Title.mp4
```

### Advanced Settings

#### 1. Download Type/Format

- **Video (Best Quality)** - `bestvideo*+bestaudio/best`
- **Audio Only (MP3)** - Extracts and converts to MP3 (192 kbps)
- **List Formats** - View all available formats and select custom format codes

#### 2. Output Path & Naming

**Preset Templates:**

| Template | Format | Example |
|----------|--------|---------|
| **Default** | `%(title)s.%(ext)s` | `My Video.mp4` |
| **Rich Metadata** | `%(upload_date)s - %(channel)s - %(title)s.%(ext)s` | `20231215 - Channel Name - My Video.mp4` |
| **Minimalist** | `%(id)s.%(ext)s` | `dQw4w9WgXcQ.mp4` |
| **Custom** | _Your template_ | Define your own! |

**Playlist Auto-Organization:**
All templates automatically organize playlists into subfolders with zero-padded indices.

**Custom Template Variables:**
```
%(title)s          - Video title
%(id)s             - Video ID
%(ext)s            - File extension
%(upload_date)s    - Upload date (YYYYMMDD)
%(channel)s        - Channel name
%(uploader)s       - Uploader name
%(playlist)s       - Playlist name
%(playlist_index)s - Video index in playlist
%(duration)s       - Video duration
%(view_count)s     - View count
```

#### 3. Post-Processing Options

- **Embed Thumbnail** - Embed video thumbnail in the file
- **Embed Subtitles** - Download and embed subtitles (English/Arabic)
- **Add Metadata** - Add rich metadata to the file
- **SponsorBlock** - Automatically remove sponsor segments and ads

#### 4. Networking Options

- **Proxy Support** - Route downloads through a proxy
  ```
  http://proxy.example.com:8080
  socks5://proxy.example.com:1080
  ```
- **Geo-Bypass** - Bypass geographic restrictions

## 💡 Examples

### Download a single video with defaults
```bash
ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ
# Select: 1. Quick Default Download
```

### Download playlist as MP3s
```bash
ytdl "https://www.youtube.com/playlist?list=PLxxxxxx"
# Select: 2. Advanced Settings
# → Select Download Type → Audio Only (MP3)
# → Start Download
```

### Custom output with metadata
```bash
ytdl https://www.youtube.com/watch?v=VIDEO_ID
# Select: 2. Advanced Settings
# → Output Path → Select "Rich Metadata"
# → Post-Processing → Check all options
# → Start Download
```

### Download with proxy
```bash
ytdl https://www.youtube.com/watch?v=VIDEO_ID
# Select: 2. Advanced Settings
# → Networking → Enter proxy URL
# → Start Download
```

## 🏗️ Project Structure

```
ytdl/
├── ytdl.py              # Main application
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── README.md            # This file
├── LICENSE              # MIT License
└── .gitignore          # Git ignore rules
```

## 🤖 Automated Releases

This project uses automated versioning and CI/CD:

- **Automatic versioning** via `setuptools_scm` (based on git tags)
- **Automated PyPI publishing** on new releases
- **CI testing** on all PRs and pushes
- **Release drafts** auto-generated from commits

### Creating a New Release

1. Go to **Actions** → **Bump Version** → **Run workflow**
2. Select version type (patch/minor/major)
3. Workflow automatically:
   - Creates git tag
   - Generates changelog
   - Creates GitHub release
   - Publishes to PyPI

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed release process.

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/abd3lraouf/ytdl.git
cd ytdl

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Code Structure

```python
# Main components:
DownloadConfig          # Configuration container
progress_hook()         # Real-time download progress
postprocessor_hook()    # Post-processing status
detect_playlist()       # Playlist detection
execute_download()      # Download execution
show_main_menu()        # Interactive menu system
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest

# Code formatting
black ytdl.py

# Type checking
mypy ytdl.py
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update README for new features
- Test thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful downloader this tool is built upon
- [questionary](https://github.com/tmbo/questionary) - Beautiful interactive prompts
- All contributors and users of this project

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service. Only download content you have permission to download.

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature request? Please [open an issue](https://github.com/abd3lraouf/ytdl/issues) on GitHub.

## 📮 Contact

- GitHub: [@abd3lraouf](https://github.com/abd3lraouf)
- Issues: [GitHub Issues](https://github.com/abd3lraouf/ytdl/issues)

## 🗺️ Roadmap

- [ ] Configuration file support (~/.ytdlrc)
- [ ] Download queue management
- [ ] Resume interrupted downloads
- [ ] Batch download from file
- [ ] GUI wrapper (tkinter/PyQt)
- [ ] Docker support
- [ ] Download scheduler

---

**Made with ❤️ by developers, for developers**
