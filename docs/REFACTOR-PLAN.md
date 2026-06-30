# KAMIKA Refactoring Plan v2.2

## 1. Target File Structure

```
KAMIKA-PROJECT/
├── config.json              # User preferences (auto-created with defaults)
├── history.json             # Download history log
├── KAMIKA.bat               # Updated launcher (unchanged)
├── kamika.py                # Slim entry point (~40 lines)
├── requirements.txt         # Dependencies (yt-dlp, ffmpeg)
├── lib/
│   ├── __init__.py          # Empty (package marker)
│   ├── config.py            # Config loading/saving, constants, paths
│   ├── lang.py              # Language system (LANG dict, set_lang)
│   ├── ui.py                # All UI: header, checkbox_select, loading_animation, menus, prompts
│   ├── download.py          # Download logic: do_download, find_ytdlp, build_time_args, show_download_info
│   ├── platform.py          # Platform detection: detect_input, extract_track, PLATFORM_MSG
│   ├── history.py           # Download history tracking (load/save/query)
│   └── sound.py             # Sound notification helper
├── LOADING/                 # Temp dir (existing pattern, fixed)
└── docs/
    ├── README.md            # Updated
    ├── TODO.md              # Updated
    └── REFACTOR-PLAN.md     # This file
```

---

## 2. Module Contents Detail

### lib/config.py
- `VERSION = "2.2"`
- `PROJECT_DIR`, `LOADING_DIR` computed from `__file__`
- `MUSIC_DIR`, `VIDEO_DIR` loaded from config.json (default `~/Desktop/KAMIKA`)
- `load_config()` → reads config.json, creates with defaults if missing
- `save_config(cfg)` → writes config.json
- `DEFAULT_CONFIG` dict for first-run generation
- `ensure_folder()` function

### lib/lang.py
- `LANG` global dict
- `set_lang(lang_code)` → populates LANG with PT or EN strings
- All language keys from current kamika.py lines 58-210
- New keys for new features (quality, playlist, history)

### lib/ui.py
- `limpar()` — clear screen
- `header()` — ANSI box header (version from config)
- `loading_animation(text, duration)` — spinner
- `checkbox_select(options, colors, show_loading, show_back)` — menu picker
- `ask_full_or_cut(media_type)` — full vs cut prompt
- `ask_time()` — time range input
- `post_download_menu()` — post-download options
- `post_download_action(choice)` — execute post-download (open folder / exit)
- `ask_quality()` — new: quality selection menu (4 options)
- `show_playlist_menu(entries)` — new: playlist selection

### lib/download.py
- `find_ytdlp()` — locate yt-dlp executable
- `build_time_args(cmd, start_t, end_t)` — append --download-sections
- `fmt_time(t)` / `parse_time(t)` — time formatting
- `show_download_info(start_t, end_t, output_dir, url, color, media_type)` — download info display
- `do_download(url, opt, file_name, skip_mode)` — main download orchestrator
- `download_playlist(url, opt, video_ids)` — new: playlist batch download

### lib/platform.py
- `detect_input(text)` → returns (platform_type, original_url)
- `extract_track(url)` → returns track name via yt-dlp
- `PLATFORM_MSG` dict

### lib/history.py
- `load_history()` → reads history.json, returns list of dicts
- `save_history(history)` → writes history.json
- `add_entry(title, url, media_type, platform, file_path)` — append + save
- `view_history()` → display formatted history

### lib/sound.py
- `notify_complete()` — plays beep/bell on download success

### kamika.py (entry point)
- Imports from lib.*
- `main_menu()` loop
- `choose_lang()` — language picker
- `if __name__ == "__main__"` block

---

## 3. Implementation Order (Dependencies)

### Phase 1: Foundation (no behavior change)
| Step | Task | Depends On | Files |
|------|------|------------|-------|
| 1.1 | Create lib/ package with __init__.py | — | lib/__init__.py |
| 1.2 | Extract config.py (paths, constants, load/save) | 1.1 | lib/config.py |
| 1.3 | Extract lang.py (set_lang, LANG dict) | 1.1 | lib/lang.py |
| 1.4 | Extract ui.py (all UI functions) | 1.2, 1.3 | lib/ui.py |
| 1.5 | Extract download.py (do_download, helpers) | 1.2, 1.4 | lib/download.py |
| 1.6 | Extract platform.py (detect_input, extract_track) | 1.1 | lib/platform.py |
| 1.7 | Slim kamika.py to entry point | 1.3, 1.4, 1.5, 1.6 | kamika.py |
| 1.8 | Update KAMIKA.bat (still just calls kamika.py) | 1.7 | KAMIKA.bat |

**Verify Phase 1**: `python kamika.py` runs identically to before.

### Phase 2: Bug Fixes
| Step | Task | Depends On | Files |
|------|------|------------|-------|
| 2.1 | Fix LOADING_DIR.rmdir() → shutil.rmtree() | 1.5 | lib/download.py, lib/config.py |
| 2.2 | Fix --remote-components (try/except around flag) | 1.5 | lib/download.py |
| 2.3 | Add startup dependency check (yt-dlp, ffmpeg) | 1.7 | kamika.py or lib/config.py |
| 2.4 | Move json/glob imports to top of download.py | 1.5 | lib/download.py |

**Verify Phase 2**: Cancel a download — LOADING dir cleaned properly; missing deps shown clearly.

