#!/usr/bin/env python3
"""Pull a video's captions with yt-dlp and turn them into a timestamped transcript.

This is the zero-key path for URLs: no /watch plugin, no Gemini, no Whisper.
It also rescues the case where yt-dlp can fetch captions but the video stream
itself is refused (YouTube's "Sign in to confirm you're not a bot" 403, common
in cloud environments). Speech only; say so in the report.

Usage:
  python3 fetch_captions.py <url> --out-dir DIR [--lang en]
  python3 fetch_captions.py --vtt captions.vtt --out-dir DIR      # convert an existing file

Writes DIR/transcript.txt ([t=MM:SS] lines, rolling duplicates removed) and
DIR/transcript-paragraphs.txt (merged into 30-second paragraphs for reading).
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

TS = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+) --> (\d+):(\d+):(\d+)[.,](\d+)")


def fmt(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def parse_vtt(text):
    """Return [(start_seconds, text)] with YouTube's rolling-caption duplicates collapsed."""
    cues = []
    for block in re.split(r"\n\n+", text):
        m = TS.search(block)
        if not m:
            continue
        start = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        body = block[m.end():]
        body = re.sub(r"<[^>]+>", "", body)
        lines = [l.strip() for l in body.splitlines() if l.strip() and "-->" not in l]
        lines = [l for l in lines if not l.startswith(("align:", "position:", "line:"))]
        t = html.unescape(" ".join(lines)).strip()
        if not t:
            continue
        if cues and (t == cues[-1][1] or t in cues[-1][1]):
            continue
        if cues and cues[-1][1] in t:
            cues[-1] = (cues[-1][0], t)
            continue
        cues.append((start, t))
    return cues


def merge_overlap(parts):
    out = parts[0]
    for p in parts[1:]:
        k = 0
        for n in range(min(len(out), len(p)), 0, -1):
            if out.endswith(p[:n]):
                k = n
                break
        out += ("" if k else " ") + p[k:]
    return out


def paragraphs(cues, window=30):
    buckets = {}
    for s, t in cues:
        buckets.setdefault(s // window, []).append(t)
    return [(b * window, merge_overlap(buckets[b])) for b in sorted(buckets)]


def download_vtt(url, out_dir, lang):
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp is not installed. Install with: pip install yt-dlp   (or pipx install yt-dlp)")
    base = out_dir / "captions"
    cmd = ["yt-dlp", "--no-warnings", "-q", "--skip-download", "--write-sub", "--write-auto-sub",
           "--sub-lang", f"{lang}.*,{lang}", "--sub-format", "vtt", "-o", str(base), url]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    files = sorted(out_dir.glob("captions*.vtt"))
    if not files:
        sys.exit(f"No captions found for {url}.\n{proc.stderr.strip()[:800]}")
    # Prefer manual subtitles over auto-generated (yt-dlp names auto ones like captions.en-orig.vtt or captions.en.vtt).
    files.sort(key=lambda p: ("orig" in p.name, len(p.name)))
    return files[0]


def write_outputs(cues, out_dir, source):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"[t={fmt(s)}] {t}" for s, t in cues]
    (out_dir / "transcript.txt").write_text("\n".join(lines) + "\n")
    paras = [f"[{fmt(s)}] {t}" for s, t in paragraphs(cues)]
    (out_dir / "transcript-paragraphs.txt").write_text("\n\n".join(paras) + "\n")
    words = sum(len(t.split()) for _, t in cues)
    print(f"Wrote {out_dir / 'transcript.txt'} ({len(cues)} cues, about {words} words)")
    print(f"Wrote {out_dir / 'transcript-paragraphs.txt'} ({len(paras)} paragraphs)")
    print(f"Transcript source: captions ({source}). Speech only; no visual information.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    ap.add_argument("--vtt", help="convert an existing .vtt/.srt file instead of downloading")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.vtt:
        path = Path(args.vtt)
    elif args.url:
        path = download_vtt(args.url, out_dir, args.lang)
    else:
        ap.error("give a URL or --vtt FILE")
    cues = parse_vtt(path.read_text(errors="replace"))
    if not cues:
        sys.exit(f"No cues parsed from {path}")
    write_outputs(cues, out_dir, path.name)


if __name__ == "__main__":
    main()
