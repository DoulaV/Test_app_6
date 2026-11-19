---
name: moneyprinterturbo-video
description: |
  Turn a topic or a finished script into a rendered MP4 with MoneyPrinterTurbo:
  script, voiceover, stock or generated footage, subtitles, music and edit,
  fully automatic. Use this whenever the user wants a finished video file made
  for them from a topic, idea or script, mentions MoneyPrinterTurbo or mpt, or
  wants a MoneyPrinterTurbo install, key setup or failed render fixed. For
  Ahmed's own @akadoola films, use it only for drafts, B-roll tests, faceless
  side formats or a quick animatic, never as the finished film; the brand rests
  on Ahmed being real and on camera.
compatibility: Needs a terminal, network, filesystem and long-running commands. Upstream supports macOS and Windows; Linux was also tested here. Uses uv.
metadata:
  author: "harry0703@hotmail.com"
  version: "1.3.2"
  upstream: "https://github.com/harry0703/MoneyPrinterTurbo"
---

# MoneyPrinterTurbo Video Generation

The user only needs to provide a video topic or script. Complete installation, configuration reuse, generation, waiting, and final MP4 delivery automatically. Do not stop after giving instructions or commands.

## Required Behavior

1. Ask the user only for required API credentials that are missing, rejected, or unusable. Combine all required credentials into one request.
2. Do not ask for confirmation before installing, generating, waiting, using defaults, or returning the result.
3. Do not create or repeatedly update a detailed plan for a standard generation request. Send one short progress update and execute.
4. Run the helper as one foreground command with a timeout of at least 20 minutes.
5. Never poll with `sleep`, `echo`, `ps`, repeated `ls`, or repeated `tail`. If the terminal returns a resumable session ID, continue waiting on that same session.
6. Do not read the full log after success. Read only the short reported error or the relevant log tail after failure.
7. Never print API keys, tokens, the full `config.toml`, or credential-bearing configuration fragments.

## Defaults

Unless the user requests otherwise, generate one Chinese `9:16` portrait video with Pexels footage, the default Chinese Edge TTS voice, subtitles, and background music. Install MoneyPrinterTurbo under the user's home directory.

## Execution

### 1. Locate the helper

Resolve `SKILL_DIR` from this `SKILL.md` file. The helper is the adjacent `mpt_agent.py`. Set the terminal tool's working directory to `SKILL_DIR` and invoke the helper by its relative filename. Do not put the absolute helper path in the command, and do not run an extra `ls` or `dir` check.

This is required on Windows because some agent terminal validators remove backslashes from absolute paths embedded in commands. Using `mpt_agent.py` with `workdir=SKILL_DIR` avoids that failure and works on both macOS and Windows.

If the client loaded only the remote `SKILL.md`, download the helper from the official repository to a temporary directory, then use that temporary directory as the command working directory:

```text
https://raw.githubusercontent.com/harry0703/MoneyPrinterTurbo/main/docs/skill/mpt_agent.py
```

### 2. Run the helper

Do not run a separate `uv --version` preflight. Run the helper directly. If the shell explicitly reports that uv is missing, install uv and retry the same helper command once.

macOS uv installation:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell uv installation:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Use this foreground command with `workdir=SKILL_DIR` and a timeout of at least 20 minutes:

```bash
uv run --no-project --python 3.11 python mpt_agent.py --subject "<video topic>"
```

On Windows, do not try absolute backslash paths, absolute forward-slash paths, or copies in the workspace before this relative command. If a terminal tool reports `referenced_script_path_missing`, verify that its working directory is exactly `SKILL_DIR` and retry the relative command once. Do not cycle through path variants.

Do not use Docker, Conda, system pip, or a manually managed virtual environment.

## Exit Handling

### Exit code 0: deliver the result

Successful output has this form:

