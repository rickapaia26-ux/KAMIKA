# 🎵 KAMIKA

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rickapaia26-ux/KAMIKA?style=social)](https://github.com/rickapaia26-ux/KAMIKA/network/members)
[![GitHub issues](https://img.shields.io/github/issues/rickapaia26-ux/KAMIKA)](https://github.com/rickapaia26-ux/KAMIKA/issues)

> **Universal Music & Video Downloader** — Download músicas e vídeos do YouTube, Spotify, SoundCloud, Bandcamp e muito mais!

---

## ✨ Funcionalidades

- 🎬 **YouTube** — Vídeos e áudio (MP3, M4A, OPUS)
- 🟢 **Spotify** — Download de músicas e playlists
- 🟠 **SoundCloud** — Faixas e playlists completas
- 🟤 **Bandcamp** — Álbuns e faixas individuais
- 📋 **Playlists** — Download em massa de playlists completas
- 🎧 **Qualidade** — Opções de qualidade de áudio/vídeo
- 📁 **Organização** — Organiza automaticamente por artista/álbum

---

## 🚀 Instalação

`ash
# Clonar o repositório
git clone https://github.com/rickapaia26-ux/KAMIKA.git

# Entrar na pasta do projeto
cd KAMIKA

# Instalar dependências
pip install -r requirements.txt
`

---

## 📖 Uso

`ash
# Download de uma música do YouTube
python kamika.py "URL_DA_MUSICA"

# Download de uma playlist completa
python kamika.py --playlist "URL_DA_PLAYLIST"

# Download em formato específico
python kamika.py --format mp3 "URL_DA_MUSICA"

# Download de alta qualidade
python kamika.py --quality best "URL_DA_MUSICA"
`

---

## 📋 Exemplos

| Comando | Descrição |
|---------|-----------|
| python kamika.py "https://youtube.com/watch?v=..." | Download simples |
| python kamika.py --spotify "https://open.spotify.com/track/..." | Download do Spotify |
| python kamika.py --playlist "https://youtube.com/playlist?list=..." | Playlist do YouTube |
| python kamika.py --format flac "URL" | Download em FLAC |

---

## 🛠️ Requisitos

- Python 3.8+
- pip
- FFmpeg (para processamento de áudio/vídeo)

---

## 🤝 Contribuir

As contribuições são bem-vindas! 

1. Fork o projeto
2. Cria uma branch (git checkout -b feature/nova-feature)
3. Commit das tuas alterações (git commit -m 'Adicionar nova feature')
4. Push para a branch (git push origin feature/nova-feature)
5. Abre um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a MIT License — vê o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

## ⭐ Suporte

Se gostares do projeto, deixe uma ⭐ no GitHub! Ajuda imenso a divulgar o projeto.