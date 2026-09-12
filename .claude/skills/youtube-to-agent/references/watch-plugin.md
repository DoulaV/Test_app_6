# Systems 1 and 2: the ingestion tools

## System 1: the `/watch` plugin

Repository: https://github.com/bradautomates/claude-video (MIT). It downloads a
video with yt-dlp, extracts frames with ffmpeg, pulls captions (or falls back to
a Whisper API when there are none), and hands frames plus transcript to Claude.

Install inside Claude Code (auto-updates through the marketplace):

```
/plugin marketplace add bradautomates/claude-video
/plugin install watch@claude-video
```

Other hosts (Codex, Cursor, Copilot, Gemini CLI): `npx skills add bradautomates/claude-video -g`

Manual: `git clone https://github.com/bradautomates/claude-video.git && ln -s "$(pwd)/claude-video/skills/watch" ~/.claude/skills/watch`

### Usage

```
/watch <URL|local-path> <question> [flags]
```

Sources: YouTube, TikTok, Loom, X, Instagram, Vimeo, local `.mp4 .mov .mkv .webm`.

| Flag | Use it for |
|---|---|
| `--resolution 1024` | Readable terminal and code text. Default 512 is too low for tutorials. |
| `--start 2:15 --end 2:45` | Dense frames over one section. Use after a "sparse scan" warning. |
| `--detail transcript\|efficient\|balanced\|token-burner` | Frame budget. `balanced` is default (up to 100 frames); `token-burner` is uncapped. |
| `--max-frames N` | Tighter budget. |
| `--timestamps 0:30,1:10` | Grab specific moments. |
| `--whisper groq\|openai` / `--no-whisper` | Force or disable API transcription. Keys live in `~/.config/watch/.env` as `GROQ_API_KEY` or `OPENAI_API_KEY`. Not needed when captions exist. |
| `--out-dir DIR` | Keep the work dir. Without it the skill cleans up after answering. |
| `--no-dedup` | Keep near-duplicate frames. |

Default frame budget by duration: under 30s about 30 frames, 1 to 3 min about
60, 3 to 10 min about 80, over 10 min capped at 100 with a sparse-scan warning.

### Report format

```
# watch: video report
- **Source:** ...
- **Title:** ...
- **Duration:** MM:SS (Ns)
- **Detail:** balanced
- **Frames:** N selected from M
## Frames
Frames live at: `/tmp/watch-xxxx/frames`
- `/tmp/watch-xxxx/frames/....jpg` (t=MM:SS, reason=scene-change)
## Transcript
```(timestamped lines)```
_Work dir: `/tmp/watch-xxxx`, delete when done._
```

`scripts/local_ingest.py` writes the same shape, so the analysis step treats
both identically.

### Captions without any plugin or key

```bash
yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en --sub-format vtt -o "%(id)s" "<url>"
```

Speech only. Say so in the report.

## System 2: a free Gemini API key from Google AI Studio

Gemini reads public YouTube URLs natively, with no download step. That makes it
a cheap second witness for every YouTube source.

1. Open https://aistudio.google.com/apikey (Google AI Studio, left sidebar
   under Project: "API Keys").
2. Create a key. The free tier allows up to 8 hours of YouTube video per day
   and only public videos.
3. Store it where `scripts/gemini_watch.py` and `scripts/setup.py` look:

```bash
export GEMINI_API_KEY=...                       # this shell
mkdir -p ~/.config/youtube-to-agent && echo "GEMINI_API_KEY=..." >> ~/.config/youtube-to-agent/.env   # persistent
```

Model defaults to `gemini-flash-latest` (an alias Google keeps pointed at the current Flash model, so it does not go stale); override with `GEMINI_MODEL` or
`--model`. The script tries the `interactions` endpoint first and falls back
to `generateContent`, so it survives either API generation.

Request shape (for reference, the script does this for you):

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"gemini-flash-latest","input":[{"type":"text","text":"..."},{"type":"video","uri":"https://www.youtube.com/watch?v=..."}]}'
```

`--mode transcript` returns near-verbatim timestamped speech with on-screen
text quoted on `[MM:SS SCREEN]` lines; use it when captions cannot be
fetched. `--question "..."` weights the beats mode toward the target
capability.

Never paste the key into chat, the repo, the spec, or a generated skill.
