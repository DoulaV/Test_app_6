# The analysis framework (System 3, part 1)

This is the prompt shown in the source video for turning `/watch` output into
something an agent can learn from. Apply it yourself when you have frames and a
transcript in context. `scripts/gemini_watch.py` sends the same block to Gemini
when it reads a YouTube URL directly, so both paths produce comparable output.

## The prompt, verbatim

```prompt
You're ingesting a /watch output: a set of timestamped frames plus a timestamped transcript of one video. Treat frames as what was seen and transcript as what was said, and merge them into a single timeline before drawing any conclusion. Build that timeline as beats (timestamp, what's on screen, what's spoken, what changed since the last beat), then read across it for structure: how it opens, how it holds attention, where it turns, how it closes. Report only what the frames or transcript actually show, marking anything inferred as inference and anything the sampling could have missed as a gap. Finish with the three highest-signal observations and cite timestamps for each.
```

## Why each clause is there

- **"Treat frames as what was seen and transcript as what was said."** The two
  channels lie in different ways. Speech recognition mangles names and code;
  frames miss anything that happened between samples. Keeping them separate
  until the merge step stops one channel from silently overwriting the other.
- **"Merge them into a single timeline before drawing any conclusion."**
  Conclusions drawn from the transcript alone drop every step that was shown
  but not narrated. Tutorials are full of those.
- **"Beats."** A beat is a change: a new screen, a new command, a new point in
  the narration. The "what changed since the last beat" column is where the
  procedure lives. If two adjacent frames are the same talking head and the
  narration continues the same point, that is one beat, not two.
- **"Read across it for structure."** Opening, attention holds, turns, close.
  For a tutorial the "turns" are usually the boundaries between steps or
  between systems, which is exactly the outline the generated skill needs.
- **"Report only what the frames or transcript actually show."** The
  generated skill inherits every hallucination in the analysis. Mark
  inference as `(inference)` and sampling gaps as `(gap)` so the spec step
  can route them into `gaps` instead of `procedure`.
- **"Three highest-signal observations with timestamps."** These become the
  headline of the final report and the sanity check for the user: if the
  three observations are wrong, everything downstream is wrong, and they can
  verify each one by scrubbing to the timestamp.

## Output template

Write `analysis.md` in this shape:

```markdown
# Analysis: <video title or filename>

- Source: <url or path>
- Duration: MM:SS
- Ingestion: /watch | local_ingest | gemini | (several)
- Frames read: N   Transcript source: captions | whisper | gemini

## Beat sheet

| t | On screen | Spoken | Changed since last beat |
|---|---|---|---|
| 00:00 | ... | ... | (start) |
| 00:14 | README of github.com/x/y, install commands visible: `...` | "first you need this repo" | cut from talking head to browser |

## Structure

- Opens: ...
- Holds attention: ...
- Turns: t=..., t=... (these are the step boundaries)
- Closes: ...

## Procedure (as taught)

1. ... (t=00:14, t=00:20)
2. ...

## Verbatim assets

Copied from frames, character for character. Say which frame.

## Inferences and gaps

- (inference) ...
- (gap) Frames sampled every 2s; a fast scroll at ~t=00:31 may have skipped content.

## Three highest-signal observations

1. ... (t=..)
2. ... (t=..)
3. ... (t=..)
```

## Practical notes

- Read frames in timestamp order, in parallel batches of 6 to 10. Skip frames
  that duplicate the previous one (talking head, static slide).
- When a frame shows a phone screenshot or a notes app, transcribe the whole
  visible text into "Verbatim assets". That text is usually the payload of
  the video.
- When the Gemini read and the frames disagree, record both and mark the
  disagreement. Decide in the spec step, with the frames winning for
  anything textual and Gemini winning for motion, audio cues, and anything
  between frame samples.
- Truncated on-screen text (a command cut off at the edge of a screenshot)
  is a `(gap)`. Resolve it with a web lookup and mark the resolution as
  "(verified externally)" rather than presenting it as seen.
