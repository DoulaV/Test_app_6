# Producing Instagram Reels in Egyptian Arabic with the six skills

This is the working guide for going from "I need ideas" to a finished
Egyptian Arabic Reel script using the six skills in this repo. They were
built by `youtube-to-agent` from five Kallaway videos, one Jay Yang
copywriting course and one Caleb Ralston personal-brand course, and they run
in a fixed order:

| Order | Skill | Decides | Source video |
|---|---|---|---|
| 0 | `brand-architect` | Who you are, what you are known for, what you refuse | How to Build a Personal Brand (Full Course) |
| 1 | `algorithm-strategist` | What to make, for whom, with what stance | How Social Media Algorithms Actually Work |
| 2 | `brand-idea-miner` | Which validated idea, remixed how, with what proof | The Power of Suggestion + Idea Mining (two videos) |
| 3 | `hook-writer` | The first three lines and the on-screen text | How to Create Irresistible Hooks |
| 4 | `story-loop-writer` | The body: stakes, big question, head fake, re-hook | The Neuroscience of Addictive Storytelling |
| 5 | `copy-sharpener` | The actual words, the on-screen text, and the close | How To Write Words That Make People Buy |
| 6 | `humanizer` | Whether it still sounds like a machine wrote it | blader/humanizer + OthmanAdi/humanizer-semitic |

You do not need to name the skills. Claude Code triggers them from the
request. Naming them is fine when you want to force the order.

## Part 1: One-time setup (do this once)

### Fix who you are (brand-architect)

Do this before the avatar, because the avatar is derived from it. Ask Claude:

> Using brand-architect. I post [what] in Egyptian Arabic. I have [N]
> followers. My best video did [N] views and the comments said [paste 5 to 10
> real comments]. What I eventually want out of this is [outcome]. Audit what
> my brand already is, then define it.

You get back: one association sentence, the Brand Journey table, the two
association lists (kept and refused), your position, the brand story in three
parts, the pillar split, and the expansion path. Save all of it in one note.
Everything below pastes from that note.

Two parts of it you will use weekly. The **refusal list** answers every
collaboration, sponsorship and podcast invitation without asking again. The
**pillar split** tells you how much of your output may go off the core topic,
which for most accounts should start at zero and rise only once reach is
reliable. Read "The off-band budget" in the skill for the exact percentages.

Egyptian Arabic note: the skill's "share your failures" advice is written for
an audience that reads confession as candour. Where your audience would read
it as complaint, buy the same trust with specificity instead: the exact
number, the exact month, the decision that cost you something. The skill has
a section on this ("Building a brand outside English").

### Fix the avatar and topic band

Ask Claude:

> Using algorithm-strategist, help me define my avatar and topic band. My
> account is about [topic]. My viewers are Egyptian, aged [range], living in
> [Cairo / Alex / the Gulf diaspora], and their problem is [problem]. Here
> are 10 accounts they already watch: [...]

You get one sentence in the form "<topic band> for <avatar>". Save it. Every
later request pastes it back in. The whole method depends on making the same
kind of video for the same person repeatedly; one off-topic viral video
costs you the next several.

### Fix the voice

Write a short voice note and paste it into every scripting request:

> Voice: Egyptian Arabic (عامية مصرية), the way [a friend / an older sister /
> a sharp colleague] talks. Use "بس" not "لكن", "بكرة" not "غداً", "ليه" not
> "لماذا", "عايز" not "أريد". Numbers spoken the Egyptian way. No Modern
> Standard Arabic except in on-screen headings if you want them to feel
> official. Short sentences. One idea per line.

