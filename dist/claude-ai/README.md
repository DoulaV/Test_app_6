# Uploading these skills to normal Claude chat

These are the same six skills from `.claude/skills/`, repackaged for
claude.ai. The only difference is the YAML `description` field, which
claude.ai caps at 200 characters. The full trigger text now lives in a
"When to use this" section at the top of each SKILL.md instead, so nothing
is lost, and Claude still reads it.

Regenerate these zips after any change to the skills:

```bash
python3 dist/claude-ai/pack.py
```

## How to install

1. claude.ai, then Settings, then Capabilities, and turn on code execution.
   Skills do not appear without it.
2. Settings, then Capabilities, then Skills (shown as Customize > Skills in
   some builds).
3. Add, or the "+" then "Create skill", and upload one zip.
4. Repeat for each zip. Toggle each one on.

Each zip contains the skill folder as its root, which is the shape the
uploader expects.

## Suggested order

Upload all six content skills. `youtube-to-agent` is optional and partly
will not work outside Claude Code, because its scripts need yt-dlp, ffmpeg
and a Gemini key.

1. brand-architect
2. algorithm-strategist
3. brand-idea-miner
4. hook-writer
5. story-loop-writer
6. copy-sharpener
