# From beat sheet to agent (System 3, part 2)

The beat sheet tells you what the video taught. This file is about turning
that into a skill Claude will actually use well a thousand times, on requests
the video never anticipated.

## What a skill is, mechanically

A skill is a folder with a `SKILL.md` (YAML frontmatter plus markdown
instructions) and optional `scripts/`, `references/`, and `assets/`. Claude
sees only the name and description until the skill triggers, then loads the
SKILL.md body, and reads bundled files only when the body points at them.
So:

- The **description** decides whether the skill fires at all.
- The **SKILL.md body** must carry the whole procedure in under about 300
  lines.
- Long material (the beat sheet, verbatim prompts, edge-case tables) goes in
  `references/` with a sentence in the body saying when to read it.

## Writing the description

Claude under-triggers skills. Write the description to cover what the skill
does and every phrasing a user might use when they need it, including cases
where they never name the skill. Pattern:

> `<What it does in one sentence>. Use this whenever the user <situation 1>,
> <situation 2>, mentions <keywords>, or wants <outcome>, even if they do not
> say "<skill name>".`

Draw the situations from the video's own framing of who this is for and from
the test prompts in the spec.

## Turning procedure into instructions

The video shows one path through the task. The skill has to describe the
method. For each procedure step in the spec:

1. State the step in the imperative.
2. Say why. Use the reason the presenter gave if they gave one (cite the
   timestamp in `references/source-notes.md`, not in the body). If they did
   not, supply the reason yourself and mark it "(not shown in the video)".
3. Give the exact command, prompt, or UI path from `verbatim_assets`.
4. Name the decision points: what to check before moving on, what a failure
   looks like, what to do about it. Videos skip these; you fill them.

Prefer explanations over capitalized MUSTs. A model that understands why a
step exists can handle the case the video did not cover; one that only has a
rule cannot.

## Generalizing beyond the example

Ask, for each concrete detail in the video: is this the method, or is this the
presenter's instance of the method? A brand name, a specific spreadsheet, a
particular API are usually instances. Write the skill around the method and
keep the video's instance as a worked example in `references/source-notes.md`.

## Filling gaps honestly

The spec's `gaps` list is the set of things the agent will need that the video
skipped: installation, authentication, error handling, what to do with a bad
input. Fill them from your own knowledge, but mark each one "(not shown in
the video)" in the body. The user chose this video as their source of truth;
they need to know where you departed from it.

## Verbatim assets

Prompts, commands, and config snippets from the video go into
`references/verbatim-assets.md` exactly as shown on screen, each with its
timestamp. The body of SKILL.md quotes the short ones inline and points to the
file for the long ones. Copy from frames, never from the transcript.

## Test prompts

Write two or three prompts a real user would type when they need this skill.
Concrete, with a bit of backstory, some casual. They go into
`evals/evals.json` so the `skill-creator` skill can run a proper
with-skill versus without-skill comparison later. A good test prompt exercises
a decision point, not just the happy path.

## Where to put the generated skill

- `.claude/skills/<name>/` in the current repo when the skill is about this
  project or the user did not say. It ships with the repo and is reviewable in
  a PR.
- `~/.claude/skills/<name>/` when the user wants it in every project.

Names are kebab-case, specific, and describe the capability, not the video
("social-media-scheduler", not "brads-video-skill").

## Checklist before you report

- Description covers the phrasings in the test prompts.
- Every procedure step has a why.
- Every claim in `source-notes.md` has a timestamp.
- Every gap-fill in the body is marked "(not shown in the video)".
- No API keys, tokens, or personal data anywhere in the skill.
- SKILL.md is under about 300 lines and points to references for the rest.
