# 🎵 KAMIKA

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/network/members)
[![GitHub issues](https://img.shields.io/github/issues/rickapaia26-ux/KAMIKA)](https://github.com/rickapaia26-ux/KAMIKA/issues)

> **Universal Music & Video Downloader** — Download music and videos from YouTube, Spotify, SoundCloud, Bandcamp and more!

---

## ✨ Features

- 🎬 **YouTube** — Download music (MP3) and video (MP4) with quality selection
- 🟢 **Spotify** — Track and playlist detection with YouTube search
- 🟠 **SoundCloud** — Direct track and playlist downloads
- 🟤 **Bandcamp** — Albums and individual tracks
- 🔵 **Deezer / Tidal / Apple Music / Audiomack** — Track detection
- 📋 **Playlists** — Full playlist download with auto-split for 150+ songs
- ✂️ **Audio/Video Cutting** — Trim by time range (MM:SS format)
- 🎧 **Video Quality** — 3 levels: Best (4K), HD (1080p), Medium (720p)
- 🌐 **Bilingual** — Portuguese & English

---

## 🚀 Quick Install (Windows)

**One click — everything is set up automatically!**

1. Download or clone this repository
2. Double-click **install.bat**
3. Follow the on-screen instructions

The installer will:
- ✅ Copy files to C:\Users\YOU\KAMIKA\
- ✅ Install **Python 3.12** (if not found)
- ✅ Install **yt-dlp** (download engine) via pip
- ✅ Download **ffmpeg** (~110MB) for MP3 conversion and video cutting
- ✅ Create a **Desktop shortcut**
- ✅ Create a **"KAMIKA Downloads"** folder on your Desktop

### Requirements
- **Python 3.8+** — [Download here](https://www.python.org/downloads/) (check "Add Python to PATH")
- **Internet connection** — for yt-dlp and ffmpeg download

---

## 📖 Usage

### Launch
- Double-click **KAMIKA START** on your Desktop
- Or run: python kamika.py

### YouTube Download
1. Choose **YouTube** from the main menu
2. Paste a YouTube link
3. Select **Music** or **Video**
4. Choose **Full** or **Cut** (time range)
5. Confirm and wait

### Track (Other Platforms)
1. Choose **Track** from the main menu
2. Paste a link from Spotify, SoundCloud, Bandcamp, etc.
3. Or type a song name to search on YouTube
4. KAMIKA auto-detects the platform and downloads

---

## 📋 Supported Platforms

| Platform | Detection |
|----------|-----------|
| YouTube | youtube.com / youtu.be |
| Spotify | spotify.com / open.spotify.com |
| SoundCloud | soundcloud.com |
| Bandcamp | bandcamp.com |
| Deezer | deezer.com |
| Tidal | tidal.com |
| Apple Music | music.apple.com |
| Audiomack | audiomack.com |

---

## 🛠️ Requirements

- **Python 3.8+**
- **yt-dlp** — installed automatically by install.bat
- **ffmpeg** — downloaded automatically by install.bat (optional, needed for MP3 + video cutting)

---

## 📁 Project Structure

    install.bat
    KAMIKA START.bat
    kamika.py
    requirements.txt
    uninstall/desinstalar.bat
    uninstall/README.md
    docs/README.md
    docs/TUTORIAL.md
    docs/REFACTOR-PLAN.md

---

## 🗑️ Uninstall

Run uninstall/desinstalar.bat or go to **Help > Uninstall** from the main menu.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Support

If you like this project, leave a ⭐ on GitHub! It helps a lot.