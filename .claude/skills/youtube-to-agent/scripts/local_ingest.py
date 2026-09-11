#!/usr/bin/env python3
"""Fallback for System 1 when the /watch plugin is not installed.

Takes a local video file, extracts one frame every N seconds and a timestamped
transcript (local Whisper via faster-whisper), and writes a report.md in the
same shape /watch produces so the analysis step does not care which path ran.

Usage:
  python3 local_ingest.py <video-file> --out-dir DIR [--interval 2] [--width 1280]
                          [--whisper-model small] [--captions FILE.vtt] [--no-transcript] [--no-install]

--captions skips Whisper and uses a caption file (for example one fetched by
fetch_captions.py), which is faster and usually more accurate for speech.

Dependencies are pip-installed on first run unless --no-install is given:
  imageio-ffmpeg (bundled ffmpeg binary), faster-whisper (transcription).
A system ffmpeg is used when present.
"""
import argparse
import importlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def ensure(module, package, allow_install):
    try:
        return importlib.import_module(module)
    except ImportError:
        if not allow_install:
            sys.exit(f"Missing python module {module}. Install with: pip install {package}")
        print(f"Installing {package} ...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", package], check=True)
        return importlib.import_module(module)


def ffmpeg_path(allow_install):
    system = shutil.which("ffmpeg")
    if system:
        return system
    mod = ensure("imageio_ffmpeg", "imageio-ffmpeg", allow_install)
    return mod.get_ffmpeg_exe()


def fmt(seconds):
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def probe_duration(ffmpeg, video):
    proc = subprocess.run([ffmpeg, "-hide_banner", "-i", str(video)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", proc.stderr)
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--interval", type=float, default=2.0, help="seconds between frames")
    ap.add_argument("--width", type=int, default=1280, help="frame width in px (keep high for on-screen text)")
    ap.add_argument("--whisper-model", default="small", help="faster-whisper model size: tiny, base, small, medium")
    ap.add_argument("--captions", help="use this .vtt/.srt file for the transcript instead of running Whisper")
    ap.add_argument("--no-transcript", action="store_true")
    ap.add_argument("--no-install", action="store_true", help="fail instead of pip-installing missing deps")
    args = ap.parse_args()

    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        sys.exit(f"Not a file: {video}")
    out = Path(args.out_dir).expanduser().resolve()
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = ffmpeg_path(not args.no_install)
    duration = probe_duration(ffmpeg, video)

    # Frames
    for old in frames_dir.glob("f_*.png"):
        old.unlink()
    subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
         "-vf", f"fps=1/{args.interval},scale={args.width}:-2", str(frames_dir / "f_%05d.png")],
        check=True,
    )
    frames = sorted(frames_dir.glob("f_*.png"))
    frame_rows = []
    for i, f in enumerate(frames):
        t = i * args.interval
        frame_rows.append({"path": str(f), "timestamp_seconds": t})

    # Transcript
    transcript_lines, transcript_source = [], "none"
    if args.captions and not args.no_transcript:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from fetch_captions import parse_vtt  # noqa: E402
        cues = parse_vtt(Path(args.captions).read_text(errors="replace"))
        transcript_lines = [f"[t={fmt(s)}] {txt}" for s, txt in cues]
        transcript_source = f"captions ({Path(args.captions).name})"
    elif not args.no_transcript:
        wav = out / "audio.wav"
        audio_ok = subprocess.run(
            [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)]
        ).returncode == 0
        if audio_ok and wav.exists() and wav.stat().st_size > 1000:
            fw = ensure("faster_whisper", "faster-whisper", not args.no_install)
            model = fw.WhisperModel(args.whisper_model, device="cpu", compute_type="int8")
            segments, _ = model.transcribe(str(wav), beam_size=5)
            for s in segments:
                transcript_lines.append(f"[t={fmt(s.start)}-{fmt(s.end)}] {s.text.strip()}")
            transcript_source = f"whisper (local faster-whisper {args.whisper_model})"
        else:
            transcript_source = "none (no audio track)"

    transcript_text = "\n".join(transcript_lines)
    (out / "transcript.txt").write_text(transcript_text + ("\n" if transcript_text else ""))
    (out / "frames.json").write_text(json.dumps(frame_rows, indent=2))

    lines = [
        "# watch: video report",
        "",
        f"- **Source:** {video}",
        f"- **Duration:** {fmt(duration)} ({duration:.1f}s)" if duration else "- **Duration:** unknown",
        f"- **Detail:** local_ingest (1 frame / {args.interval:g}s, width {args.width})",
        f"- **Frames:** {len(frames)}",
        f"- **Transcript source:** {transcript_source}",
        "",
        "## Frames",
        "",
        f"Frames live at: `{frames_dir}`",
        "",
    ]
    for row in frame_rows:
        lines.append(f"- `{row['path']}` (t={fmt(row['timestamp_seconds'])})")
    lines += ["", "## Transcript", "", "```", transcript_text or "(no transcript)", "```", "",
              f"_Work dir: `{out}`_", ""]
    report = out / "report.md"
    report.write_text("\n".join(lines))
    print(f"Wrote {report}")
    print(f"Frames: {len(frames)}  Transcript lines: {len(transcript_lines)}  Source: {transcript_source}")


if __name__ == "__main__":
    main()
