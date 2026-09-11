---
name: youtube-to-agent
description: Turn any YouTube tutorial, screen recording, or shared video into a working Claude Code skill or agent. Use this whenever the user shares a video URL or video file (YouTube, TikTok, Loom, Instagram, X, .mp4, .mov) and wants Claude to learn from it, "watch this and build it", "turn this tutorial into a skill", "teach my agent to do what this video does", "make an agent from this", or asks to extract a workflow, method, or SOP from a video. Also use it when the user wants to set up the three systems for video-based skill building (the /watch plugin, a Gemini API key from Google AI Studio, and the beat-sheet analysis framework), even if they never say the word "skill".
argument-hint: "<video-url-or-path> [what the agent should be able to do]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
---

# YouTube to Agent

Teach Claude Code a real-world skill by having it watch a video, reason about
what was seen and said, and distill that into a reusable skill (a folder with a
SKILL.md plus supporting files) that future sessions can invoke.

The method has three systems. Each one is a separate step below.

| System | What it gives you | Tool |
|---|---|---|
| 1. Watch | Timestamped frames and transcript of the video | `/watch` plugin (bradautomates/claude-video) or `scripts/local_ingest.py` |
| 2. Native YouTube understanding | A second, independent read of a YouTube video by a model that ingests YouTube URLs directly | `scripts/gemini_watch.py` with a free Gemini API key from Google AI Studio |
| 3. Agent framework | Turns raw frames plus transcript into a beat sheet, then into a skill | `references/analysis-prompt.md` and `references/agent-blueprint.md`, scaffolded by `scripts/scaffold_agent.py` |

Systems 1 and 2 are both optional individually, but you need at least one of
them. When both are available, use both: frames catch on-screen text (commands,
URLs, UI states) that speech never mentions, and the Gemini read catches
motion and audio nuance that sparse frame sampling misses. Disagreements
between the two are the most informative signal you will get.

## Step 0: Check the setup

Script paths below are relative to the repo root where this skill is installed
(`.claude/skills/youtube-to-agent/`). If the skill lives in `~/.claude/skills/`
instead, use that prefix.

Run the setup check first. It reports which of the three systems are ready
and prints exact install commands for anything missing.

```bash
python3 .claude/skills/youtube-to-agent/scripts/setup.py
```

Add `--json` when you want to branch on the result programmatically.

Missing pieces and what to do about them:

- **`/watch` plugin missing.** Tell the user to run these two commands inside
  Claude Code, then continue with whichever ingestion path is available:
  ```
  /plugin marketplace add bradautomates/claude-video
  /plugin install watch@claude-video
  ```
  Do not block on this. `scripts/local_ingest.py` covers local files without
  the plugin, and `scripts/gemini_watch.py` covers YouTube URLs.
- **No Gemini key.** The key is free. Point the user at
  https://aistudio.google.com/apikey (Google AI Studio, left sidebar, "API
  Keys"). They can export it as `GEMINI_API_KEY` or put
  `GEMINI_API_KEY=...` in `~/.config/youtube-to-agent/.env`. Never ask the user
  to paste the key into chat, and never write it into the repo.
- **Nothing available at all.** Fall back to captions only with
  `scripts/fetch_captions.py` (Path D below). It needs only `yt-dlp`, which
  `pip install yt-dlp` provides. Tell the user the result is speech only, with
  no visual information.

## Step 1: Watch the video

Parse the user's request into three things: the video source (URL or local
path), the target capability (what the resulting agent should be able to do),
and any constraints (where to put the skill, tools it may use). If the target
capability is unclear, infer it from the video title and confirm it in your
final report rather than stopping to ask. The user shared the video because
they want an agent that does what the video teaches.

### Path A: `/watch` plugin is installed

Invoke it with a question that forces detail, since a vague question yields a
vague summary:

```
/watch <source> Give me a complete, timestamped account of every step shown or spoken, every command, URL, filename, setting and tool visible on screen. --resolution 1024 --out-dir <workdir>
```

`--resolution 1024` matters for tutorials because on-screen code and terminal
text is unreadable at the 512px default. Use `--start` and `--end` to densify
frames over a critical section (a config screen, a command sequence) when the
first pass reports a "sparse scan". Pass `--out-dir` so the frames survive for
the analysis step instead of being auto-cleaned.

### Path B: local video file, no plugin

```bash
python3 .claude/skills/youtube-to-agent/scripts/local_ingest.py <video-file> --out-dir <workdir> [--interval 2] [--width 1280] [--captions file.vtt]
```

