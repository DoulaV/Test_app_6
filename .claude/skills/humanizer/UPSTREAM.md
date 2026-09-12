# Upstream and provenance

`SKILL.md` is our merge of two skills. Both are MIT and both are vendored
unmodified in `references/`, with their licence files kept beside them.

| Source | Version | Commit | Vendored as | Licence |
|---|---|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | 3.0.0 | 9862685 | `references/english-patterns.md` | `LICENSE-blader-humanizer` (MIT, Copyright (c) 2025 Siqi Chen) |
| [OthmanAdi/humanizer-semitic](https://github.com/OthmanAdi/humanizer-semitic), skill `humanizer-ar-egt` | 1.0.0 | 2c9d4fb | `references/egyptian-arabic-patterns.md` | `LICENSE-othmanadi-humanizer-semitic` (MIT, Copyright (c) 2026 OthmanAdi) |

The two reference files are byte-identical to upstream. Do not edit them. To
update, re-copy the file from the source repo and bump the commit above, then
re-read `references/merge.md` and check whether any conflict resolution moved.

blader/humanizer draws its patterns from Wikipedia's
["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup. humanizer-semitic credits
blader/humanizer as its structural model and adds research-grounded patterns
for Arabic and Hebrew.

## What is ours

`SKILL.md` and `references/merge.md`. Specifically:

- The language router, and the rule that the two lists are never run together.
- The cut / swap / add distinction, and the closed list of what may be added.
- The resolution that the no-invention rule beats the Egyptian source's
  instruction to reach for specific place names and foods when vocabulary is
  flat. See conflict 2 in `merge.md`. This one matters: without it the skill
  will fabricate detail in a personal script.
- The hedging resolution, where the two sources appear to contradict each
  other and do not.
- Promoting the writing-sample override from the English source to both
  languages.
- The **Dramatic** register rung, for written dialogue and voiceover, which
  neither source has and which is the main thing this repo is used to write.
- The mixed-script rule in §D.

## Not vendored

humanizer-semitic also ships MSA (`humanizer-ar-msa`), Levantine
(`humanizer-ar-shami`) and Modern Hebrew (`humanizer-he`) skills. They are out
of scope here. If this repo ever needs MSA, add it the same way: vendor the
file into `references/`, keep it unmodified, and extend the router in Step 0
rather than blending its patterns into the Egyptian ones.

## Where it sits among our skills

Last. It runs after `copy-sharpener`, which decides what the words say and how
they land. This one removes the residue that says a model wrote them.

Unlike the English-only version this repo carried before, it now covers the
Egyptian Arabic scripts too, which was the gap. The thing to watch is the
register: on a cinematic script, use the Dramatic rung, where the grammar
patterns apply in full and the performative additions do not. Running the
Ultra-Casual rung over film dialogue will fill it with هههههه and reader
questions that do not belong in a character's mouth.
