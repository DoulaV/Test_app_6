# Upstream and provenance

| | |
|---|---|
| Source | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo), `docs/skill/` |
| Skill version | 1.3.2 |
| Commit | 92e0f9a (2026-11-16) |
| Author | harry0703 |
| Licence | MIT, full text in `LICENSE` |

## What is unmodified

`mpt_agent.py` is byte-identical to upstream
(sha256 `d445dc9db35e19f211e9448dd016bd023927a2232a4b44a14f1f8f4115f5d66a`).
The body of `SKILL.md`, from `# MoneyPrinterTurbo Video Generation` down to the
`Local notes` heading, is byte-identical to upstream.

The helper was read in full before vendoring. It downloads the project archive
from GitHub on first run, runs `uv sync --frozen` and `cli.py`, writes supplied
keys into the local `config.toml`, and checks Pexels keys against
`api.pexels.com`. It never prints key values and sends no telemetry. Note that it
installs whatever is on the project's `main` branch at the time, not a pinned
release.

## What we changed

1. **Frontmatter.** The `description` was rewritten to say when the skill fits
   Ahmed's brand (drafts, B-roll tests, faceless formats, animatics) and when it
   does not (his finished films). `compatibility` notes that Linux was tested.
2. **A `Local notes` section was appended.** It overrides upstream where they
   conflict: keys are never requested in chat; Egyptian Arabic voice and 9:16 by
   default instead of Chinese; using his own script and search terms so no AI
   writer key is needed; the `claude_code` provider; Arabic subtitle fonts; the
   git clone fallback when the archive download returns 403.

## Install test (2026-11-19, Linux cloud container)

- Archive download: HTTP 403 from the session proxy. Cloning and rerunning
  worked; the helper reused the checkout.
- Helper: created `config.toml`, exited 10 asking for `moonshot_api_key` and
  `pexels_api_keys`, as designed.
- `uv sync --frozen`: succeeded, about 1.3 GB.
- CLI with an Egyptian Arabic script: stopped at the voice stage because Edge TTS
  uses a WebSocket, which the cloud proxy does not carry. Not a fault in the app;
  run it on a personal computer.

Not packaged for claude.ai: it needs a long-running local install and network
access that the claude.ai sandbox does not provide.
