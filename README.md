# 🎵 KAMIKA

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/network/members)
[![GitHub issues](https://img.shields.io/github/issues/rickapaia26-ux/KAMIKA)](https://github.com/rickapaia26-ux/KAMIKA/issues)

> **Universal Music & Video Downloader** — Download music and videos from YouTube, Spotify, SoundCloud, Bandcamp and more!

---

## ✨ Features

- 🎬 **YouTube** — Videos and audio (MP3, M4A, OPUS)
- 🟢 **Spotify** — Music and playlist downloads
- 🟠 **SoundCloud** — Tracks and full playlists
- 🟤 **Bandcamp** — Albums and individual tracks
- 📋 **Playlists** — Bulk download of complete playlists
- 🎧 **Quality** — Audio/video quality options
- 📁 **Organization** — Automatic sorting by artist/album

---

## 🚀 Installation

`ash
# Clone the repository
git clone https://github.com/rickapaia26-ux/KAMIKA.git

# Navigate to the project directory
cd KAMIKA

# Install dependencies
pip install -r requirements.txt
`

---

## 📖 Usage

`ash
# Download a song from YouTube
python kamika.py "SONG_URL"

# Download a full playlist
python kamika.py --playlist "PLAYLIST_URL"

# Download in a specific format
python kamika.py --format mp3 "SONG_URL"

# Download in high quality
python kamika.py --quality best "SONG_URL"
`

---

## 📋 Examples

| Command | Description |
|---------|-------------|
| python kamika.py "https://youtube.com/watch?v=..." | Simple download |
| python kamika.py --spotify "https://open.spotify.com/track/..." | Spotify download |
| python kamika.py --playlist "https://youtube.com/playlist?list=..." | YouTube playlist |
| python kamika.py --format flac "URL" | Download in FLAC |

---

## 🛠️ Requirements

- Python 3.8+
- pip
- FFmpeg (for audio/video processing)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a branch (git checkout -b feature/new-feature)
3. Commit your changes (git commit -m 'Add new feature')
4. Push to the branch (git push origin feature/new-feature)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Support

If you like this project, leave a ⭐ on GitHub! It helps a lot to spread the word.