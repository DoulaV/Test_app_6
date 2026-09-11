#!/usr/bin/env python3
"""Check which of the three youtube-to-agent systems are ready.

Systems:
  1. /watch plugin (bradautomates/claude-video) or the local ingest fallback
  2. Gemini API key from Google AI Studio (GEMINI_API_KEY)
  3. The analysis framework (bundled with this skill, always present)

Usage: python3 setup.py [--json]
Exit code is 0 when at least one ingestion path works, 1 otherwise.
"""
import json
import os
import shutil
import sys
from pathlib import Path

HOME = Path.home()
ENV_FILES = [
    HOME / ".config" / "youtube-to-agent" / ".env",
    HOME / ".config" / "watch" / ".env",
]
WATCH_INSTALL = [
    "/plugin marketplace add bradautomates/claude-video",
    "/plugin install watch@claude-video",
]
GEMINI_KEY_URL = "https://aistudio.google.com/apikey"


def read_env_files():
    found = {}
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for line in path.read_text(errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            if key.startswith("export "):
                key = key[len("export "):].strip()
            found.setdefault(key, (value.strip().strip('"').strip("'"), str(path)))
    return found


def find_watch_plugin():
    """Return the path of an installed /watch skill, or None."""
    candidates = []
    for root in [HOME / ".claude" / "skills", HOME / ".claude" / "plugins"]:
        if root.is_dir():
            candidates.extend(root.rglob("SKILL.md"))
    cwd_skills = Path.cwd() / ".claude" / "skills"
    if cwd_skills.is_dir():
        candidates.extend(cwd_skills.rglob("SKILL.md"))
    for skill_md in candidates:
        if skill_md.parent.name == "watch":
            try:
                head = skill_md.read_text(errors="replace")[:600]
            except OSError:
                continue
            if "name: watch" in head:
                return str(skill_md.parent)
    return None


def python_module(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False


def main():
    as_json = "--json" in sys.argv
    env_files = read_env_files()

    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    gemini_source = "environment" if gemini_key else None
    if not gemini_key:
        for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            if key in env_files:
                gemini_key, gemini_source = env_files[key]
                break

    watch_path = find_watch_plugin()
    ffmpeg = shutil.which("ffmpeg") or (
        "imageio-ffmpeg (bundled)" if python_module("imageio_ffmpeg") else None
    )
    ytdlp = shutil.which("yt-dlp")
    whisper_local = python_module("faster_whisper")

    report = {
        "watch_plugin": {"ready": watch_path is not None, "path": watch_path, "install": WATCH_INSTALL},
        "local_ingest": {
            "ready": True,
            "ffmpeg": ffmpeg,
            "faster_whisper": whisper_local,
            "note": "Missing pieces are pip-installed on first run of local_ingest.py",
        },
        "gemini": {
            "ready": bool(gemini_key),
            "key_source": gemini_source,
            "model": os.environ.get("GEMINI_MODEL", "gemini-flash-latest"),
            "get_key": GEMINI_KEY_URL,
            "env_file": str(ENV_FILES[0]),
        },
        "yt_dlp": {"ready": ytdlp is not None, "path": ytdlp},
        "framework": {"ready": True, "path": str(Path(__file__).resolve().parent.parent / "references")},
    }
    report["any_ingestion_ready"] = bool(watch_path or gemini_key or ffmpeg)

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        def mark(ok):
            return "READY  " if ok else "MISSING"

        print("youtube-to-agent setup check")
        print(f"[{mark(report['watch_plugin']['ready'])}] System 1: /watch plugin"
              + (f"  ({watch_path})" if watch_path else ""))
        if not watch_path:
            print("           Install inside Claude Code:")
            for cmd in WATCH_INSTALL:
                print(f"             {cmd}")
        print(f"[{mark(True)}] System 1b: local ingest fallback (ffmpeg: {ffmpeg or 'will install'}, "
              f"faster-whisper: {'yes' if whisper_local else 'will install'})")
        print(f"[{mark(report['gemini']['ready'])}] System 2: Gemini API key"
              + (f"  (from {gemini_source})" if gemini_key else ""))
        if not gemini_key:
            print(f"           Get a free key at {GEMINI_KEY_URL}, then either")
            print("             export GEMINI_API_KEY=...        (shell)")
            print(f"             or add GEMINI_API_KEY=... to {ENV_FILES[0]}")
        print(f"[{mark(ytdlp is not None)}] yt-dlp (URL download and free captions)")
        if not ytdlp:
            print("           pipx install yt-dlp   or   pip install yt-dlp")
        print(f"[{mark(True)}] System 3: analysis framework ({report['framework']['path']})")
        print()
        if report["any_ingestion_ready"]:
            print("At least one ingestion path is available. Proceed to Step 1.")
        else:
            print("No ingestion path is available yet. Install /watch or add a Gemini key.")

    sys.exit(0 if report["any_ingestion_ready"] else 1)


if __name__ == "__main__":
    main()