### Phase 3: Config & Preferences
| Step | Task | Depends On | Files |
|------|------|------------|-------|
| 3.1 | Auto-create config.json with defaults on first run | 1.2 | lib/config.py |
| 3.2 | Load video quality from config | 1.2 | lib/config.py |
| 3.3 | Save language choice to config.json | 1.3 | lib/config.py, lib/lang.py |
| 3.4 | Save quality choice to config.json | 3.2 | lib/config.py, lib/ui.py |

**Verify Phase 3**: Run once, check config.json created; change language, restart — persists.

### Phase 4: New Features
| Step | Task | Depends On | Files |
|------|------|------------|-------|
| 4.1 | Video quality selection menu | 3.2 | lib/ui.py, lib/download.py |
| 4.2 | Playlist detection + selection menu | 1.6, 1.5 | lib/platform.py, lib/ui.py, lib/download.py |
| 4.3 | Download history (add + view) | 1.1 | lib/history.py, lib/ui.py |
| 4.4 | Sound notification on complete | 1.1 | lib/sound.py, lib/download.py |
| 4.5 | Progress bar (yt-dlp --progress or parse) | 1.5 | lib/download.py |

**Verify Phase 4**: Each feature tested individually.

---

## 4. Key Code Patterns

### Config auto-creation
```python
# lib/config.py
DEFAULT_CONFIG = {
    "download_dir": "~/Desktop/KAMIKA",
    "video_quality": "best",
    "language": None,
    "version": "2.2"
}

def load_config():
    config_path = PROJECT_DIR / "config.json"
    if not config_path.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
```

### History entry format
```python
# lib/history.py
ENTRY = {
    "timestamp": "2026-06-26T14:30:00",
    "title": "Song Name",
    "url": "https://...",
    "type": "music",          # or "video"
    "platform": "youtube",    # or "spotify", "soundcloud", etc.
    "file_path": "/path/to/file.mp3"
}
```

### Rmdir fix pattern
```python
# Replace all: LOADING_DIR.rmdir()
# With: shutil.rmtree(LOADING_DIR, ignore_errors=True)
# Or use the existing finish_loading pattern which already handles this
```

### Remote-components guard
```python
def build_ytdlp_cmd(args, use_remote_components=True):
    cmd = [YTDLP] + args
    if use_remote_components:
        try:
            # Test if this yt-dlp version supports it
            result = subprocess.run([YTDLP, "--version"], capture_output=True, text=True)
            # Add flag with try/except at subprocess level
            cmd += ["--remote-components", "ejs:github"]
        except Exception:
            pass
    return cmd
```

### Playlist detection
```python
def is_playlist(url):
    return "playlist" in url or "list=" in url

def get_playlist_entries(url):
    cmd = [YTDLP, "--flat-playlist", "-j", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    entries = []
    for line in result.stdout.strip().split("\n"):
        if line:
            info = json.loads(line)
            entries.append({
                "id": info.get("id"),
                "title": info.get("title", "Unknown"),
                "url": f"https://www.youtube.com/watch?v={info['id']}"
            })
    return entries
```

---

## 5. Config & History File Handling

### config.json
- **Location**: `KAMIKA-PROJECT/config.json` (same dir as kamika.py)
- **Auto-create**: On first run, if missing, write DEFAULT_CONFIG
- **Load order**: config.py loads at module import time
- **Save triggers**: Language change, quality change, download dir change
- **Format**: JSON, 2-space indent, UTF-8

### history.json
- **Location**: `KAMIKA-PROJECT/history.json`
- **Auto-create**: On first entry, if missing, create empty list `[]`
- **Load**: On history view or app start
- **Save**: Append entry + write (atomic via temp file)
- **Max size**: Rotate when > 500 entries (keep last 500)
- **Format**: JSON array, 2-space indent, UTF-8

---

## 6. Verification Checklist

### Phase 1 — Modularization
- [ ] `python kamika.py` starts language picker
- [ ] YouTube music download works
- [ ] YouTube video download works
- [ ] Cut (time range) works
- [ ] Track/Rastrear menu works
- [ ] Spotify/SoundCloud detection works
- [ ] Post-download menu (open/back/exit) works
- [ ] LOADING dir created and cleaned

### Phase 2 — Bug Fixes
- [ ] Cancel download → LOADING dir fully removed (not just empty rmdir)
- [ ] --remote-components doesn't crash on older yt-dlp
- [ ] Missing yt-dlp shows clear error at startup
- [ ] Missing ffmpeg shows clear error at startup
- [ ] All imports at top of files (no function-level imports)

### Phase 3 — Config & Preferences
- [ ] First run creates config.json with defaults
- [ ] Language saved to config.json and persists across restarts
- [ ] Video quality saved to config.json
- [ ] Custom download_dir from config is respected

### Phase 4 — New Features
- [ ] Quality menu: Best/1080p/720p/480p
- [ ] Quality selection used in yt-dlp -f format string
- [ ] Playlist URL detected → menu shows entries
- [ ] Playlist: download all or select specific
- [ ] history.json created on first download
- [ ] Each download adds entry to history
- [ ] History viewable from menu
- [ ] Sound notification plays on successful download
- [ ] Progress display during download

### Integration
- [ ] KAMIKA.bat still works (calls kamika.py)
- [ ] Portuguese language works end-to-end
- [ ] English language works end-to-end
- [ ] Ctrl+C exits cleanly
- [ ] No regression in existing functionality
