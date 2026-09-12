# Upstream

This skill is vendored from https://github.com/blader/humanizer (MIT,
Copyright (c) 2025 Siqi Chen), version 3.0.0, at commit 9862685f575c65a8247f90369951df1b3416e3d6.

`SKILL.md` and `LICENSE` are byte-identical to upstream and should stay that
way. Do not edit them. To update, re-copy both files from the repo and bump
the commit above. Anything we want to add about how it fits the rest of this
repo goes in this file instead.

## Where it sits among our skills

It runs **after** `copy-sharpener`, as the last pass over finished English
prose. copy-sharpener decides what the words should say and how they should
land. humanizer removes the residue that says a model wrote them.

Two overlaps worth knowing:

- Both care about concrete over abstract. copy-sharpener gets there through
  the So What ladder and the deaf-and-mute test. humanizer gets there by
  deleting the staging (§1 to §5). They agree, so run copy-sharpener first
  and let humanizer clean up after.
- humanizer §8 bans em dashes from the final rewrite unless a writing sample
  uses them. That matches the standing preference in this repo, so it doubles
  as an enforcement pass.

## What it does not do

It is written for English. The pattern list (stock words, hyphenated pairs,
curly quotes, sales language) does not transfer to Egyptian Arabic, and §1
explicitly says the not-X-but-Y formula exists in every language but gives no
guidance beyond that. Use it on English captions, bios, pitches and English
notes. Do not run it on Arabic voiceover lines and expect the list to apply.

The skill also takes a writing sample and matches it, which is the highest
value way to use it. Give it three or four paragraphs you actually wrote.
