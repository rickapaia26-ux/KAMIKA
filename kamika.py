import os
import subprocess
import sys
import re
import time
import shutil
import glob
import json
from pathlib import Path


sys.stdout.reconfigure(encoding='utf-8')

DEV_DIR = Path(__file__).parent / "dev"
LOG_DIR = DEV_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_msg(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_DIR / f"session_{time.strftime('%Y-%m-%d')}.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

MUSIC_DIR = Path.home() / "Desktop" / "KAMIKA Downloads"
VIDEO_DIR = Path.home() / "Desktop" / "KAMIKA Downloads"
SCRIPT_DIR = Path(__file__).parent
LOADING_DIR = SCRIPT_DIR / "LOADING"

def start_loading():
    LOADING_DIR.mkdir(parents=True, exist_ok=True)
    return LOADING_DIR

def clean_thumbnails(directory):
    """Remove thumbnail files (.webp, .jpg, .jpeg, .png) from a directory."""
    try:
        for f in Path(directory).iterdir():
            if f.is_file() and f.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png"):
                try:
                    f.unlink()
                except Exception:
                    pass
    except Exception:
        pass

def unique_path(path):
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    n = 1
    while True:
        new = parent / f"{stem} ({n}){suffix}"
        if not new.exists():
            return new
        n += 1

def finish_loading(final_dir):
    if not LOADING_DIR.exists():
        return
    clean_thumbnails(LOADING_DIR)
    for f in LOADING_DIR.iterdir():
        if f.is_file():
            dest = unique_path(final_dir / f.name)
            try:
                f.replace(dest)
            except Exception:
                try:
                    shutil.copy2(f, dest)
                    f.unlink()
                except Exception:
                    pass
    try:
        LOADING_DIR.rmdir()
    except Exception:
        pass

def ask_confirm():
    """Pergunta S/N, insiste ate resposta valida. Retorna True (sim) ou False (nao)."""
    while True:
        answer = input(f"  \033[38;5;208m[ ]\033[0m {LANG['confirm']}? \033[38;5;208m>\033[0m \033[1;31m(S/N)\033[0m: ").strip().lower()
        if answer in ("s", "y", "sim", "yes"):
            return True
        if answer in ("n", "nao", "no", ""):
            return False
        print(f"\n  \033[1;33m{'─' * 53}\033[0m")
        print(f"  \033[1;33m  Resposta invalida! Use S (Sim) ou N (Nao)\033[0m")
        print(f"  \033[1;33m{'─' * 53}\033[0m")
        print()

def find_ytdlp():
    """Find real yt-dlp.exe, avoiding pyenv .bat shim that breaks %variables%."""
    script_path = os.path.abspath(__file__) if '__file__' in dir() else os.path.abspath(sys.argv[0])
    script_dir = Path(os.path.dirname(script_path))
    local_exe = script_dir / "yt-dlp.exe"
    if local_exe.exists():
        return str(local_exe)
    pyenv_versions = Path.home() / ".pyenv" / "pyenv-win" / "versions"
    if pyenv_versions.is_dir():
        for ver_dir in sorted(pyenv_versions.iterdir(), reverse=True):
            exe = ver_dir / "Scripts" / "yt-dlp.exe"
            if exe.exists():
                return str(exe)
    found = shutil.which("yt-dlp")
    if found and found.endswith(".exe"):
        return found
    return "yt-dlp"

YTDLP = find_ytdlp()

LANG = {}
CURRENT_LANG = None

def set_lang(lang):
    global LANG, CURRENT_LANG
    CURRENT_LANG = lang
    if lang == "1":
        LANG = {
            "main_opt1": "YouTube",
            "main_opt2": "Rastrear",
            "ask_url": "Link do YouTube: ",
            "invalid_url": "Link invalido. Prima Enter...",
            "opt_music": "Musica",
            "opt_video": "Video",
            "back": "Voltar",
            "invalid_opt": "ESCOLHA UMA DAS OPCOES DISPONIVEIS",
            "press_enter": "Prima Enter para continuar...",
            "back_main": "Prima Enter para voltar ao menu principal...",
            "done": "Download Concluido com Sucesso!",
            "confirm": "Download",
            "post_title": "O QUE DESEJA FAZER?",
            "post_title_now": "O QUE DESEJA FAZER AGORA?",
            "post_open": "Abrir pasta",
            "post_back": "Voltar ao inicio",
            "post_exit": "Sair",
            "time_header": "Intervalo de tempo",
            "time_fmt": "Formato: MM:SS    00:12  01:10  32:21",
            "time_invalid": "Formato de tempo invalido. Prima Enter...",
            "ask_start": "Escolha tempo de inicio: ",
            "ask_end": "Escolha tempo de fim:    ",
            "dl_music_full": "A preparar o download da sua musica ... Aguarde",
            "dl_music_between": "A preparar o download da sua musica de {0} ate {1} ... Aguarde",
            "dl_music_from": "A preparar o download da sua musica de {0} ao fim ... Aguarde",
            "dl_music_until": "A preparar o download da sua musica do inicio ate {0} ... Aguarde",
            "dl_video_full": "A preparar o download do seu video ... Aguarde",
            "dl_video_between": "A preparar o download do seu video de {0} ate {1} ... Aguarde",
            "dl_video_from": "A preparar o download do seu video de {0} ao fim ... Aguarde",
            "dl_video_until": "A preparar o download do seu video do inicio ate {0} ... Aguarde",
            "dl_to": "Para:",
            "goodbye": "Ate logo!",
            "rastrear_title": "RASTREAR",
            "menu_title": "MENU PRINCIPAL",
            "rastrear_ask": "Link ou nome da musica: ",
            "rastrear_invalid": "Entrada invalida. Prima Enter...",
            "rastrear_spotify": "Spotify detectado, a procurar no YouTube...",
            "rastrear_yt_link": "YouTube detectado, A preparar o download...",
            "rastrear_platforms": "Plataformas suportadas:",
            "rastrear_any_link": "Ou qualquer link / nome de musica",
            "rastrear_scraping": "A analisar o site por ficheiros de audio...",
            "rastrear_found_files": "Ficheiros de audio encontrados:",
            "rastrear_no_files": "Nenhum ficheiro encontrado, a procurar no YouTube...",
            "choose_prompt": "Escolha uma opcao:",
            "other_platforms": "outras plataformas/links",
            "loading": "A carregar",
            "full_title": "MODO DE DOWNLOAD",
            "full_opt_full": "Musica Completa",
            "full_opt_full_m": "Video Completo",
            "full_opt_cut": "Cortar Musica",
            "full_opt_cut_v": "Cortar Video",
            "dl_error": "Erro ao preparar download",
            "dl_not_found": "Ficheiro nao encontrado",
            "dl_cut_error": "Erro ao cortar",
            "playlist_single": "Download apenas desta Musica",
            "playlist_all": "Download da Playlist completa",
            "playlist_detected": "PLAYLIST DETETADA!",
            "playlist_split": "Playlist com {0} musicas. Dividida em {1} partes.",
            "playlist_part": "Parte {0}/{1}: {2} musicas",
            "playlist_downloading": "A descarregar parte {0}/{1}...",
        }
    else:
        LANG = {
            "main_opt1": "YouTube",
            "main_opt2": "Track",
            "ask_url": "YouTube link: ",
            "invalid_url": "Invalid link. Press Enter...",
            "opt_music": "Music",
            "opt_video": "Video",
            "back": "Back",
            "invalid_opt": "CHOOSE A VALID OPTION",
            "press_enter": "Press Enter to continue...",
            "back_main": "Press Enter to go back to main menu...",
            "done": "Download Complete!",
            "confirm": "Download",
            "post_title": "WHAT DO YOU WANT TO DO?",
            "post_title_now": "WHAT DO YOU WANT TO DO NOW?",
            "post_open": "Open folder",
            "post_back": "Back to start",
            "post_exit": "Exit",
            "time_header": "Time range",
            "time_fmt": "Format: MM:SS    00:12  01:10  32:21",
            "time_invalid": "Invalid time format. Press Enter...",
            "ask_start": "Choose start time: ",
            "ask_end": "Choose end time:   ",
            "dl_music_full": "Preparing your music download ... Please wait",
            "dl_music_between": "Preparing your music download from {0} to {1} ... Please wait",
            "dl_music_from": "Preparing your music download from {0} to end ... Please wait",
            "dl_music_until": "Preparing your music download from start to {0} ... Please wait",
            "dl_video_full": "Preparing your video download ... Please wait",
            "dl_video_between": "Preparing your video download from {0} to {1} ... Please wait",
            "dl_video_from": "Preparing your video download from {0} to end ... Please wait",
            "dl_video_until": "Preparing your video download from start to {0} ... Please wait",
            "dl_to": "To:",
            "goodbye": "Goodbye!",
            "rastrear_title": "TRACK",
            "menu_title": "MAIN MENU",
            "rastrear_ask": "Link or song name: ",
            "rastrear_invalid": "Invalid input. Press Enter...",
            "rastrear_spotify": "Spotify detected, searching YouTube...",
            "rastrear_yt_link": "YouTube detected, preparing download...",
            "rastrear_platforms": "Supported platforms:",
            "rastrear_any_link": "Or any link / song name",
            "rastrear_scraping": "Scanning site for audio files...",
            "rastrear_found_files": "Audio files found:",
            "rastrear_no_files": "No files found, searching YouTube...",
            "choose_prompt": "Choose an option:",
            "other_platforms": "other platforms/links",
            "loading": "Loading",
            "full_title": "DOWNLOAD MODE",
            "full_opt_full": "Full",
            "full_opt_full_m": "Full",
            "full_opt_cut": "Cut",
            "full_opt_cut_v": "Cut",
            "dl_error": "Error preparing download",
            "dl_not_found": "File not found",
            "dl_cut_error": "Error cutting",
            "playlist_single": "Download just this song",
            "playlist_all": "Download full playlist",
            "playlist_detected": "PLAYLIST DETECTED!",
            "playlist_split": "Playlist with {0} songs. Split into {1} parts.",
            "playlist_part": "Part {0}/{1}: {2} songs",
            "playlist_downloading": "Downloading part {0}/{1}...",
        }

def download_playlist_generic(url, default_name):
    playlist_name = extract_track(url) or default_name
    playlist_dir = MUSIC_DIR / playlist_name
    playlist_dir.mkdir(parents=True, exist_ok=True)
    playlist_count = get_playlist_size(url)
    output = playlist_dir / "%(title)s.%(ext)s"
    cmd = [YTDLP, "-x", "--audio-format", "mp3",
           "--audio-quality", "0",
           "-o", str(output),
           "--embed-thumbnail", "--add-metadata",
           "--remote-components", "ejs:github"]
    print()
    if not ask_confirm():
        return False
    if playlist_count > 150:
        chunks = split_playlist(url)
        print(f"\n  \033[1;33m{LANG.get('playlist_split', 'Playlist com {0} musicas. Dividida em {1} partes.').format(playlist_count, len(chunks))}\033[0m")
        for i, (chunk_url, chunk_size) in enumerate(chunks, 1):
            print(f"  \033[1;36m{LANG.get('playlist_part', 'Parte {0}/{1}: {2} musicas').format(i, len(chunks), chunk_size)}\033[0m")
        for i, (chunk_url, chunk_size) in enumerate(chunks, 1):
            chunk_cmd = cmd.copy()
            chunk_cmd.append(chunk_url)
            print(f"\n  \033[1;33m{LANG.get('playlist_downloading', 'A descarregar parte {0}/{1}...').format(i, len(chunks))}\033[0m")
            subprocess.run(chunk_cmd)
    else:
        cmd.append(url)
        print(f"\n  \033[1;33mDownload em andamento, por favor Aguarde...\033[0m")
        subprocess.run(cmd)
    clean_thumbnails(playlist_dir)
    print()
    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
    print()
    print(f"  \033[1;32m✓ Download Concluido com Sucesso!\033[0m")
    print()
    print(f"  \033[1;35m♪ ♫ Playlist guardada em:\033[0m")
    print(f"  \033[1;32m✓ {playlist_dir}\033[0m")
    print()
    try:
        musicas = sum(1 for f in playlist_dir.iterdir() if f.is_file())
        print(f"  \033[1;36m✓ Foi efetuado o download de: {musicas} musicas.\033[0m")
    except Exception:
        pass
    print()
    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
    return True

def open_folder(path):
    try:
        subprocess.run(["explorer", str(path)], check=False)
    except Exception:
        try:
            os.startfile(str(path))
        except Exception:
            subprocess.run(["cmd", "/c", "start", "", str(path)], check=False)

def after_open_prompt():
    print()
    print(f"  \033[1;36m→ Pasta aberta.\033[0m")
    print()
    print(f"  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[1;36m│\033[0m [\033[1;33m1\033[0m] {LANG.get('post_back', 'Voltar ao menu principal')}")
    print(f"  \033[1;36m│\033[0m [\033[1;31m2\033[0m] EXIT")
    print(f"  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
    print()
    after = input(f"  \033[38;5;208m[ ]\033[0m {LANG.get('choose_prompt', 'Choose:')} \033[38;5;208m>\033[0m ").strip()
    if after == "2":
        print(f"\n  \033[1;35m{LANG['goodbye']}\033[0m\n")
        sys.exit(0)

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def ensure_folder():
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)

def header():
    print("  \033[1;36m╔═══════════════════════════════════════════════════════╗\033[0m")
    print("  \033[1;36m║\033[0m                  \033[1;35mK A M I K A  v2.1\033[0m                  \033[1;36m║\033[0m")
    print("  \033[1;36m╚═══════════════════════════════════════════════════════╝\033[0m")

def loading_animation(text, duration=2):
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  \033[1;33m{spinner[i % len(spinner)]} {text}...\033[0m  ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  \033[1;32m✓\033[0m {text}!\033[2K\n")
    sys.stdout.flush()

def checkbox_select(options, colors, show_loading=True, show_back=True):
    prompt = LANG.get('choose_prompt', 'Choose:')
    valid = [str(i) for i in range(1, len(options) + 1)]
    if show_back:
        valid.append("0")
    while True:
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        for i, (opt, color) in enumerate(zip(options, colors), 1):
            print(f"  \033[1;36m│\033[0m [{i}] {color}{opt}\033[0m")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        if show_back:
            print()
            print(f"  [0] \033[1;31m{LANG['back']}\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m {prompt} \033[38;5;208m>\033[0m ").strip()
        if choice in valid:
            break
        print()
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31m{LANG.get('invalid_opt', 'Invalid option.')}\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print()

    if choice == "0":
        return "0"

    if show_loading:
        loading_text = LANG.get('loading', 'Loading')
        loading_animation(f"{loading_text}... {choice}", 2)
    return choice

def fmt_time(t):
    return t if t else t

def parse_time(t):
    t = t.strip()
    if not t:
        return None
    m = re.match(r'^(\d+):(\d{2})$', t)
    if m:
        return f"00:{m.group(1)}:{m.group(2)}"
    return None

def ask_full_or_cut(media_type="music"):
    prompt = LANG.get('choose_prompt', 'Choose:')
    full_text = LANG['full_opt_full'] if media_type == "music" else LANG.get('full_opt_full_m', 'Completo')
    cut_text = LANG['full_opt_cut'] if media_type == "music" else LANG.get('full_opt_cut_v', 'Cortar')
    while True:
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print(f"  \033[1;36m│\033[0m  \033[1;36m{LANG['full_title']}\033[0m")
        print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
        print(f"  \033[1;36m│\033[0m [\033[1;33m1\033[0m] {full_text}")
        print(f"  \033[1;36m│\033[0m [\033[1;33m2\033[0m] {cut_text}")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        print(f"  [0] \033[1;31m{LANG['back']}\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m {prompt} \033[38;5;208m>\033[0m ").strip()
        if choice in ("0", "1", "2"):
            return choice
        print()
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31m{LANG.get('invalid_opt', 'Invalid option.')}\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print()

def ask_time():
    while True:
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print(f"  \033[1;36m│\033[0m  \033[1;36m{LANG['time_header']}\033[0m")
        print(f"  \033[1;36m│\033[0m  {LANG['time_fmt']}")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()

        start = input(f"  \033[38;5;208m[ ]\033[0m {LANG['ask_start']}").strip()
        if start == "0":
            return None
        start_t = parse_time(start) if start else None
        if start and not start_t:
            print()
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print(f"  \033[1;31m{LANG['time_invalid']}\033[0m")
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print()
            continue

        end = input(f"  \033[38;5;208m[ ]\033[0m {LANG['ask_end']}").strip()
        if end == "0":
            return None
        end_t = parse_time(end) if end else None
        if end and not end_t:
            print()
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print(f"  \033[1;31m{LANG['time_invalid']}\033[0m")
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print()
            continue

        return start_t, end_t

QUALITY_NAMES = {
    "1": "Melhor Qualidade (4K, 60fps, HDR)",
    "2": "HD (1080p)",
    "3": "Media (720p)",
}

QUALITY_FORMATS = {
    "1": [
        "bestvideo+bestaudio/best",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    ],
    "2": [
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "bestvideo+bestaudio/best",
        "18",
    ],
    "3": [
        "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    ],
}

QUALITY_MERGE = {
    "1": "",
    "2": "mp4",
    "3": "mp4",
}

def ask_video_quality():
    prompt = LANG.get('choose_prompt', 'Choose:')
    while True:
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print("  \033[1;36m│\033[0m              \033[1;36mQUALIDADE DO VIDEO\033[0m")
        print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
        print(f"  \033[1;36m│\033[0m [1] \033[1;33m{QUALITY_NAMES['1']}\033[0m")
        print(f"  \033[1;36m│\033[0m [2] \033[1;32m{QUALITY_NAMES['2']}\033[0m")
        print(f"  \033[1;36m│\033[0m [3] \033[1;34m{QUALITY_NAMES['3']}\033[0m")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        print(f"  [0] \033[1;31m{LANG['back']}\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m {prompt} \033[38;5;208m>\033[0m ").strip()
        if choice in ("0", "1", "2", "3"):
            return choice
        print()
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31m{LANG.get('invalid_opt', 'Invalid option.')}\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print()

def try_download_with_quality(load_dir, url, quality="2", start_t=None, end_t=None):
    q = QUALITY_FORMATS.get(quality, QUALITY_FORMATS["2"])
    merge_format = QUALITY_MERGE.get(quality, "mp4")
    q_name = QUALITY_NAMES.get(quality, "HD (1080p)")
    print(f"\n  \033[1;33m┌{'─' * 53}┐\033[0m")
    print(f"  \033[1;33m│\033[0m  Download em andamento, por favor Aguarde...")
    print(f"  \033[1;33m│\033[0m  Qualidade: {q_name}")
    print(f"  \033[1;33m└{'─' * 53}┘\033[0m\n")
    for fmt in q:
        output = load_dir / "%(title)s.%(ext)s"
        cmd = [YTDLP, "--no-playlist", "-f", fmt, "-o", str(output)]
        if merge_format:
            cmd += ["--merge-output-format", merge_format]
        cmd += ["--extractor-retries", "3", "--retries", "10",
                "--throttled-rate", "100K"]
        cmd.append(url)
        log_msg(f"Video download: qualidade {quality}, formato: {fmt}")
        print(f"  \033[1;33m→\033[0m A tentar: {fmt}")
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"  \033[1;32m✓\033[0m Download concluido!\n")
            return True
        log_msg(f"Formato {fmt} falhou (code {result.returncode})")
    print(f"\n  \033[1;31m✗ Nao foi possivel descarregar o video.\033[0m\n")
    return False

def build_time_args(cmd, start_t, end_t):
    if start_t and end_t:
        cmd += ["--download-sections", f"*{start_t}-{end_t}"]
    elif start_t:
        cmd += ["--download-sections", f"*{start_t}-"]
    elif end_t:
        cmd += ["--download-sections", f"*00:00:00-{end_t}"]

def show_download_info(start_t, end_t, output_dir, url, color, media_type="music"):
    prefix = "dl_music" if media_type == "music" else "dl_video"
    print()
    print()
    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
    print()
    if start_t and end_t:
        print(f"  {color}→\033[0m {LANG[f'{prefix}_between'].format(fmt_time(start_t), fmt_time(end_t))}")
    elif start_t:
        print(f"  {color}→\033[0m {LANG[f'{prefix}_from'].format(fmt_time(start_t))}")
    elif end_t:
        print(f"  {color}→\033[0m {LANG[f'{prefix}_until'].format(fmt_time(end_t))}")
    else:
        print(f"  {color}→\033[0m {LANG[f'{prefix}_full']}")
    print(f"  {color}→\033[0m {LANG['dl_to']} {output_dir}")
    print()
    print(f"  \033[1;33m{url}\033[0m")
    print()
    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")

def post_download_menu():
    prompt = LANG.get('choose_prompt', 'Choose:')
    while True:
        print()
        print()
        print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
        print()
        print(f"  \033[1;32m✓\033[0m \033[1;32m{LANG['done']}\033[0m")
        print()
        print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print(f"  \033[1;36m│\033[0m  \033[1;37m{LANG['post_title_now']}\033[0m")
        print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
        print(f"  \033[1;36m│\033[0m [\033[1;33m1\033[0m] {LANG['post_open']}")
        print(f"  \033[1;36m│\033[0m [\033[1;33m2\033[0m] {LANG['post_back']}")
        print(f"  \033[1;36m│\033[0m [\033[1;31m3\033[0m] {LANG['post_exit']}")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m {prompt} \033[38;5;208m>\033[0m ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print()
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31m{LANG.get('invalid_opt', 'Invalid option.')}\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print()

def do_download(url, opt, file_name=None, skip_mode=False):
    ensure_folder()
    try:
        return _do_download_internal(url, opt, file_name, skip_mode)
    except Exception as e:
        print(f"\n  \033[1;31m✗ Erro: {e}\033[0m")
        import traceback
        traceback.print_exc()
        return False

def _do_download_internal(url, opt, file_name=None, skip_mode=False):
    while True:
        if skip_mode:
            mode = "1"
            start_t, end_t = None, None
        else:
            mode = ask_full_or_cut("music" if opt == "1" else "video")
            if mode == "0":
                return None

            start_t, end_t = None, None
            if mode == "2":
                result = ask_time()
                if result is None:
                    return None

                start_t, end_t = result

        load_dir = start_loading()

        if opt == "1":
            suffix = " (Cortada)" if mode == "2" else ""
            output = load_dir / f"%(title)s{suffix}.%(ext)s"
            cmd = [
                YTDLP, "-x", "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", str(output),
                "--embed-thumbnail", "--add-metadata",
                "--remote-components", "ejs:github",
            ]
            final_dir = MUSIC_DIR
            color = "\033[1;32m"
            log_msg(f"URL: {url[:80]} | is_playlist: {is_playlist(url)} | mode: {mode}")
            if is_playlist(url) and mode == "1":
                playlist_choice = ask_playlist_option(url)
                if playlist_choice == "1":
                    cmd.insert(1, "--no-playlist")
                elif playlist_choice == "2":
                    playlist_name = get_playlist_name(url)
                    playlist_dir = final_dir / playlist_name
                    playlist_dir.mkdir(parents=True, exist_ok=True)
                    playlist_count = get_playlist_size(url)
                    if playlist_count > 150:
                        chunks = split_playlist(url)
                        print(f"\n  \033[1;33m{LANG.get('playlist_split', 'Playlist com {0} musicas. Dividida em {1} partes.').format(playlist_count, len(chunks))}\033[0m")
                        for i, (chunk_url, chunk_size) in enumerate(chunks, 1):
                            print(f"  \033[1;36m{LANG.get('playlist_part', 'Parte {0}/{1}: {2} musicas').format(i, len(chunks), chunk_size)}\033[0m")
                        for i, (chunk_url, chunk_size) in enumerate(chunks, 1):
                            chunk_cmd = cmd.copy()
                            chunk_cmd[chunk_cmd.index("-o") + 1] = str(playlist_dir / "%(title)s.%(ext)s")
                            chunk_cmd.append(chunk_url)
                            print(f"\n  \033[1;33m{LANG.get('playlist_downloading', 'A descarregar parte {0}/{1}...').format(i, len(chunks))}\033[0m")
                            subprocess.run(chunk_cmd)
                    else:
                        cmd[cmd.index("-o") + 1] = str(playlist_dir / "%(title)s.%(ext)s")
                        cmd.append(url)
                        print(f"\n  \033[1;33mDownload em andamento, por favor Aguarde...\033[0m")
                        subprocess.run(cmd)
                    clean_thumbnails(playlist_dir)
                    print()
                    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
                    print()
                    print(f"  \033[1;35m♪ ♫ Playlist guardada em:\033[0m")
                    print(f"  \033[1;32m✓ {playlist_dir}\033[0m")
                    print()
                    try:
                        musicas = sum(1 for f in playlist_dir.iterdir() if f.is_file())
                        print(f"  \033[1;36m✓ Foi efetuado o download de: {musicas} musicas.\033[0m")
                    except Exception:
                        pass
                    print()
                    print(f"  \033[1;38;5;206m{'─' * 53}\033[0m")
                    return True
                elif playlist_choice == "0":
                    return None
                else:
                    return None
            elif is_playlist(url) and mode == "2":
                cmd.insert(1, "--no-playlist")
            build_time_args(cmd, start_t, end_t)
            cmd.append(url)
            show_download_info(start_t, end_t, final_dir, url, color, "music")
            print()
            if not ask_confirm():
                try:
                    LOADING_DIR.rmdir()
                except Exception:
                    pass
                if skip_mode:
                    return False
                continue
            print(f"  \033[1;33mDownload em andamento, por favor Aguarde...\033[0m")
            result = subprocess.run(cmd)
            if result.returncode == 0:
                finish_loading(final_dir)
                return True
            return False
        else:
            final_dir = VIDEO_DIR
            color = "\033[1;34m"
            log_msg(f"URL: {url[:80]} | is_playlist: {is_playlist(url)} | mode: {mode}")
            if not skip_mode:
                quality = ask_video_quality()
                if quality == "0":
                    try:
                        LOADING_DIR.rmdir()
                    except Exception:
                        pass
                    return None
            else:
                quality = "2"
            show_download_info(start_t, end_t, final_dir, url, color, "video")
            print()
            if not ask_confirm():
                try:
                    LOADING_DIR.rmdir()
                except Exception:
                    pass
                if skip_mode:
                    return False
                continue
            print()
            success = try_download_with_quality(load_dir, url, quality, start_t, end_t)
            if not success:
                print(f"\n  \033[1;31m✗ {LANG.get('dl_error', 'Erro ao preparar download')}\033[0m")
                continue
            if start_t or end_t:
                pattern = str(load_dir / "*.*")
                files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
                if not files:
                    print(f"\n  \033[1;31m✗ {LANG.get('dl_not_found', 'Ficheiro nao encontrado')}\033[0m")
                    continue
                downloaded = Path(files[0])
                out_path = unique_path(final_dir / downloaded.name)
                ffmpeg_cmd = ["ffmpeg", "-y"]
                if start_t:
                    ffmpeg_cmd += ["-ss", start_t]
                ffmpeg_cmd += ["-i", str(downloaded)]
                if end_t:
                    if start_t:
                        start_parts = start_t.split(":")
                        end_parts = end_t.split(":")
                        start_sec = int(start_parts[0]) * 3600 + int(start_parts[1]) * 60 + int(start_parts[2])
                        end_sec = int(end_parts[0]) * 3600 + int(end_parts[1]) * 60 + int(end_parts[2])
                        duration = end_sec - start_sec
                        h, r = divmod(duration, 3600)
                        m, s = divmod(r, 60)
                        ffmpeg_cmd += ["-t", f"{h:02d}:{m:02d}:{s:02d}"]
                    else:
                        ffmpeg_cmd += ["-to", end_t]
                ffmpeg_cmd += ["-c", "copy", "-movflags", "+faststart", str(out_path)]
                print()
                result = subprocess.run(ffmpeg_cmd)
                if result.returncode == 0:
                    log_msg(f"Video cortado com sucesso: {out_path.name}")
                    try:
                        downloaded.unlink()
                    except Exception:
                        pass
                    try:
                        LOADING_DIR.rmdir()
                    except Exception:
                        pass
                    return True
                else:
                    log_msg(f"Erro ffmpeg ao cortar video (code {result.returncode})")
                    print(f"\n  \033[1;31m✗ {LANG.get('dl_cut_error', 'Erro ao cortar')}\033[0m")
                    try:
                        downloaded.unlink()
                    except Exception:
                        pass
                    try:
                        LOADING_DIR.rmdir()
                    except Exception:
                        pass
                    continue
            else:
                log_msg("Video completo descarregado com sucesso")
                finish_loading(final_dir)
                return True

def extract_track(url):
    result = subprocess.run(
        [YTDLP, "--flat-playlist", "-j", url],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        info = json.loads(result.stdout.strip().split('\n')[0])
        title = info.get("title", "")
        artist = info.get("artist", info.get("uploader", ""))
        if artist and title:
            return f"{artist} - {title}"
        return title
    return None

def is_playlist(url):
    """EXCEPTION: So usado no YouTube (menu_youtube + rastrear->yt link).
       As outras plataformas (Spotify, SoundCloud, Bandcamp, etc.) tem
       detecao propria em menu_rastrear() e detect_input().
       Regra geral do KAMIKA: cada plataforma trata playlists a seu modo."""
    result = "list=" in url or "playlist?" in url
    return result

def get_playlist_size(url):
    try:
        result = subprocess.run(
            [YTDLP, "--flat-playlist", "--print", "%(playlist_count)s", url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            count = int(result.stdout.strip().split('\n')[0])
            return count
    except:
        pass
    return 0

def get_playlist_name(url):
    try:
        result = subprocess.run(
            [YTDLP, "--flat-playlist", "--print", "%(playlist_title)s", url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            name = result.stdout.strip().split('\n')[0]
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                name = name.replace(char, '_')
            return name[:100]
    except:
        pass
    return "Playlist"

def split_playlist(url, chunk_size=100):
    count = get_playlist_size(url)
    if count <= 150:
        return [url]
    chunks = []
    for i in range(0, count, chunk_size):
        chunk_url = f"{url}&playlist-start={i+1}&playlist-end={min(i+chunk_size, count)}"
        chunks.append((chunk_url, min(chunk_size, count - i)))
    return chunks

def ask_playlist_option(url=None):
    count = get_playlist_size(url) if url else 0
    if count > 0:
        single = LANG.get('playlist_single', 'Download apenas desta Musica')
        all_text = f"{LANG.get('playlist_all', 'Download da Playlist completa')} ({count} {'musicas' if CURRENT_LANG == '1' else 'songs'})"
    else:
        single = LANG.get('playlist_single', 'Download apenas desta Musica')
        all_text = LANG.get('playlist_all', 'Download da Playlist completa')
    print()
    print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[1;36m│\033[0m  \033[1;33m{'PLAYLIST DETETADA!':^51}\033[0m")
    print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
    print(f"  \033[1;36m│\033[0m [1] {single}")
    print(f"  \033[1;36m│\033[0m [2] {all_text}")
    print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
    print()
    choice = input(f"  \033[38;5;208m[ ]\033[0m {LANG.get('choose_prompt', 'Choose:')} \033[38;5;208m>\033[0m ").strip()
    return choice

def detect_input(text):
    text_lower = text.lower()
    if "youtube.com" in text_lower or "youtu.be" in text_lower:
        return "youtube", None
    elif "spotify.com" in text_lower or "open.spotify.com" in text_lower:
        return "spotify", text
    elif "soundcloud.com" in text_lower:
        return "soundcloud", text
    elif "bandcamp.com" in text_lower:
        return "bandcamp", text
    elif "deezer.com" in text_lower or "deezer.page.link" in text_lower:
        return "deezer", text
    elif "tidal.com" in text_lower:
        return "tidal", text
    elif "music.apple.com" in text_lower or "itunes.apple.com" in text_lower:
        return "apple", text
    elif "audiomack.com" in text_lower:
        return "audiomack", text
    elif re.search(r'https?://', text_lower):
        return "other_site", text
    else:
        return "search", text

PLATFORM_MSG = {
    "spotify": ("spotify", "\033[1;35m"),
    "soundcloud": ("SoundCloud", "\033[1;33m"),
    "bandcamp": ("Bandcamp", "\033[1;36m"),
    "deezer": ("Deezer", "\033[1;34m"),
    "tidal": ("Tidal", "\033[1;35m"),
    "apple": ("Apple Music", "\033[1;37m"),
    "audiomack": ("Audiomack", "\033[1;33m"),
    "other_site": ("site", "\033[1;33m"),
}

def menu_youtube():
    limpar()
    header()
    print()
    print("  \033[1;37m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[1;37m│\033[0m{'YOUTUBE':^53}\033[1;37m│\033[0m")
    print("  \033[1;37m└─────────────────────────────────────────────────────┘\033[0m")
    print()
    url = input(f"  \033[1;33m?\033[0m {LANG['ask_url']}").strip()
    for prefix in ["youtube:", "youtube link:", "link do youtube:", "link:"]:
        if url.lower().startswith(prefix):
            url = url[len(prefix):].strip()
            break
    if not url:
        input(f"\n  {LANG['invalid_url']}")
        return
    url_lower = url.lower()
    if "youtube.com" not in url_lower and "youtu.be" not in url_lower and not url_lower.startswith("ytsearch"):
        print(f"\n  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31m{LANG['invalid_url']}\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        return

    print()
    while True:
        print()
        opt = checkbox_select(
            [LANG['opt_music'], LANG['opt_video']],
            ["\033[1;32m", "\033[1;34m"],
            show_loading=False
        )

        if opt == "0":
            return

        result = do_download(url, opt, url[:50])
        if result is None:
            continue
        if result is False:
            print(f"\n  \033[1;31m✗ Download falhou\033[0m")
            input(f"\n  {LANG.get('press_enter', 'Prima Enter para continuar...')}")
            continue
        if result:
            choice = post_download_menu()
            if choice == "1":
                open_folder(MUSIC_DIR if opt == "1" else VIDEO_DIR)
                after_open_prompt()
            elif choice == "2":
                pass
            elif choice == "3":
                print(f"\n  \033[1;35m{LANG['goodbye']}\033[0m\n")
                sys.exit(0)
            return True
        return True

def menu_rastrear():
    limpar()
    header()
    print()
    print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[1;36m│\033[0m              \033[1;35m{LANG['rastrear_title']}\033[0m")
    print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
    print(f"  \033[1;36m│\033[0m  {LANG['rastrear_platforms']}")
    print("  \033[1;36m│\033[0m  YouTube / Spotify / SoundCloud / Bandcamp")
    print("  \033[1;36m│\033[0m  Deezer / Tidal / Apple Music / Audiomack")
    print(f"  \033[1;36m│\033[0m  {LANG['rastrear_any_link']}")
    print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
    print()
    query = input(f"  \033[1;33m?\033[0m {LANG['rastrear_ask']}").strip()
    for prefix in ["youtube:", "youtube link:", "link do youtube:", "link:", "link ou nome da musica:"]:
        if query.lower().startswith(prefix):
            query = query[len(prefix):].strip()
            break
    if not query:
        input(f"\n  {LANG['rastrear_invalid']}")
        return

    input_type, original_url = detect_input(query)
    track_name = None

    if input_type == "youtube":
        print(f"\n  → {LANG['rastrear_yt_link']}")
        url = query
        file_name = query[:50]
        result = do_download(url, "1", file_name, skip_mode=True)
        if result is False:
            print(f"\n  \033[1;31m✗ Download falhou\033[0m")
            input(f"\n  {LANG.get('press_enter', 'Prima Enter para continuar...')}")
            return True
        if result:
            choice = post_download_menu()
            if choice == "1":
                open_folder(MUSIC_DIR)
            elif choice == "2":
                return True
            elif choice == "3":
                print(f"\n  \033[1;35m{LANG['goodbye']}\033[0m\n")
                sys.exit(0)
        return True

    if input_type == "spotify":
        if "/playlist/" in query:
            print(f"\n  → Playlist Spotify detetada!")
            playlist_choice = ask_playlist_option(query)
            if playlist_choice == "1":
                track_name = extract_track(query)
                if track_name:
                    query = track_name
                else:
                    input(f"\n  {LANG['rastrear_invalid']}")
                    return
            elif playlist_choice == "2":
                return download_playlist_generic(query, "Spotify Playlist")
            else:
                return None
        else:
            print(f"\n  → {LANG['rastrear_spotify']}")
            track_name = extract_track(query)
            if not track_name:
                input(f"\n  {LANG['rastrear_invalid']}")
                return
            print(f"  ♪ {track_name}")
            query = track_name

    elif input_type in PLATFORM_MSG:
        name, color = PLATFORM_MSG[input_type]
        print(f"\n  {color}→ Link do {name} detectado\033[0m")
        if "/sets/" in original_url or "/playlist/" in original_url:
            print(f"  → Playlist {name} detetada!")
            playlist_choice = ask_playlist_option(original_url)
            if playlist_choice == "1":
                track_name = extract_track(original_url)
                if track_name:
                    print(f"  ♪ {track_name}")
                else:
                    input(f"\n  {LANG['rastrear_invalid']}")
                    return
            elif playlist_choice == "2":
                return download_playlist_generic(original_url, f"{name} Playlist")
            else:
                return None
        else:
            track_name = extract_track(original_url)
            if track_name:
                print(f"  ♪ {track_name}")
            if input_type in ("soundcloud", "bandcamp", "audiomack"):
                print(f"  → A preparar download do {name}...")
                url = original_url
                file_name = track_name
                ensure_folder()
                load_dir = start_loading()
                output = load_dir / "%(title)s.%(ext)s"
                cmd = [YTDLP, "--no-playlist", "-x", "--audio-format", "mp3",
                       "--audio-quality", "0",
                       "-o", str(output),
                       "--embed-thumbnail", "--add-metadata",
                       "--remote-components", "ejs:github", url]
                print()
                if not ask_confirm():
                    try: LOADING_DIR.rmdir()
                    except Exception: pass
                    return False
                print(f"  \033[1;33mDownload em andamento, por favor Aguarde...\033[0m")
                result = subprocess.run(cmd)
                if result.returncode == 0:
                    finish_loading(MUSIC_DIR)
                    choice = post_download_menu()
                    if choice == "1":
                        open_folder(MUSIC_DIR)
                        after_open_prompt()
                    elif choice == "2":
                        pass
                    elif choice == "3":
                        print(f"\n  \033[1;35m{LANG['goodbye']}\033[0m\n")
                        sys.exit(0)
                return True
            else:
                print(f"  → {name} nao suportado, a procurar no YouTube...")
                query = track_name
    else:
        print(f"  → A procurar no YouTube...")

    url = f"ytsearch1:{query}"
    file_name = track_name or query[:50]
    ensure_folder()
    load_dir = start_loading()
    output = load_dir / "%(title)s.%(ext)s"
    cmd = [YTDLP, "-x", "--audio-format", "mp3",
           "--audio-quality", "0",
           "-o", str(output),
           "--embed-thumbnail", "--add-metadata",
           "--remote-components", "ejs:github", url]
    print()
    if not ask_confirm():
        try: LOADING_DIR.rmdir()
        except Exception: pass
        return False
    print(f"  \033[1;33mDownload em andamento, por favor Aguarde...\033[0m")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        finish_loading(MUSIC_DIR)
        choice = post_download_menu()
        if choice == "1":
            open_folder(MUSIC_DIR)
            after_open_prompt()
        elif choice == "2":
            pass
        elif choice == "3":
            print(f"\n  \033[1;35m{LANG['goodbye']}\033[0m\n")
            sys.exit(0)
    return True

def main_menu():
    limpar()
    header()
    print()
    print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
    print(f"  \033[1;36m│\033[0m              \033[1;36m{LANG['menu_title']}\033[0m")
    print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
    print()
    print()
    opt = checkbox_select(
        [LANG['main_opt1'],
         f"{LANG['main_opt2']}   \033[1;37m({LANG['other_platforms']})\033[0m"],
        ["\033[1;34m", "\033[1;35m"]
    )
    if opt == "1":
        menu_youtube()
    elif opt == "2":
        menu_rastrear()
    elif opt == "0":
        choose_lang()
    else:
        print(f"\n  {LANG['invalid_opt']}")
        input(f"\n  {LANG['press_enter']}")

def menu_ajuda():
    while True:
        limpar()
        header()
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print("  \033[1;36m│\033[0m                   \033[1;33mHELP\033[0m")
        print("  \033[1;36m├─────────────────────────────────────────────────────┤\033[0m")
        print("  \033[1;36m│\033[0m [1] \033[1;33mRepair KAMIKA\033[0m")
        print("  \033[1;36m│\033[0m [2] \033[1;31mUninstall KAMIKA\033[0m")
        print("  \033[1;36m│\033[0m [3] \033[1;35mCredits\033[0m")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        print("  [0] \033[1;36mBack\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m Choose: \033[38;5;208m>\033[0m ").strip()
        if choice == "0":
            return
        if choice == "1":
            # Repair - verifica yt-dlp, ffmpeg, atalho, pastas
            print(f"\n  \033[1;33m→\033[0m Checking KAMIKA installation...\n")
            # Verificar yt-dlp
            yt_found = shutil.which("yt-dlp")
            if yt_found:
                print(f"  \033[1;32m✓\033[0m yt-dlp: found")
            else:
                print(f"  \033[1;33m!\033[0m yt-dlp: NOT found - run install.bat to install")
            # Verificar ffmpeg
            ff_found = shutil.which("ffmpeg")
            if ff_found:
                print(f"  \033[1;32m✓\033[0m ffmpeg: found")
            else:
                print(f"  \033[1;33m!\033[0m ffmpeg: NOT found - required for MP3 and cutting")
            # Verificar atalho
            shortcut = Path.home() / "Desktop" / "KAMIKA START.lnk"
            if shortcut.exists():
                print(f"  \033[1;32m✓\033[0m Desktop shortcut: OK")
            else:
                print(f"  \033[1;33m!\033[0m Desktop shortcut: missing")
            print()
            input(f"  \033[1;33mPress Enter to continue...\033[0m")
        elif choice == "2":
            desinstalar_path = SCRIPT_DIR / "uninstall" / "desinstalar.bat"
            if desinstalar_path.exists():
                print(f"\n  \033[1;33m→\033[0m Opening uninstaller...\n")
                subprocess.run([str(desinstalar_path)], shell=True)
                print()
                input(f"  \033[1;33mPress Enter to continue...\033[0m")
            else:
                print(f"\n  \033[1;31m\u2717 Uninstall file not found.\033[0m")
                input(f"  \033[1;33mPress Enter...\033[0m")
        elif choice == "3":
            print()
            print("  \033[1;36m╔═══════════════════════════════════════════════════════╗\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m██╗  ██╗  █████╗  ███╗   ███╗  ██╗  ██████╗  █████╗\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m██║ ██╔╝ ██╔══██╗ ████╗ ████║ ██║ ██╔════╝ ██╔══██╗\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m█████╔╝  ███████║ ██╔████╔██║ ██║ ██║      ███████║\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m██╔═██╗  ██╔══██║ ██║╚██╔╝██║ ██║ ██║      ██╔══██║\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m██║  ██╗ ██║  ██║ ██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m \033[1;33m╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝\033[0m \033[1;36m║\033[0m")
            print("  \033[1;36m║\033[0m   \033[1;37mv2.1  —  Universal Music / Video Downloader\033[0m    \033[1;36m║\033[0m")
            print("  \033[1;36m╠═══════════════════════════════════════════════════════╣\033[0m")
            print("  \033[1;36m║\033[0m  \033[1;32m●\033[0m \033[1;37mFormats:\033[0m  MP3  /  MP4  /  MKV")
            print("  \033[1;36m║\033[0m  \033[1;32m●\033[0m \033[1;37mAudio:\033[0m    Maximum quality (--audio-quality 0)")
            print("  \033[1;36m║\033[0m  \033[1;32m●\033[0m \033[1;37mVideo:\033[0m    3 quality levels with auto fallback")
            print("  \033[1;36m║\033[0m  \033[1;32m●\033[0m \033[1;37mCut:\033[0m      Audio and video trimming")
            print("  \033[1;36m║\033[0m  \033[1;32m●\033[0m \033[1;37mPlaylist:\033[0m  Full download + auto-split over 150")
            print("  \033[1;36m╠═══════════════════════════════════════════════════════╣\033[0m")
            print("  \033[1;36m║\033[0m  \033[1;35mPlatforms:\033[0m  YouTube  |  Spotify  |  SoundCloud")
            print("  \033[1;36m║\033[0m             Bandcamp  |  Deezer  |  Tidal  |  Apple")
            print("  \033[1;36m║\033[0m             Audiomack  |  any link or search")
            print("  \033[1;36m╠═══════════════════════════════════════════════════════╣\033[0m")
            print("  \033[1;36m║\033[0m  \033[1;36mEngine:\033[0m  yt-dlp + ffmpeg")
            print("  \033[1;36m║\033[0m  \033[1;36mPython:\033[0m  stdlib (no external dependencies)")
            print("  \033[1;36m╠═══════════════════════════════════════════════════════╣\033[0m")
            print("  \033[1;36m║\033[0m            \033[1;35mCreated by KAPA  ⚡  2025-2026\033[0m             \033[1;36m║\033[0m")
            print("  \033[1;36m╚═══════════════════════════════════════════════════════╝\033[0m")
            print()
            input(f"  \033[1;33mPress Enter to continue...\033[0m")
        else:
            print()
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print(f"  \033[1;31mInvalid option\033[0m")
            print(f"  \033[1;31m{'─' * 53}\033[0m")
            print()
            input(f"  \033[1;33mPress Enter...\033[0m")

def choose_lang():
    while True:
        limpar()
        header()
        print()
        print("  \033[1;38;5;206m")
        print("     ██╗  ██╗  █████╗  ███╗   ███╗  ██╗  ██████╗  █████╗ ")
        print("     ██║ ██╔╝ ██╔══██╗ ████╗ ████║ ██║ ██╔════╝ ██╔══██╗")
        print("     █████╔╝  ███████║ ██╔████╔██║ ██║ ██║      ███████║")
        print("     ██╔═██╗  ██╔══██║ ██║╚██╔╝██║ ██║ ██║      ██╔══██║")
        print("     ██║  ██╗ ██║  ██║ ██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║")
        print("     ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝\033[0m")
        print()
        print("  \033[1;33m            ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫\033[0m")
        print()
        print()
        print()
        print("  \033[1;36m┌─────────────────────────────────────────────────────┐\033[0m")
        print("  \033[1;36m│\033[0m [1] \033[1;32mPortugues\033[0m")
        print("  \033[1;36m│\033[0m [2] \033[1;34mEnglish\033[0m")
        print("  \033[1;36m│\033[0m [3] \033[1;33mHelp\033[0m")
        print("  \033[1;36m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        print("  [0] \033[1;31mExit\033[0m")
        print()
        choice = input(f"  \033[38;5;208m[ ]\033[0m Choose an option: \033[38;5;208m>\033[0m ").strip()

        if choice == "0":
            print(f"\n  Goodbye!\n")
            sys.exit(0)

        if choice in ("1", "2"):
            loading_animation(f"Loading... {choice}", 2)
            set_lang(choice)
            return

        if choice == "3":
            menu_ajuda()
            continue

        print()
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print(f"  \033[1;31mCHOOSE A VALID OPTION\033[0m")
        print(f"  \033[1;31m{'─' * 53}\033[0m")
        print()
        input("  Press Enter...")

if __name__ == "__main__":
    try:
        if CURRENT_LANG:
            set_lang(CURRENT_LANG)
        else:
            choose_lang()
        while True:
            main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  \033[1;31m✗ Erro inesperado: {e}\033[0m")
        import traceback
        traceback.print_exc()
        input("\n  Prima Enter para continuar...")

