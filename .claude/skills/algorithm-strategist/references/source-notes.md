# Source notes: How Social Media Algorithms Actually Work (And How to Beat Them)

- Source: https://youtu.be/8cQidXgtGmU
- Author: Kallaway
- Duration: 17:20

Every claim below carries a timestamp so it can be verified by scrubbing to it.

# Analysis: How Social Media Algorithms Actually Work (And How to Beat Them)

- Source: https://youtu.be/8cQidXgtGmU (Kallaway, 17:20, about 887k views at time of analysis)
- Ingestion: YouTube auto-captions via fetch_captions.py + Gemini native read via gemini_watch.py (first attempt dropped the connection; the retry succeeded)
- Frames read: 0 (video stream refused from this environment). Visual claims are Gemini's and marked "Gemini only".
- Transcript source: auto-captions; wording favors captions, on-screen text favors Gemini.

## Beat sheet

| t | On screen (Gemini only) | Spoken (captions) | Changed since last beat |
|---|---|---|---|
| 00:00 | Title "SOCIAL MEDIA ALGORITHM"; stats 1M+ followers, 1B+ views; Adam Mosseri (Head of Instagram) quote callout | Promise: more views with less effort by understanding how algorithms work; based on outlier data and statements by the Instagram CEO. Credentials. | (start) |
| 00:43 | Header "1 How Do Algorithms Actually Work?"; app icons pointing to "Goal: keep people on the platform as long as possible" | Platforms have one goal: time on platform (ads). The algorithm is "one giant matchmaker" between people and content. To be pushed, help it make better matches. | Core model stated. |
| 01:39 | Header "2 How Does The Algorithmic Matchmaking Process Work?"; phone mockup with layers: computer vision, audio fingerprinting, metadata; flow to "Analysis" then "TOPIC MAPPING"; "Fit score" | On upload the platform builds a "digital fingerprint": watches (vision), listens (transcript), reads metadata (caption, hashtags, creator, location). Combined into a topic mapping, from which it computes a fit score: who will like this. | Ingest mechanics. |
| 02:47 | Node grid: Users 100M, Sample size 200, "Most of them are non-followers" | The fit score picks about 200 people as the initial sample test group, mostly non-followers, to test how strangers react. "Followers don't matter" is roughly right for sampling. | The sampling model. |
| 03:28 | Branches: Positive (2,000 to 20,000 to 200,000), Neutral (resample 200), Negative (stop); card "What Happens After You Post" | Positive data confirms the fit score and the push scales by roughly 10x per round until data weakens. Neutral: recompute fit score, resample another 200. Negative: tighten and stop, to avoid alienating viewers. "200 view jail" means bad sample data. Even bangers fade when they run out of people. | Feedback loop. |
| 05:21 | Header "4 How to Hijack The Algorithm"; "Hack the Algorithm in 2 Steps" | Two things only: 1. help the algorithm build a better fit score so the first 200 are the right people; 2. make sure that sample engages. | Turn to tactics. |
| 06:00 | Promo card, shortformsystem.co | Free content system guide. | Promotion. |
| 06:35 | Header "5 How to Help It Build The Right Fit Score"; "Talks about X topic for Y avatar profile"; "AUDIENCE MATCHING"; diagram of tech, health, politics videos blending | Answer: consistently make videos about the same topic for the same audience avatar, over and over. After a few similar videos the algorithm knows "X topic for Y avatar" and reuses those sample groups. Mixed topics give mixed data; a confused algorithm pushes less. Example: tech, health, politics, then a fourth health video gets a blended fit score and flops. Say no to viral-looking ideas for the wrong audience; one off-audience hit poisons the next several videos. Beginners "spray and pray". | Side one of the equation. |
| 09:14 | Header "6 How to Make Sure Your Sample Group Engages Well"; "3 Metrics That Matter for Sample Data" | Three metrics: average watch time (and percent completion), engagement rate (likes + comments + shares + saves + reposts over views), and watch time session share (share of a viewer's session spent on your videos; not visible to creators). | Side two: what is measured. |
| 10:50 | Slide "4 Ways to skyrocket engagement in your videos" with the four attributes and a layman's translation | Four attributes of a video that lift engagement: 1. topic highly relevant to the ideal viewer (solves a problem they have); 2. information non-obvious and tactically implementable; 3. high absorption (they can understand it); 4. short distance to implement (small action, big result). In plain words: cover a core pain, say something useful, say it understandably, make it applicable. Same four turn viewers into buyers. | The content quality bar. |
| 12:40 | Screen recording of sandcastles.ai: channel list, outlier score filter, video detail tabs (Transcript, Idea Analysis, Hook, Storytelling Format, Visual Layout) | Easiest way to pick topics: study what already works in your niche; filter competitor channels by outlier score, inspect hook and storytelling, remix. Few people use data for topic decisions. | Research tooling. |
| 13:50 | Header "7 How to Drive More Comments"; five tactics list | Bonus: five ways to drive comments. 1. Take a hard stance (people comment when they disagree). 2. Be contrarian (majority thinks you are wrong). 3. Amplify the take (more extreme framing: "better than every mom-and-pop pasta shop"). 4. Build around cult-loved brands, people, ideas, movements (Nike vs "shoes"). 5. Drive significant emotion. All feed back into right topic for right group. | Engagement lever. |
| 15:48 | Recap cards; crossed-out badges "Posting time", "Hashtags", "Captions" | Recap. Settings hacks and caption tweaks do not work: posting time, hashtags, captions do not matter. The only thing that matters is great videos for a specific avatar across a narrow band of topics, repeatedly. "That is the cake. Everything else is the icing." Comments inform future videos. | Close. |

## Structure

- Opens: problem-and-promise hook, authority (CEO quote), credentials, within 45 seconds.
- Holds attention: one mechanical model (fingerprint, fit score, 200 sample, scale or stop) explained with a consistent visual metaphor, then every tactic tied back to that model.
- Turns: 05:21 (theory to hijack), 09:14 (fit score side to engagement side), 13:50 (bonus comment tactics), 15:48 (myth-busting close).
- Closes: cake versus icing, call to action, request for comment topics.

## Procedure (as taught)

1. Pick one audience avatar and a narrow band of topics; make the same kind of video for the same person repeatedly (audience matching). Refuse off-avatar ideas even if they look viral. (t=06:35 to 09:14)
2. For each video, check the four engagement attributes: relevant to the avatar's real problem, non-obvious and implementable, absorbable, short distance to result. (t=10:50 to 12:40)
3. Choose topics from data: study outlier videos in the niche, inspect their hooks and storytelling, remix. (t=12:40 to 13:50)
4. To lift comments, take a hard, contrarian, amplified stance on a cult-loved subject with emotion. (t=13:50 to 15:48)
5. Read performance through the sampling model: a flop means the first 200 gave bad data (wrong fit or weak engagement); diagnose which side failed. (t=02:47 to 05:21)
6. Ignore posting time, hashtags, and caption tricks. (t=16:10)

## Verbatim assets

From captions unless marked Gemini only.

- "Social media companies only have one goal, to keep people on the platform as long as possible." (t=00:50) "The algorithm is just one giant matchmaker." (t=01:05)
- The post-upload sequence (Gemini only card, confirmed by speech at t=04:50): you post; the algorithm maps the topic; it tests on about 200 viewers; it boosts, retries, or stops.
- "Hack the Algorithm in 2 Steps: 1 Help the algorithm build a better fit score so it can find the best 200 person sample group initially. 2 Make sure that sample group actually engages strongly with your video." (Gemini only card; speech t=05:20)
- "All you have to do is consistently make videos about the same topic for the same audience avatar over and over and over." (t=06:45) "To improve fit score, keep your topic and audience consistently narrow." (Gemini only card)
- "Even one viral hit to an audience outside of your core demo will result in the next several videos having poor sample data because it confuses the algorithm." (t=08:45)
- Three metrics (Gemini only card wording): average watch time and percent completion; engagement rate = (likes + comments + shares + saves + reposts) / views; watch time session share.
- Four ways (Gemini only card): 1 topic highly relevant (solves a problem they have); 2 non-obvious and tactically implementable; 3 high absorption rate; 4 short distance to implement. Layman's: cover a core pain point; have something useful or interesting to say; say it in a way they understand; they can apply it on their own.
- Five comment tactics (Gemini only card, confirmed in speech): Take a Hard Stance; Be Contrarian; Amplify Your Take; Use Polarizing Topics (brands, people, issues with strong opinions); Trigger Emotion.
- Amplification example: "This is the best way to cook pasta" vs "This pasta is better than all the mom and pop pasta shops in the world." (t=14:40) Cult-loved example: Nike vs the category of shoes. (t=15:05)
- "Posting time does not matter. Hashtags in your captions don't matter. The captions themselves don't matter. The only thing that matters is making great videos for a specific avatar group across a narrow band of topics over and over and over. That is the cake. Everything else is the icing." (t=16:10)

## Inferences and gaps

- (gap) No frames; card wording is Gemini's reading. The long list of Instagram URLs Gemini transcribed from the Sandcastles demo is irrelevant to the skill and omitted.
- (inference) The presenter's numbers (200, 10x steps, 100M) are illustrative of a mechanism, not documented platform constants; the skill should present them as a mental model.
- (gap) No method for defining an avatar or a topic band; the video assumes you have one. The skill must supply a lightweight worksheet.
- (gap) No method for auditing an existing channel's topic consistency; the skill should supply one.
- (gap) The comment tactics can be applied unethically (manufactured outrage). The skill should keep stances honest: real opinions, amplified framing, not fabricated conflict.
- (gap) Nothing on how the four attributes interact with hooks and storytelling; the skill should hand those off to hook-writer and story-loop-writer.

## Three highest-signal observations

1. Distribution is a sampling loop: about 200 mostly non-follower viewers see the video first, and the platform scales, resamples, or stops based on their watch time and engagement. A flop is bad sample data, not bad luck. (t=02:47 to 05:21)
2. The single highest-leverage move is audience matching: the same topic band for the same avatar, repeatedly, so the fit score sharpens; one off-avatar video, even a viral one, muddies the next several. (t=06:35 to 09:14)
3. Engagement comes from four content attributes (relevant, non-obvious and implementable, absorbable, short distance to result), and everything else (posting time, hashtags, captions) is icing. (t=10:50 to 12:40, t=16:10)

