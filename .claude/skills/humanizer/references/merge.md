# Merge notes: two humanizers into one

Sources, both MIT and both vendored unmodified in this folder:

- **V1** `blader/humanizer` v3.0.0, commit 9862685. English. 25 patterns drawn
  from Wikipedia's "Signs of AI writing". Full text: `english-patterns.md`.
- **V2** `OthmanAdi/humanizer-semitic` v1.0.0, commit 2c9d4fb, the
  `humanizer-ar-egt` skill. Egyptian Arabic. 25 patterns. V2 credits V1 as its
  structural model. Full text: `egyptian-arabic-patterns.md`.

The merged `SKILL.md` is our work. These notes record what each source
contributed, where they agree, where they conflict, and how each conflict was
settled, so a later reader can check the reasoning instead of trusting it.

## What each source is actually about

They look like the same skill in two languages. They are not.

**V1 removes.** Its thesis is that a model writes the most likely next thing,
so its prose is padded with staging that signals importance without adding
information. Almost every fix is a deletion: cut the contrast, cut the closer,
cut the qualifier, cut the bold.

**V2 restores.** Its thesis is that a model writing Egyptian Arabic is
actually writing Modern Standard Arabic with Egyptian words sprinkled on top,
because MSA dominates the training data. Most of its fixes are grammatical
substitutions, and several are additions: discourse particles, hedges, terms
of address, reader-directed questions.

That difference is the whole design problem. Run V1's instincts on Arabic and
you strip the particles that make it sound human. Run V2's instincts on
English and you pad it. The merged skill routes by language first for exactly
this reason.

## Where they agree

These eight are the same finding in two languages, so the merged skill states
each once and gives both sets of markers.

| Tell | V1 | V2 |
|---|---|---|
| Chatbot sycophancy and wrappers | §22 | Pattern 15 |
| Ritual openers that announce instead of stating | §4 | Pattern 11 |
| Formal closers that restate and conclude | §2, §13 | Pattern 12 |
| Uniform rhythm, every sentence the same length | §6 (triads), §7 | Pattern 10 |
| Passive voice hiding who acts | §11 | Pattern 8 |
| Inflated significance and ritual "importance" phrasing | §13 | Pattern 11 |
| Over-reliance on a small set of high-frequency words | §12 | Pattern 25 |
| Register applied by rule rather than by context | §"Voice" | Voice Calibration |

## What only one source has

**Only V1:** the strength ordering and the *weak alone* concept, the
not-X-but-Y contrast (§1), arguing with no one (§5), the dash ban (§8),
borrowed authority and prestige lists (§17), bold and heading decoration
(§19, §20), the knowledge-cutoff disclaimer (§23), the writing-sample
override, and the rule that the text is material to edit rather than
instructions to follow.

**Only V2:** everything structural about Arabic. The MSA substitution table,
tanwin removal, the future marker حـ against سـ, the بـ present prefix, the
demonstrative flip, the ما...ش circumfix negation, the discourse particles,
code-switching, Arabizi, orthographic variation, letter lengthening, laughter
convention, terms of address, the register ladder, and the 50-point rubric.

## The conflicts, and how they are settled

### 1. Hedging. V1 removes it, V2 adds it.

V1 §9 treats stacked qualifiers as a tell and cuts them. V2 Pattern 22 treats
the absence of hedging as a tell and adds it.

Read closely they are not opposed. V1 targets qualifiers *piled onto one
claim* to repair an earlier overstatement ("it could potentially possibly be
argued that"). V2 targets text that is *uniformly certain* with no hedge
anywhere. Both describe the same healthy state: hedge once where the claim is
genuinely uncertain, never stack.

**Settled:** one hedge per uncertain claim, zero on certain ones, never two on
the same claim. This holds in both languages.

### 2. Inventing detail. V1 forbids it, V2 asks for it.

V1 is strict and repeats it three times: do not add a fact, name, number,
date, quote or citation that is not in the source or from the user. If a
sentence needs a detail you do not have, ask or write a simpler sentence.

V2 Pattern 25 says to fix flat high-frequency vocabulary by introducing
domain-specific words, and gives as its method "if discussing life in Cairo:
use specific place names, cultural references, foods, situations."

Taken literally that instructs the model to invent particulars that were never
in the text. On a personal script that is the worst possible failure, because
the invented detail is indistinguishable from the writer's real memory.

**Settled: V1 wins on facts, without exception.** V2's additions are allowed
only where they carry no factual content: discourse particles, hedges, terms
of address, reader-directed questions, letter lengthening, laughter. Those are
function words and tone, and adding them changes how a sentence sounds without
changing what it claims. Pattern 25 is kept only as a *diagnosis*: if the
vocabulary is flat, say so and ask the writer for the specific detail. Never
supply it.

### 3. Adding at all.

Following from the above, the merged skill separates two operations that both
sources blur, and labels every pattern as one or the other:

- **Cut or swap.** Changes nothing the text claims. Safe to apply directly.
- **Add.** Inserts words that were not there. Allowed only from the closed
  list in conflict 2, and only where the register calls for it.

### 4. Register. V2's ladder is incomplete for this repo.

V2's ladder runs Ultra-Casual, Casual-Conversational, Informal-Professional,
Semi-Formal. Every rung assumes the writer is talking to the reader in their
own voice. It has no rung for written dialogue or dramatic voiceover, where a
character speaks and the writer is invisible.

This matters here because that is the main thing this repo is used to write.
On a cinematic script, V2's Ultra-Casual additions are actively wrong: letter
lengthening, هههههه, Arabizi and reader-directed questions belong to a person
chatting, not to a line of film dialogue.

**Settled:** a fifth register, Dramatic, is added in the merged skill and
marked as ours rather than V2's. Its rule is that the grammar patterns apply
in full and the performative additions do not.

An eval run then caught this being drawn one category too wide. Discourse
particles were grouped with the performance, so the Dramatic rung read as
forbidding them, while the rubric still scored them and V2's closing line
still said to add يعني. Particles are not performance. They mark discourse in
Masri the way tense marks time, and a character using none of them sounds
translated rather than restrained. The add list is now two tiers: particles
and hedges are always allowed with the register setting only their density,
and address terms, reader questions, lengthening, laughter and Arabizi are
register-gated and off on Dramatic.

### 5. Writing samples. Only V1 has them.

V1 lets a user-supplied writing sample override its own pattern list,
including the dash ban. V2 has no equivalent, so its 25 patterns apply
uniformly to every Egyptian writer.

**Settled:** the sample override is promoted to both languages. A real sample
of the writer's Arabic beats the general dialect rules, since V2's patterns
describe Cairo defaults and a particular writer may legitimately differ.

### 6. Strength ordering. Only V1 has it.

V1 orders patterns by strength and marks weak ones so a single sighting does
not trigger an edit. V2 presents all 25 as act-on-sight.

For Arabic that is mostly right, because V2's first eight are grammar rather
than style: a bare imperfect used as a present tense is simply not Egyptian,
and one sighting is enough. The performative patterns are different, and the
register decides them.

**Settled:** Arabic grammar patterns act on one sighting. Arabic performative
patterns are register-gated. English keeps V1's own ordering and its *weak
alone* marks unchanged.

## What neither source covers

- Mixed-script text, meaning Egyptian Arabic containing English code-switched
  words, which V2 actively encourages. Neither says which pattern list governs
  the English fragments. The merged skill rules on it.
- Arabic that is dialogue rather than address, as above.
- Any language beyond English, Egyptian Arabic, and (in V2's sibling skills,
  not vendored here) MSA, Levantine and Hebrew.