Adjust the register to your persona. Egyptian Arabic has its own sub-registers
(Cairo casual, more formal media Egyptian, Sa'idi flavour) and the skill will
hold whichever you specify, but only if you specify it.

### Save your first hit of value

Both hook-writer and story-loop-writer will ask, or assume, what the viewer
learns in the first seconds. Have the one concrete takeaway of each video
written down before you start; scripts written without it come back with
bracketed placeholders you must fill.

## Part 2: The weekly loop (every batch of Reels)

### Step 1: Choose the next videos (algorithm-strategist)

> Using algorithm-strategist. Avatar and band: [paste]. Here are my last 8
> Reels with views: [list]. Here are 10 ideas: [list]. Audit consistency,
> diagnose the flops, and tell me which 3 to make next with a stance for each.

What you get back: a consistency table, a fit-versus-engagement diagnosis of
any flop, three to five ideas each with the avatar's pain, the non-obvious
point, the small action, and a stance line, plus a "stop doing" list.

Keep the stance honest. The skill will amplify the framing of an opinion you
actually hold; it will not invent outrage, and you should not ask it to.
Cult-hopping anchors work well in Egypt: a famous brand, a well-known TV
host, a football club, a proverb everyone knows. Pick ones your avatar has
opinions about.

### Step 1b: Mine and shape the ideas (brand-idea-miner)

When you are out of ideas, or want to beat a reference reel rather than guess:

> Using brand-idea-miner. Avatar and band: [paste]. Voice: [paste]. Here are
> 10 to 20 accounts my viewer already watches: [...]. Set up my research,
> log the outliers you can see from what I paste, and give me a ranked
> shortlist with hold/remix, the collision, the five-element check, and the
> proof plan for each.

Egyptian-specific notes: collision sources that land with Egyptian viewers
include proverbs (أمثال), football, Ramadan routines, family dynamics, and
public figures your avatar already has opinions about. Proof stays honest:
Egyptian audiences punish inflated numbers in the comments, so borrowed proof
is cited and own results are exact.

### Step 2: Write the hook (hook-writer)

> Using hook-writer. Avatar: [paste]. Voice: [paste]. Format: Instagram Reel,
> vertical, under 45 seconds. Topic: [idea from step 1]. Stance: [stance from
> step 1]. First value hit: [your takeaway]. Give me 4 candidates in
> Egyptian Arabic with English glosses, and the on-screen text.

Each candidate comes back as Lean, Stop, Snap, on-screen text, opening
visual, first value hit, and why it works, with a recommendation.

Egyptian-specific checks on the result:

- The Stop line should start with "بس" (or "لكن" if your persona is more
  formal). If it comes back with "لكن" in a casual voice, ask for a redo.
- On-screen text: three to five words, right-to-left, in a font with real
  Arabic ligatures. Avoid Latin-script brand names in the first frame unless
  the brand is the hook.
- The 4-second rule still applies: the on-screen text and line one must land
  the topic in the first second; the first payoff by about second four.

### Step 3: Write the body (story-loop-writer)

> Using story-loop-writer. Avatar: [paste]. Voice: [paste]. Format: Instagram
> Reel, 45 seconds. Here is the hook we chose: [paste candidate]. Here is what
> actually happened / the facts: [list]. Write the body as one master loop
> and give me the clean recordable copy.

You get a labelled draft (stakes, big question, head fake, re-hook), a
head-fake check table, a clean copy with labels stripped, and the assumed
audience line.

Egyptian-specific checks on the result:

- The re-hook bridge phrases should be Egyptian: "وده بالظبط اللي..."
  ("which is exactly why"), "بس المشكلة إن..." ("but here's the problem"),
  "وساعتها فهمت إن..." ("and that's when I realized").
- Word budget: Egyptian Arabic runs slightly slower spoken than English, so
  plan about 2.2 to 2.6 words per second. A 45-second Reel holds roughly 100
  to 115 Arabic words; a 30-second one 65 to 80.
- Placeholders in square brackets are facts you did not supply. Replace or
  cut every one before recording; do not keep a detail that is not true.

### Step 3b: Sharpen the words (copy-sharpener)

Your on-screen Arabic text is the primary carrier, so it is worth a pass of
its own:

> Using copy-sharpener. Here is the full script: [paste]. Voice: [paste].
> Line-edit the on-screen text against the five tests, keep the register
> consistent (dialect, not Modern Standard), and write me a close.

Arabic-specific notes it applies: Hemingway and the fifth-grade reading rule
do not work here, so it uses the read-aloud and squint tests instead; cadence
is judged on clause length rather than syllables; and mixing Modern Standard
with dialect reads as a translation, so it holds one register throughout.

For emotional pieces it will not bolt a sales close onto the ending. It
softens to a single question, which is also what fixes a low comment count.

### Step 3c: Strip the AI residue (humanizer)

> Using humanizer. Register: Dramatic. This is voiceover for a cinematic short
> film in Egyptian Arabic. [paste the script]

The Egyptian pattern list catches what a general-purpose skill cannot: MSA
vocabulary that crept in (الآن instead of دلوقتي, جداً instead of أوي), tanwin,
سوف futures where Masri wants هـ, a bare imperfect missing its بـ prefix,
هذا before the noun instead of ده after it, MSA negation instead of ما...ش,
and a paragraph with no يعني or بقى anywhere in it. One جداً is enough to mark
a text as machine-written.

Say **Dramatic** every time for film work. Without it the skill assumes you
are writing a post and starts adding هههههه, letter lengthening and reader
questions, which belong in a chat and not in a character's mouth.

For English captions and your bio, drop the register line and it uses the
English list instead.

### Step 4: Assemble and check

Paste hook plus body into one script and ask:

> Audit this full script with story-loop-writer, then check the opening with
> hook-writer. Where does attention drop?

Fix what comes back, then run the four-attribute check yourself: does it
solve the avatar's real problem, say something non-obvious they can act on,
in words they absorb, with a short distance to the result?

### Step 5: Record and post

- On-screen text on frame zero, spoken first word at 0.0 seconds, no
  greeting.
- One subject with modest motion in the opening visual (a lean toward the
  camera, setting an object down).
- Posting time, hashtags, and caption tricks do not matter per the source.
  Spend that time on the next script.

### Step 6: Feed results back

Every week, paste the views and any comments into Step 1. Flops are
diagnosed as fit problems (wrong 200 viewers, usually an off-band topic) or
engagement problems (right viewers, weak on one of the four attributes), and
the next batch adjusts.

## Part 3: A worked request, start to finish

Topic: procrastination, cinematic short, Egyptian Arabic. Avatar: "beating
procrastination on studies and side projects, for Egyptians 18 to 28 who
scroll at night feeling guilty".

1. algorithm-strategist confirms the topic is on band, proposes the stance
   "التسويف مش كسل، التسويف خوف" (procrastination is not laziness, it is fear)
   and anchors it to the university exam season everyone in the avatar has
   lived through.
2. hook-writer returns four candidates; the pick is a Tomorrow-as-a-place
   hook: Lean "كلمة 'بكرة' أكتر كلمة قلتها في حياتك. قلتها النهاردة كمان." Stop
   "بس بكرة مش يوم." Snap "بكرة مكان. مكان بتبعت له كل حاجة خايف تطلع فيها
   وحش، وعمرك ما بتزوره." On-screen text: "بكرة مش يوم".
3. story-loop-writer builds the body: stakes (a real deadline, what it costs,
   the clock), big question (what actually happens to the things you send to
   tomorrow), head fake on the cause (the fear is of succeeding at something
   you do not want, planted by a clue earlier), re-hook into a question the
   viewer answers in the comments ("إيه آخر حاجة بعتّها لبكرة؟").
4. The clean copy is checked for word count (about 110 words for 45
   seconds) and for "بس" over "لكن", then recorded with the on-screen text on
   frame zero.

## Part 4: Common failures and the fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Views stuck in the low hundreds after a good run | An off-band video muddied the fit score | Audit with algorithm-strategist; run several same-band videos |
| Big views, very few new followers | Nothing tells the viewer there is more of this; the association is stranded | brand-architect audit; the drift shape is *stranded* |
| A large audience that does not trust or buy | One thing in common only, no second interest, no brand story | brand-architect: spend the off-band budget, and publish the catalyst |
| Unsure whether to accept a collab or sponsorship | No refusal list | brand-architect, step 4 |
| People leave at 2 to 3 seconds | Hook has no stop line, or on-screen text missing on frame zero | hook-writer critique mode |
| People leave in the middle | A resolution with dead air after it, or a vague teaser | story-loop-writer audit mode |
| Script sounds translated | Voice note missing or too thin | Add specific phrase swaps and a persona to the voice note |
| Lots of views, no comments | Hedged take | Ask algorithm-strategist for an honest, amplified stance |
| Claude keeps inserting bracketed placeholders | You did not give the facts or the first value hit | Supply them up front in the request |
| The Arabic reads stiff, like a news bulletin | MSA crept into the dialect | humanizer, Egyptian list: check جداً, tanwin, سوف, missing بـ, هذا before the noun |

## Part 5: Extending the system

Any new tutorial can become another skill with `youtube-to-agent`: share the
link and say "turn this into a skill and cross-link it with the others".
Candidates that would slot into this pipeline: a video on editing pace and
cuts for Reels, one on caption-free visual storytelling, one on Egyptian
Arabic copywriting register, and a production-operations skill covering
cadence, the waterfall distribution model (one long piece becomes ten), and
batching, which is the largest remaining gap in this system.
