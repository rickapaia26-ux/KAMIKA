# KAMIKA v2.1

> Universal Music / Video Downloader — YouTube, Spotify, SoundCloud, Bandcamp, and more.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![yt-dlp](https://img.shields.io/badge/yt--dlp-2026.06.09-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

---

## Features

- **MP3 Download** — Best audio quality (`--audio-quality 0`)
- **Video Download** — 3 quality levels with auto fallback:
  - Best (4K, 60fps, HDR) → MKV
  - HD (1080p) → MP4
  - Medium (720p) → MP4
- **Audio/Video Trimming** — Cut by time (MM:SS)
- **Playlists** — Full download with auto-split when over 150 tracks
- **Track mode** — Download from any platform:
  YouTube, Spotify, SoundCloud, Bandcamp, Deezer, Tidal, Apple Music, Audiomack
- **Help Menu** — Repair installation, Uninstall, Credits
- **Dual Language** — Portuguese / English

## Installation

### Option 1: Portable Setup
1. Download `KAMIKA_Setup.bat` + `KAMIKA_Setup.zip`
2. Run `KAMIKA_Setup.bat`
3. It will:
   - Check Python
   - Install yt-dlp
   - Copy files to `%USERPROFILE%\KAMIKA\`
   - Create Desktop shortcut

### Option 2: Manual
1. Ensure Python 3.8+ is installed
2. Run `install.bat`
3. Or manually: `pip install yt-dlp`

## Usage

1. Double-click `KAMIKA START.bat` (or Desktop shortcut)
2. Choose language
3. Select **YouTube** or **Track**
4. Paste a link and follow the prompts

## Requirements

- **OS:** Windows 10 / 11
- **Python:** 3.8+ (with `pip` and `Add to PATH`)
- **ffmpeg:** Optional — required for MP3 conversion and video cutting
- **Internet:** Required for downloads

## Install Locations

| Item | Path |
|------|------|
| Program files | `%USERPROFILE%\KAMIKA\` |
| Shortcut | Desktop → `KAMIKA START.lnk` |
| Downloads | Desktop → `KAMIKA Downloads\` |

## Uninstall

Run `%USERPROFILE%\KAMIKA\uninstall\desinstalar.bat`
Or open the app → Help → Uninstall KAMIKA

## Tech Stack

- **Language:** Python (standard library only — no pip dependencies besides yt-dlp)
- **Engine:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) + ffmpeg
- **Lines:** ~1250

## License

MIT — see [LICENSE](LICENSE)

---

*Built with Python by KAPA — 2025-2026*