This extracts one frame every N seconds and transcribes the audio with a local
Whisper model (it installs `imageio-ffmpeg` and `faster-whisper` on first run
if they are missing). Pass `--captions` with a subtitle file when you have one;
it is faster and more accurate than Whisper. Pick the frame interval from the
duration: 2 seconds under 3 minutes, 5 seconds up to 10 minutes, 10 seconds
beyond that, so the frame count stays near 100. It writes `report.md` in the same format `/watch`
produces (frame paths with `t=MM:SS` markers plus a timestamped transcript).
Then Read the frames. Read them in parallel in batches; each frame path in
the report carries its timestamp.

### Path C: YouTube URL with a Gemini key

```bash
python3 .claude/skills/youtube-to-agent/scripts/gemini_watch.py <youtube-url> --out <workdir>/gemini-beats.md
```

This asks Gemini to produce the beat sheet described in Step 2 directly from
the YouTube URL, including verbatim on-screen text. Pass `--question "..."` to
focus it on the target capability. Run it alongside Path A when both are
available. Gemini is a witness, not an oracle: treat its output as a second
transcript to be reconciled with the frames, and mark anything only Gemini
reports as "Gemini only".

### Path D: YouTube URL, no plugin, with or without a Gemini key

```bash
python3 .claude/skills/youtube-to-agent/scripts/fetch_captions.py <url> --out-dir <workdir>
```

This pulls the video's captions with yt-dlp (no key needed) and writes a
timestamped transcript plus a 30-second-paragraph version for reading. Pair it
with Path C when a Gemini key exists: captions give exact wording, Gemini gives
the visuals. In cloud environments YouTube often refuses the video stream with
a 403 "confirm you're not a bot" error even though captions download fine, so
do not treat a failed video download as a dead end. When you end up with no
frames at all, say so in the analysis and mark every visual claim "Gemini
only".

When yt-dlp is blocked outright (YouTube's bot check now refuses even
caption and metadata requests from some cloud machines), run Path C twice:
once in the default beats mode and once with `--mode transcript`, which asks
Gemini for near-verbatim timestamped speech plus quoted on-screen text. The
transcript stands in for captions as "what was said"; the beats stand in for
frames as "what was seen". Titles and authors still come free from
`https://www.youtube.com/oembed?url=<video-url>&format=json`.

Path C in numbers, from a 16-minute test video: about 70 seconds wall clock,
about 90k video tokens in, about 2.3k tokens out, with the caption text and
Gemini's read agreeing on every substantive point and Gemini adding the
on-screen labels and URLs the captions could not.

Run the ingestion paths in parallel where possible. Write everything into one
working directory (default `.youtube-to-agent/<slug>/`, which is gitignored by
the scaffolder) so the analysis step has a single place to look.

## Step 2: Build the beat sheet

Read `references/analysis-prompt.md` and apply it to the material from Step 1.
The short version: merge what was seen and what was said into a single
timeline of beats before drawing any conclusion, then read across the beats
for structure, then report only what the evidence shows, marking inference as
inference and sampling gaps as gaps, and finish with the three highest-signal
observations with timestamps.

Save the result to `<workdir>/analysis.md`. This file becomes the provenance
record for the generated skill, so every claim in it should carry a timestamp
someone could verify by scrubbing to it.

Why bother with a beat sheet instead of summarizing directly? Tutorials
interleave narration, demonstration, and asides. A summary written straight
from the transcript reliably drops the steps that were only shown (the click
that was never narrated, the flag visible in the terminal) and keeps the
asides that were only spoken. The beat sheet forces the two channels to be
aligned first, and the "what changed since the last beat" column is where
the actual procedure lives.

## Step 3: Extract the skill spec

From the beat sheet, write a skill spec at `<workdir>/spec.json`. This is the
bridge between "what the video showed" and "what the agent should do". Read
`references/agent-blueprint.md` for the full reasoning; the fields are:

```json
{
  "name": "kebab-case-skill-name",
  "description": "What it does AND when to trigger, written pushy (see blueprint)",
  "capability": "One sentence: what the agent can now do",
  "source": {"url_or_path": "...", "title": "...", "author": "...", "duration": "MM:SS"},
  "prerequisites": ["tools, accounts, keys the workflow needs"],
  "procedure": [
    {"step": "imperative instruction", "why": "the reason the video gave or you inferred", "evidence": ["t=MM:SS"], "commands": ["exact commands or UI paths"]}
  ],
  "decision_rules": [{"when": "situation", "do": "action", "evidence": ["t=MM:SS"]}],
  "gotchas": [{"issue": "...", "fix": "...", "evidence": ["t=MM:SS"]}],
  "verbatim_assets": [{"kind": "prompt|command|config|template", "text": "...", "evidence": ["t=MM:SS"]}],
  "gaps": ["things the video did not cover that the agent will need"],
  "test_prompts": ["2 or 3 realistic user requests the finished skill should handle"]
}
```

