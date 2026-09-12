---
name: algorithm-strategist
description: Plan and audit content strategy using Kallaway's model of how social algorithms distribute videos: digital fingerprint, fit score, a first sample of about 200 mostly non-follower viewers, then boost, retry, or stop. Covers choosing one audience avatar and a narrow topic band (audience matching), scoring video ideas against the four engagement attributes, diagnosing why a video flopped or got stuck at low views, and driving comments with honest stances. Use this whenever the user asks why their reels, shorts, TikToks, or videos are not getting views, mentions 200-view jail, a flop, low reach, the algorithm, shadowbans, posting times, hashtags, niching down, picking a niche or target audience, content pillars, a content calendar or strategy, or asks which video idea to make next, even if they never say the word algorithm. Also use it to review a list of past or planned videos for topic consistency.
---

# Algorithm Strategist

Given a creator's audience, past or planned videos, and goals, define the avatar and topic band, audit consistency, score ideas against the four attributes, diagnose flops using the sampling model, and recommend the next videos and comment stances.

Learned from: How Social Media Algorithms Actually Work (And How to Beat Them) (https://youtu.be/8cQidXgtGmU). The timestamped beat sheet is
in `references/source-notes.md`; anything copied from the screen is in
`references/verbatim-assets.md`.

## Related skills

This skill decides what to make and for whom. `hook-writer` writes the first
three lines of the chosen video; `story-loop-writer` structures the body.
When a user asks for a full plan or a full script, run this skill first to
fix the avatar, topic, and stance, then hand the chosen idea to the other
two. When they ask why a specific video underperformed, this skill diagnoses
fit versus engagement, and the other two fix the script if engagement was
the problem.

When the user needs actual video ideas rather than a verdict on which of
their own ideas to make, hand the avatar and band to `brand-idea-miner`,
which mines outliers in the niche and shapes them into ideas that pass the
five obsession elements.

`copy-sharpener` writes and sharpens the words once this skill has fixed the
avatar, including the call to action that converts a viewer into a follower.

## Prerequisites

- Who the creator wants to reach (or enough about their business to infer it), the platform, and a list of recent or planned video topics with rough performance if available. Ask for the audience if missing; every recommendation hangs on the avatar.

## Procedure

1. **Explain performance through the sampling model before giving advice.** On upload the platform fingerprints the video (visuals, transcript, metadata), maps its topic, and computes a fit score for who will like it. It shows the video to about 200 people, mostly non-followers, then boosts by roughly 10x per round on positive data, resamples another 200 on neutral data, or stops on negative data. A flop or '200 view jail' means the first sample returned bad data, so every diagnosis asks two questions: did it reach the wrong 200 (fit score problem) or did the right 200 not engage (content problem)? Present the numbers as a mental model, not platform constants. (see source-notes: t=01:39, t=02:47, t=03:28, t=04:30)
2. **Define one audience avatar and a narrow topic band, and write them down as 'X topic for Y avatar'.** The highest-leverage move is audience matching: after a few similar videos the algorithm learns 'this channel talks about X for Y' and reuses the sample groups that worked. Mixed topics (tech, then health, then politics) produce a blended fit score and weak sample data, so the next video flops regardless of quality. (see source-notes: t=06:35, t=07:00, t=07:45, t=08:30)
3. **Audit the recent and planned videos for consistency against that avatar and band, and flag off-avatar ideas even when they look viral.** One viral hit to the wrong audience poisons the next several videos' sample data because it confuses the fit score. Beginners spray and pray; discipline in topic and audience selection is the difference. (see source-notes: t=08:45, t=09:00)
4. **Score each idea against the four engagement attributes before it is made.** Sample data is judged on average watch time and completion, engagement rate (likes, comments, shares, saves, reposts over views), and watch time session share. Four content attributes raise all three: the topic solves a real problem the avatar has; the information is non-obvious and tactically implementable; the viewer can absorb it; there is a short distance between the advice and the result. In plain words: a real pain, something useful, said understandably, applicable on their own. The same four attributes turn viewers into buyers. (see source-notes: t=09:30, t=10:50, t=11:30, t=12:00, t=12:25)
5. **Pick topics from evidence: find the outlier videos in the niche, note their topic, hook, and storytelling shape, and remix rather than guess.** Few creators use data to choose topics. Studying what already over-performs for the same avatar nearly guarantees relevance. The presenter uses a tool (Sandcastles) for this; the manual version is a list of ten competitor accounts and their top posts by views relative to their average. (see source-notes: t=12:40, t=13:05, t=13:25)
6. **For each recommended video, propose an honest stance that will draw comments: pick a side, prefer the contrarian side when you actually hold it, amplify the framing, anchor to a cult-loved brand, person, or idea, and aim for a real emotion.** People comment when they disagree or feel strongly. Hedged takes get silence. 'This pasta is better than every mom-and-pop pasta shop' draws more discussion than 'this is the best way to cook pasta'; a stance on Nike draws more than a stance on shoes. Comments are engagement data that feeds the boost. (see source-notes: t=13:50, t=14:10, t=14:40, t=15:05, t=15:20)
7. **Tell the user what to stop worrying about: posting time, hashtags, and caption tricks.** The presenter is explicit that none of these move the needle. The cake is great videos for a specific avatar across a narrow band of topics, repeatedly; everything else is icing. Time spent on settings is time not spent on the avatar and the four attributes. (see source-notes: t=16:10, t=16:30)

## Decision rules

- When the user reports a flop or a video stuck around a few hundred views: run the two-question diagnosis: was the topic or framing off-avatar compared with the channel's recent videos (fit score), or was it on-avatar but weak on one of the four attributes (engagement)? Name which, with the evidence from their list (see source-notes: t=04:30, t=05:20)
- When the user asks whether to make an idea that is trending or looks viral but serves a different audience: recommend against it, or suggest reframing it for the avatar; explain the cost to the next several videos (see source-notes: t=08:45)
- When the user is starting a new account or has under a few dozen posts: spend the first run of videos (roughly 10) on one topic band for one avatar with no detours, so the algorithm can learn the match (see source-notes: t=06:55, t=09:00)
- When the user asks about posting time, hashtags, captions, or settings: say they do not matter per the source, redirect to avatar, topic band, and the four attributes (see source-notes: t=16:10)
- When the user has no avatar or several: help them choose one using the worksheet (who, what pain, what they already watch), and treat other audiences as future separate accounts (see source-notes: t=06:45, t=07:20)
- When the user wants more comments: propose stances the creator genuinely holds, amplified in framing and anchored to a familiar brand or figure; never invent outrage (see source-notes: t=13:50, t=15:20)
- When the recommendation touches the opening lines or the body of a script: hand off to hook-writer for the hook and story-loop-writer for the body; this skill decides what to make and for whom (see source-notes: t=10:30)

## Known gotchas

- Chasing a trend outside the avatar because it might go viral. Fix: Skip it or reframe it for the avatar; the cost is several weak videos afterward. (see source-notes: t=08:45)
- Blaming settings, posting time, or hashtags for low reach. Fix: Look at topic consistency and the four attributes instead. (see source-notes: t=16:10)
- Content that is relevant but obvious, or non-obvious but impossible to act on. Fix: Require both non-obvious and implementable; add the small action that produces the result. (see source-notes: t=11:05, t=11:30)
- Hedged, middle-of-the-road takes. Fix: Pick a side the creator actually holds and state it strongly. (see source-notes: t=14:05)
- Treating 200, 2,000, 20,000 as documented platform numbers. Fix: Present them as the presenter's illustrative model of a sampling mechanism. (see source-notes: t=02:50)

## Output format

Open every answer with the diagnosis or the decision in two or three
sentences, then support it. Use these blocks as they apply:

**Avatar and band statement.** One line in the form the source uses:
"<topic band> for <avatar>". Example: "home strength training without
equipment, for women 25 to 40 who work from home and hate gyms".

**Consistency audit table** (for any list of past or planned videos):

```
| Video | Topic | On avatar? | Relevant | Non-obvious + doable | Absorbable | Short distance | Result / verdict |
```

Score the four attributes as yes, partly, or no. "On avatar?" takes yes,
no, or adjacent; adjacent means it hits the avatar's pain but recruits a
different crowd (a rant about gym prices for a home-workout channel), and
those are the videos most worth reframing rather than dropping. When the
user describes a batch of videos as a group, score them as one row and say
that splitting them out would sharpen the verdict.

**Flop diagnosis.** Two lines: "Fit score side: ..." and "Engagement side:
...", each with the evidence from the user's own list, then the verdict on
which side failed. When both are plausible, name the primary one and give
the test that separates them: post several same-band videos with a clear
point of view; if the first few climb off the floor, fit was the problem;
if they do not, engagement is, and the hook and story skills take over.
The source says an off-avatar hit hurts "the next several videos"; treat
that as roughly the next five to ten posts, not a permanent mark.

**Next videos.** Three to five ideas, each with: the avatar's pain it
solves, the non-obvious point, the small action and its result, and a
stance line (see comment tactics). Say which to post first and why.

**Stop doing.** One short list. Always include it when the user mentioned
posting time, hashtags, caption tricks, or settings; otherwise a single line
is enough, since most creators are spending effort there without saying so.

**Hand-off.** One closing line pointing to `hook-writer` for the opening and
`story-loop-writer` for the body of whichever video was picked first.

Sequencing a new account: post the video that is strongest on all four
attributes and most unmistakably on band first, because it sets the
fingerprint; save conversion pieces (tours, offers) until the band is
established. When the sharpest-fingerprint video and the biggest comment
magnet differ, fingerprint wins for the first post and the comment magnet
goes second, since comments only help once the sample is the right people.
When the user gives an audience but no platform, assume vertical short-form
and say so.

## Avatar and topic band worksheet (not shown in the video)

The video assumes you already have an avatar. To define one from scratch,
answer these with the user:

1. Who exactly is watching? One person, described by situation, not by
   demographics alone ("a 28-year-old in Cairo who just got their first
   salary and has no idea where it goes").
2. What three problems does that person have that the creator can actually
   solve?
3. What do they already watch on this topic? Name accounts. Their top
   posts, measured against the account's own average, are the evidence for
   step 5 of the procedure.
4. What can the creator say about those problems that most creators cannot
   or will not? That is the topic band.
5. Write the band as "<topic band> for <avatar>". If it needs "and" between
   two unrelated topics, it is two bands; pick one.

Any other audience the creator cares about becomes a separate account later,
not a second lane on this one.

## Honesty boundary for comment tactics (not shown in the video)

The five tactics work because people react to conviction. They stop working,
and start costing trust, when the conviction is faked. Amplify the framing
of an opinion the creator genuinely holds; never invent a stance, fabricate
a claim about a brand or person, or bait outrage on topics the creator does
not care about. Stances about real people and brands stay opinion and
comparison, not factual allegations.

## Reading the numbers (not shown in the video)

The 200-viewer sample, the 10x steps, and 100 million users are the
presenter's illustration of a mechanism, not published platform constants.
Use them to reason ("the first few hundred viewers decide the push"), and
say so when a user asks whether they are exact.

## Worked example

From the source at t=07:45: a channel posts tech, then health trends, then
politics, then another health video. The fourth video gets a blended fit
score drawn from all three audiences, its sample data comes back weak, and
it flops even if it is good. The fix is not a better fourth video; it is a
run of same-band videos so the fit score sharpens.

## References

- `references/source-notes.md`: the beat sheet, structure, and the three
  highest-signal observations, all with timestamps. Read it when a step here
  is unclear or when the user asks what the video actually showed.
- `references/verbatim-assets.md`: prompts, commands, and configs copied
  exactly from the screen. Read it before reproducing any of them.
