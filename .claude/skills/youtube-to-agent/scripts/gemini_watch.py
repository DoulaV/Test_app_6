#!/usr/bin/env python3
"""Ask Gemini to watch a public YouTube video and produce a timestamped beat sheet.

Gemini ingests YouTube URLs natively, so no download, frame extraction, or
transcription happens on this machine. The result is written as markdown.

Usage:
  python3 gemini_watch.py <youtube-url> [--out FILE] [--question TEXT]
                          [--model MODEL] [--api auto|interactions|generate] [--raw]

Key lookup order: GEMINI_API_KEY, GOOGLE_API_KEY, then the same names in
~/.config/youtube-to-agent/.env or ~/.config/watch/.env.
Free tier limit (per Google docs): 8 hours of YouTube video per day.
"""
import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
BASE = "https://generativelanguage.googleapis.com/v1beta"
ENV_FILES = [
    Path.home() / ".config" / "youtube-to-agent" / ".env",
    Path.home() / ".config" / "watch" / ".env",
]
YOUTUBE_RE = re.compile(r"^(https?://)?(www\.|m\.)?(youtube\.com|youtu\.be)/", re.I)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "references" / "analysis-prompt.md"

FALLBACK_PROMPT = """You are watching one video so that an AI coding agent can learn the skill it teaches.
Produce a beat sheet: a markdown table with one row per beat (a beat is a change in what is on screen or a new point in the narration).
Columns: timestamp (MM:SS), on screen (describe visuals and copy any visible text, commands, URLs, filenames, settings VERBATIM), spoken (paraphrase, quote exact product and tool names), what changed since the last beat.
Then a section "Structure": how it opens, how it holds attention, where it turns, how it closes.
Then a section "Procedure": the ordered steps a person would follow to reproduce what the video teaches, each with timestamps.
Then a section "Verbatim assets": every prompt, command, config snippet, or URL shown on screen, copied exactly.
Report only what the video actually shows or says. Mark inference as (inference). Mark anything you could not read or hear as (gap).
Finish with the three highest-signal observations, each citing timestamps."""


def load_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for line in path.read_text(errors="replace").splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


TRANSCRIPT_PROMPT = """Produce a timestamped transcript of everything spoken in this video, as close to verbatim as you can.
Format: one line per 5 to 15 seconds of speech, each starting with [MM:SS]. Do not summarize, do not skip sections, do not add commentary.
Where on-screen text appears that is not spoken (titles, lists, diagrams, URLs), add a line starting with [MM:SS SCREEN] quoting it exactly.
Continue until the end of the video."""


def build_prompt(question, mode="beats"):
    if mode == "transcript":
        return TRANSCRIPT_PROMPT
    prompt = FALLBACK_PROMPT
    if PROMPT_PATH.is_file():
        text = PROMPT_PATH.read_text(errors="replace")
        # Use the verbatim prompt block from the reference if present.
        m = re.search(r"```prompt\n(.*?)```", text, re.S)
        if m:
            prompt = m.group(1).strip() + "\n\n" + (
                "Because you are ingesting the YouTube video directly rather than sampled frames, "
                "also copy every prompt, command, URL, filename and setting visible on screen VERBATIM "
                "into a final section titled 'Verbatim assets'."
            )
    if question:
        prompt += f"\n\nThe person asking wants an agent that can: {question}\nWeight the beat sheet toward that."
    return prompt


def post(url, key, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read().decode())


def collect_text(obj, out):
    """Depth-first walk that gathers every string under a 'text' key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                out.append(v)
            else:
                collect_text(v, out)
    elif isinstance(obj, list):
        for item in obj:
            collect_text(item, out)
    return out


def call_interactions(key, model, url, prompt):
    body = {"model": model, "input": [{"type": "text", "text": prompt}, {"type": "video", "uri": url}]}
    data = post(f"{BASE}/interactions", key, body)
    outputs = data.get("output") or data.get("outputs") or data
    return "\n".join(collect_text(outputs, [])).strip(), data


def call_generate(key, model, url, prompt):
    body = {"contents": [{"parts": [{"text": prompt}, {"file_data": {"file_uri": url}}]}]}
    data = post(f"{BASE}/models/{model}:generateContent", key, body)
    parts = []
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "text" in part:
                parts.append(part["text"])
    return "\n".join(parts).strip(), data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out", help="write markdown here (default: stdout)")
    ap.add_argument("--question", help="what the resulting agent should be able to do")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--api", choices=["auto", "interactions", "generate"], default="auto")
    ap.add_argument("--raw", action="store_true", help="also dump the raw JSON response next to --out")
    ap.add_argument("--mode", choices=["beats", "transcript"], default="beats",
                    help="beats (default): the analysis beat sheet; transcript: near-verbatim timestamped speech plus on-screen text, for when captions are unavailable")
    args = ap.parse_args()

    if not YOUTUBE_RE.match(args.url):
        sys.exit("gemini_watch.py only accepts public YouTube URLs. For other sources use /watch or local_ingest.py.")
    key = load_key()
    if not key:
        sys.exit(
            "No Gemini API key found. Get a free one at https://aistudio.google.com/apikey and "
            "export GEMINI_API_KEY=... or add it to ~/.config/youtube-to-agent/.env"
        )

    prompt = build_prompt(args.question, args.mode)
    order = {"auto": ["interactions", "generate"], "interactions": ["interactions"], "generate": ["generate"]}[args.api]
    text, raw, errors = "", None, []
    for api in order:
        fn = call_interactions if api == "interactions" else call_generate
        stop = False
        for attempt in range(3):  # long videos can drop the connection; retry with backoff
            try:
                text, raw = fn(key, args.model, args.url, prompt)
                if text:
                    break
                errors.append(f"{api}: empty response")
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:500]
                errors.append(f"{api}: HTTP {e.code} {detail}")
                if e.code in (401, 403):
                    stop = True  # a bad key will not get better on the fallback endpoint
                if e.code not in (429, 500, 502, 503, 504):
                    break
            except (urllib.error.URLError, TimeoutError, http.client.HTTPException, ConnectionError, OSError) as e:
                errors.append(f"{api}: attempt {attempt + 1}: {type(e).__name__}: {e}")
            if attempt < 2:
                print(f"{api}: retrying in {5 * (attempt + 1)}s ...", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        if text or stop:
            break

    if not text:
        sys.exit("Gemini returned nothing usable.\n" + "\n".join(errors))

    kind = "transcript" if args.mode == "transcript" else "watch report"
    header = f"# Gemini {kind}\n\n- **Source:** {args.url}\n- **Model:** {args.model}\n- **Note:** independent read by Gemini; reconcile against frames before trusting details.\n\n"
    output = header + text + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output)
        print(f"Wrote {out}")
        if args.raw and raw is not None:
            raw_path = out.with_suffix(".raw.json")
            raw_path.write_text(json.dumps(raw, indent=2))
            print(f"Wrote {raw_path}")
    else:
        print(output)
    if errors:
        print("Notes: " + "; ".join(errors), file=sys.stderr)


if __name__ == "__main__":
    main()