Rules that keep the spec honest:

- Every procedure step, rule, and gotcha cites at least one timestamp from
  the beat sheet. If you cannot cite it, it goes in `gaps`, not `procedure`.
- `verbatim_assets` holds text that must survive character for character:
  prompts shown on screen, commands, config snippets. Copy from frames, not
  from the transcript, since speech recognition mangles code.
- `gaps` is not a failure list. Videos are short and skip setup, error
  handling, and edge cases. Naming the gaps lets you fill them from your own
  knowledge in the generated skill while flagging them as "not from the
  video" so the user knows what to verify.
- Generalize beyond the video's specific example. If the video builds a
  social media manager for one brand, the procedure should describe the
  method for any brand, with the video's case as an example.

## Step 4: Scaffold the agent

```bash
python3 .claude/skills/youtube-to-agent/scripts/scaffold_agent.py <workdir>/spec.json --dest .claude/skills [--analysis <workdir>/analysis.md] [--force]
```

This creates:

```
.claude/skills/<name>/
├── SKILL.md                  # frontmatter + procedure, rendered from the spec
├── references/
│   ├── source-notes.md       # beat sheet + observations, with timestamps
│   └── verbatim-assets.md    # prompts, commands, configs copied exactly
└── evals/
    └── evals.json            # the test prompts, ready for skill-creator
```

Use `--dest ~/.claude/skills` when the user wants the skill available in
every project rather than just this repo. The scaffolder refuses to
overwrite an existing skill unless you pass `--force`, so an accidental
name collision cannot destroy someone's hand-written skill.

After scaffolding, open the generated SKILL.md and edit it by hand. The
scaffolder produces a correct skeleton, not a finished skill. In particular:

- Rewrite the procedure so it explains why each step matters, not just what
  to do. Future Claude will face situations the video never showed, and
  understanding the intent is what lets it adapt.
- Fill the gaps you listed in the spec from your own knowledge, marked with
  "(not shown in the video)" so the user can verify them.
- Keep SKILL.md under about 300 lines. Push long material into
  `references/` and point to it.

## Step 5: Test it

Spawn one subagent per test prompt from `evals/evals.json` with an
instruction like:

```
Read the skill at <path>/SKILL.md and follow it to complete this task: <prompt>.
Save any outputs under <workdir>/test-<n>/. Report what the skill left unclear.
```

Read the "left unclear" reports and fix the skill. One round is usually
enough for a first version; if the user wants a rigorous loop with baselines
and grading, hand off to the `skill-creator` skill, which reads the same
`evals/evals.json`.

## Step 6: Report

End with a short report the user can act on without scrolling back:

- Where the new skill lives and how to invoke it.
- The three highest-signal observations from the video, with timestamps.
- What came from the video versus what you filled in, and what needs
  verifying.
- Which of the three systems were used and which are still missing, with
  the exact commands to add them.

## Several videos into one skill

When the user gives two or more videos on one theme (three tutorials on
Instagram growth, say), build one skill, not three, and make the merge
visible:

1. Run Step 1 and Step 2 per video, in parallel, each in its own working
   directory, so every beat sheet stands on its own.
2. Tag the sources V1, V2, V3 in the order the user gave them and prefix
   every timestamp with its tag ("V2 t=04:10") from the spec onward.
3. Before writing the spec, write `<workdir>/merge.md` with three lists:
   points all videos agree on (these become the procedure's spine), points
   only one video makes (keep them, attributed), and points where the videos
   disagree (state both sides and pick one with a reason, or offer the
   choice to the user in the skill's decision rules). Disagreements are the
   most valuable content in a merged skill; do not average them away.
4. Use `"sources": [...]` in the spec instead of `"source"`, and pass all
   analyses to the scaffolder: `--analysis v1/analysis.md v2/analysis.md
   v3/analysis.md`.
5. Name the skill after the capability, not the videos, and keep it to one
   capability. If the merge list shows two unrelated capabilities, say so
   and build two skills.

## Working notes

- The uploaded-file case ("save and share this video to Claude Code") is a
  local file path, usually a portrait phone recording. Path B handles it.
  The on-screen text is usually a phone screenshot inside the video, so use
  a wide `--width` and read the frames at full size.
- Talking-head segments with no screen content produce near-identical
  frames. Skip reading duplicates; the transcript covers them.
- Speech recognition mishears product names ("cloud code" for Claude Code,
  "GitHub Studio" for Google AI Studio). Resolve names from frames and, when
  a repo or product is named, verify it exists with a quick web lookup
  before writing it into the skill.
- Never write API keys into the generated skill, the spec, or the repo.
  Reference environment variable names only.