```text
MPT_RESULT
VIDEO_FILE=<absolute path>/final-1.mp4
TASK_DIR=<absolute path>/storage/tasks/<task_id>
LOG_FILE=<absolute path>/run-<task_id>.log
RESULT_FILE=<absolute path>/latest-result.json
```

`mpt_agent.py` emits `VIDEO_FILE` only after confirming that the file exists and is non-empty. Do not run another `ls`, `stat`, or file validation command.

If the terminal reports `exitCode=0` but truncates the output or returns a history-file reference without `MPT_RESULT`, do not infer failure and do not inspect old logs. Read this file once:

```text
~/MoneyPrinterTurbo/.agent-logs/moneyprinterturbo-video/latest-result.json
```

Treat `status=completed` as success. Return only the absolute video path and a concise description, for example:

```text
The video is ready.
Topic: ...
Video file: /absolute/path/to/final-1.mp4
Summary: Chinese portrait video with voice-over, subtitles, and background music.
```

### Exit code 10: request credentials once

`MPT_NEEDS_INPUT` includes only the required fields, recommended LLM providers and signup links, custom OpenAI-compatible requirements, and material-provider signup links. Ask only for the listed values and do not request credentials already found in `config.toml`.

After the user responds, rerun the same foreground command with only the required environment variables:

```text
MPT_LLM_PROVIDER
MPT_LLM_API_KEY
MPT_LLM_BASE_URL
MPT_LLM_MODEL_NAME
MPT_PEXELS_API_KEY
MPT_VOLCENGINE_ARK_API_KEY
MPT_OFOX_API_KEY
MPT_METASO_MINIMAX_API_KEY
MPT_MUAPI_API_KEY
MPT_USEAPI_TOKEN
MPT_INFISTAR_VIDEO_API_KEY
MPT_JALAPENO_VIDEO_API_KEY
```

When `SEEDANCE_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated Seedance clip creates a paid Ark task. Only after the user explicitly
confirms, rerun with `--confirm-seedance-charge`; never add this flag silently.

When `WAVESPEED_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated WaveSpeed clip is billed per request by WaveSpeed. Only after the user
explicitly confirms, rerun with `--confirm-wavespeed-charge`; never add this
flag silently.

When `OFOX_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated OFox clip creates a paid task. Only after the user explicitly
confirms, rerun with `--confirm-ofox-charge`; never add this flag silently.

When `METASO_MINIMAX_CHARGE_CONFIRMATION_REQUIRED` is present, explain that
every generated MiniMax H3 clip creates a paid Metaso task. Only after the user
explicitly confirms, rerun with `--confirm-metaso-minimax-charge`; never add
this flag silently.

When `MUAPI_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated MuAPI clip creates a paid task. Only after the user explicitly
confirms, rerun with `--confirm-muapi-charge`; never add this flag silently.

When `USEAPI_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated useapi.net clip spends credits on the user's own Google AI plan,
Kling AI account or Dreamina account connected to useapi.net. Only after the
user explicitly confirms, rerun with `--confirm-useapi-charge`; never add this
flag silently.
The `useapi_image` source uses the same `MPT_USEAPI_TOKEN`. Nano Banana images
need no confirmation flag; a Kling image model (`useapi_image_model` starting
with `kling-`) spends Kling credits and needs `--confirm-useapi-charge`, asked
for the same way.

When `INFISTAR_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated Infistar clip creates a paid task. Only after the user explicitly
confirms, rerun with `--confirm-infistar-charge`; never add this flag silently.
Use the dedicated video key, separate from the Infistar LLM key.

When `JALAPENO_CHARGE_CONFIRMATION_REQUIRED` is present, explain that every
generated Jalapeno Cloud clip creates a paid task. After the user confirms,
rerun with `--confirm-jalapeno-charge`. An empty video key reuses the
configured Jalapeno Cloud LLM key; a dedicated video key takes priority.

### Exit code 1: repair or report

