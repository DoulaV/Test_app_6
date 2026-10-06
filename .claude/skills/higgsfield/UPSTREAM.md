# Upstream and provenance

| | |
|---|---|
| Source | [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) |
| Version | 3.40.0 (specs snapshot 2026-09-26) |
| Commit | 7075497 |
| Author | O-Side Media |
| Licence | MIT, full text in `LICENSE` |

Every file here is byte-identical to upstream. Nothing was edited. This is the
runtime subset of the repo: the files the dispatcher `SKILL.md` and its 33
sub-skills reference while working, in the same folder layout, because they
point at each other by relative path.

## Installed

- `SKILL.md`, the dispatcher, and `skills/`, all 33 sub-skills with their
  satellite files
- `templates/`, the genre, Seedance technique, character-design and text-overlay
  templates
- The root references the skills cite: `model-guide.md`, `image-models.md`,
  `vocab.md`, `prompt-examples.md`, `photodump-presets.md`, `DISCIPLINE.md`,
  `production-benchmarks.md`, and `docs/Seedance 2 Skill.md`
- `specs/`, the generated model specs, keeping only the newest dated
  `models_explore` snapshot of each family
- `db/`, the seeded filter and quality memory and the ledger schema
- `workspace/` with its three ignore files, so documents the skill files there
  stay out of git
- The six scripts the skills tell Claude to run, all standard library only:
  `higgsfield_memory.py` (generation ledger), `seedance_lint.py` and
  `preflight.py` (prompt checks before spending credits), and the three modules
  they import (`sub_skill_descriptions.py`, `refresh_specs.py`, `sync_specs.py`)

## Deliberately not installed

| Upstream | Why |
|---|---|
| `.claude/settings.json` | Pre-approves `git push`, any `python3` command, `gh`, and edits to `.claude/`, without prompting. Right for the author's repo, wrong to import into this one. |
| `CLAUDE.md`, `.claude/commands/`, `.claude/rules/` | The author's maintenance instructions (release, validate, refresh specs). Claude Code loads a nested `CLAUDE.md` when it reads files in that folder, so shipping it would inject their release workflow into these sessions. |
| `.github/`, `tests/`, `evals/`, the other scripts | CI, test suite and maintainer tooling. |
| `INDEX.md`, `CHANGELOG.md`, `docs/archive/`, `docs/user-guide/`, `assets/fonts/` | Not referenced by any skill at runtime. The fonts are only for the PDF user-guide generator. |
| `db/routing-log.json` | The author's own routing telemetry. The ledger script recreates it when needed. |
| Older `models_explore` snapshots | Superseded by the 2026-09-26 set. |

## What it does, and how it fits here

It writes prompts for Higgsfield: picks the model, names the camera move and
motion preset, structures every video prompt as Model, Camera, Subject, Look,
Action, and appends the right negative constraints. It does not generate
anything itself. Execution goes through Higgsfield's MCP connector, CLI or the
website.

It overlaps with `hook-writer` and `story-loop-writer` only in the word
"script". Those decide what the film says. This decides what the generator is
told to render. A realistic chain is story-loop-writer for the scene, then this
for the shot prompts, then the Higgsfield connector to render them.

## Runtime notes

- The skill asks Claude to read its files in full before answering (its HARD
  RULE 2) and to open the first line of every answer with which sub-skills it
  routed to. That is upstream behaviour, not a bug.
- Generation logs go to `db/ledger/<project>.json` and per-project memory to
  `db/projects/`. The repo `.gitignore` keeps the per-project files and the
  routing telemetry out of git.
- The specs are a snapshot. The skill itself says to verify live when the
  snapshot is older than 30 days.

## The claude.ai package differs in one way

claude.ai rejects a zip with more than one `SKILL.md`, and this package has one
per sub-skill folder (36 in total). `dist/claude-ai/pack.py` renames the 35
nested ones to `SUBSKILL.md` in the zip only, rewrites every path that points at
them (481 references, all checked to resolve), and adds a one-paragraph note at
the top of the zipped dispatcher explaining the rename. The copy in this folder
is untouched, because Claude Code reads nested `SKILL.md` files without
complaint.

## Updating

Run the copy again against a fresh clone of upstream, using the same include
list as above, then bump the commit and version here.
