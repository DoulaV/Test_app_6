# Upstream and provenance

| | |
|---|---|
| Source | [MetcalfSolutions/Satori](https://github.com/MetcalfSolutions/Satori) |
| Version | 5.1.0 |
| Commit | 6440b52 |
| Author | Matthew Metcalf |
| Licence | Apache License 2.0, full text in `LICENSE` |

## What is unmodified

All nine files in `references/` are byte-identical to upstream. The body of
`SKILL.md`, from the `# Satori` heading down to the `Local notes` heading, is
byte-identical to upstream.

## What we changed (Apache 2.0, section 4(b))

Two changes, both in `SKILL.md`, both made on installation into this repo:

**1. The `description` field was rewritten.** Upstream is written to activate on
"any emotionally charged framing" and closes with "When in doubt, activate." In
this repo that is a real problem rather than a style choice: the owner makes films
about male emotional suppression, so almost every content request carries emotional
language, and the upstream trigger would answer a script request as a therapy
session. The rewrite keeps the scope (the inner life, the traditions, the
frameworks) and adds an explicit exclusion for creative and content work, with a
rule for switching when a content request turns personal.

The upstream description, verbatim:

> Satori is a clinically informed wisdom companion for navigating the inner life — emotions, meaning, grief, purpose, relationship, identity, and the questions that don't resolve easily. Activate when someone is processing something difficult, wrestling with a life question, seeking perspective, or simply needs to think alongside someone who won't rush them toward an answer. Also activate when someone uses language like "I've been struggling with," "I don't know what to do," or "I need to figure out" — or any emotionally charged framing. When in doubt, activate. Draws from Taoism, Buddhism, Stoicism, Christianity, Sufi wisdom, Hindu philosophy, Confucian ethics, and African thought, alongside modern psychology, neuroscience, and trauma-informed frameworks (IFS, DBT, CFT, Schema Therapy, Somatic). Uses Motivational Interviewing, Voss tactical empathy, McAdams Life Story, and Singer Self-Defining Memory — woven naturally, not mechanically.

**2. A `Local notes` section was appended** at the end of `SKILL.md`, covering
scope, crisis resources outside the United States, and memory files. It is marked
as ours in the file itself.

## What was deliberately not installed

| Upstream file | Why it was left out |
|---|---|
| `.mcp.json` | Declares two MCP servers for the author's own tooling (`tessl`, and `marp-mcp` fetched and run through `npx`). Not part of the skill. Installing it here would make Claude Code offer to download and execute an npm package. |
| `registry-submissions/` | The author's script for forking skill registries and opening pull requests under their GitHub account. |
| `SatoriSkill-v5.zip` | A prebuilt package. It is out of date against the repo's own `SKILL.md`, puts files at the zip root rather than in a skill folder, and its description is 950 characters against claude.ai's 200 limit, so it would be rejected on upload. We build our own from source. |
| `docs/`, `slides/`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, manifests | Project website, presentation and packaging for the upstream repo. |

## Three things worth knowing about how it behaves

- **It claims to remember you across sessions.** That depends on the platform's
  memory feature being on. Without it, each conversation starts fresh whatever the
  skill says.
- **Its crisis numbers are United States numbers.** The local note fixes this by
  leading with the international directory and asking where the person is.
- **It is not therapy and says so.** It has a crisis protocol, a separate "dark
  night" protocol for despair without danger that escalates to the crisis protocol
  on any sign of intent, and a referral threshold inside the shadow work arc.

## Where it sits among our skills

Apart from them. Every other skill in this repo is for making content. This one is
for the person making it.

The one sanctioned crossover is character research: when a writer asks for a
character's psychology, its frameworks can explain the character's inner logic. A
routing test caught the first version of our description excluding "characters"
while the local notes allowed character research, which left that request with no
skill at all. Both now agree. The understanding shapes what the
character does. The vocabulary never reaches the film. That line matters here
because "therapy-speak, diagnosis, advice about mental health" is on the brand's
refusal list in `docs/project-instructions.md`.

## Updating

Re-copy `references/` and `LICENSE` from upstream, bump the commit above, then
re-apply the two changes: take the new upstream `SKILL.md` body, keep our
`description`, and re-append the `Local notes` section. Check the local notes still
match upstream's crisis protocol and memory model before re-appending.