Use `MPT_ERROR` and `LOG_FILE` to repair a recoverable problem and retry once. Ask the user only if the repair requires a new API key. If the retry fails, report the failed stage, a short error, and the log path.

A terminal-tool path validation error is not a video-generation failure because the helper did not start. Correct the working directory and retry the relative command once. Never ask the user to copy `mpt_agent.py`, run commands manually, or confirm whether the agent should continue.

## Configuration and Background Fallback

The helper may read the complete local `config.toml` to reuse existing settings, but it must never print its contents. It reuses a working LLM provider automatically and validates configured Pexels keys through the authenticated My Collections endpoint before generation.

Use background mode only if the agent platform cannot wait for a foreground process. Wait for the platform's process-completion notification without polling, then read `latest-result.json` once.

## Scope

- Support macOS and Windows only.
- Use uv and the MoneyPrinterTurbo CLI only.
- Do not start Docker, WebUI, or API services.
- Do not run multiple video jobs concurrently.
- Pass additional video requirements after `--`. Run `cli.py --help` once only when an unfamiliar option must be verified.

## Local notes (this library; these override the upstream text above where they conflict)

Not from upstream. See `UPSTREAM.md` for what was changed and why.

**Keys never go through chat.** Upstream says to ask the user for missing keys
and pass them as environment variables. Here, never ask the user to paste a key
into the conversation. On exit code 10, list the missing fields with their
signup links and tell the user to add them themselves, either in the WebUI
(Basic Settings) or directly in `~/MoneyPrinterTurbo/config.toml`, then rerun.
In a Claude Code cloud session, use the environment's secret settings instead.

**Default to Ahmed's language, not Chinese.** Unless the user asks otherwise,
pass these after `--`:

```
--video-language ar-EG --voice-name ar-EG-ShakirNeural-Male --video-aspect 9:16
```

`ar-EG-SalmaNeural-Female` is the female Egyptian voice. For Gulf or formal
Arabic, `ar-SA-HamedNeural-Male`. Edge TTS is free and needs no key.

**When Ahmed supplies his own script, skip the AI writer entirely.** Pass the
script and the footage search terms yourself, and no LLM key is needed at all,
only a Pexels key:

```
uv run --no-project --python 3.11 python mpt_agent.py --subject "<short title>" -- \
  --video-script "<his script>" --video-terms "rain window,night street,man alone" \
  --video-language ar-EG --voice-name ar-EG-ShakirNeural-Male
```

Write the search terms in English; stock libraries index English. Run the
script through `humanizer` first if it was AI-drafted.

**Use his own footage when the point is his look.** `--video-source local
--video-materials <folder>` cuts his clips instead of stock. Stock footage will
never match his grade, so stock output is for drafts and animatics.

**No API key for the writer on his own machine.** If Claude Code is logged in on
the same computer, set `llm_provider = "claude_code"` in `config.toml`; it uses the
Claude subscription through the local `claude` CLI.

**Arabic subtitles.** The app shapes Arabic text (the `khatt` library) and falls
back to an Arabic-capable font when the chosen one lacks the glyphs. For his
brand typeface, drop the `.ttf` into `~/MoneyPrinterTurbo/resource/fonts/` and
pass `--font-name <file>.ttf`.

**If the first-time download returns HTTP 403** (some proxies block GitHub's
zip archives), clone instead and rerun; the helper reuses an existing checkout:

```
git clone --depth 1 https://github.com/harry0703/MoneyPrinterTurbo.git ~/MoneyPrinterTurbo
```

**Paid generators.** Every source other than `pexels`, `pixabay`, `coverr` and
`local` costs money per clip. Never add a `--confirm-*-charge` flag without the
user's explicit yes for that run, as upstream already requires.

**Where this sits.** Plan the film with `story-loop-writer` and `hook-writer`,
write the words with `akadoola-voice` (claude.ai project) or `humanizer`, check the idea against
`brand-architect`. This skill only renders.

