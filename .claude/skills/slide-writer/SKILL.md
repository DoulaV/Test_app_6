---
name: slide-writer
description: |
  Plan, write, build and review business presentations in the style of the top
  strategy consulting firms (McKinsey, BCG, Bain): a storyline carried by action
  titles, one message per slide, every slide laid out as a table of rows and
  columns, charts chosen and stripped to the data, and a polishing pass for
  alignment and consistency. Use this whenever the user wants a presentation,
  deck, slides, PowerPoint, Keynote or Google Slides, a pitch deck, board or
  leadership update, steering committee, management or client presentation,
  executive summary, quarterly review or report deck; asks for slide titles, a
  storyline, an agenda or the structure of a deck; wants a chart or table turned
  into a slide; asks why their slides look unprofessional, cluttered or amateur;
  or shares a slide or deck for feedback, even if they never say the word slide.
  Also use it to check slides an AI tool or script generated, and to write the
  executive summary or introduction of a business document.
---

# Slide Writer

Build and review business presentations the way the top strategy consulting firms
do: the argument carried by the slide titles, one message per slide, every page a
table of rows and columns, charts stripped to the point they make, and a polishing
pass nobody skips.

Learned from the Firm Learning slide-writing playlist by Heinrich, a former
McKinsey consultant who taught slide writing inside the firm. 22 of its 23 videos
were read from captions; one (V03) was blocked. Every rule below cites a video and
timestamp in `references/source-notes.md`. Anything marked *(not from the videos)*
is filled in and worth verifying.

## Where this sits among the other skills

This skill decides **what the deck says and how each page is built**. It does not
write the file by itself.

- To produce an actual `.pptx`, use a pptx or presentation-building skill if one
  is installed, apply the rules here while building, then run the linter
  (`scripts/lint_pptx.py`) before handing anything over.
- If the organisation has a template or brand skill, its fonts, colours and master
  layouts win. This skill's structure and rules apply inside the template.
- `copy-sharpener` sharpens the words on the page; `humanizer` is the last pass,
  in English or Egyptian Arabic.

## Before you start

You need three things:

1. **The occasion and audience.** Who reads it, and what decision or reaction it
   should produce.
2. **How it will be consumed.** Presented live with you in the room, or sent,
   printed and forwarded without you. This decides the density of every page.
3. **The facts.** Data, notes, a briefing. Do not invent numbers to make a title
   quantified; mark the slot `[number needed]` and list it as an open question.

**Proceed, do not stall.** When the audience, the delivery mode or some facts are
missing, go ahead: state your assumption in one line at the top, put
`[number needed]` wherever a figure belongs, and end with the open questions whose
answers would change the work. Ask before starting only when the goal itself is
unknown, meaning you cannot say what decision or reaction the deck should produce.
A wrong guess about the audience costs one revision; a round of questions before
any draft costs the same and shows nothing. *(Resolution chosen for this skill;
the videos assume you know your audience.)*

Check the user's own arithmetic. If their figures do not produce the percentage
they quoted, say so and use the correct number in the title. If two figures
contradict each other (a reason accounting for more complaints than the channel it
belongs to), do not quietly pick one: build with the figure the title needs, flag
the conflict in that page's footnote, and list it first among the open questions.

**Cover page:** a deck that is presented or sent formally gets a cover with the
title, date and owner. An internal update of five pages or fewer can open straight
on the executive summary. Either way the linter checks slide 1 unless it looks like
a cover. *(Not from the videos.)*

## Step 1: Match the document to the occasion

The single most common mismatch is applying the wrong style. Pick the row first
(V17 t=02:00, V21 t=06:30):

| Occasion | Density and effort |
|---|---|
| Keynote to a large audience | A picture and a few words per slide. Needs a speaker; useless sent on its own. |
| Team alignment, informal discussion | Brief and plain. No storyline polish, no page design. |
| Recurring cross-team update | Agree a standing agenda once and reuse it. Keep quality up, because it gets forwarded. |
| Senior leadership or board | Nail it. Basic language, no jargon, larger type, detail in the appendix. Small inaccuracies derail the meeting. |
| External: investors, banks | Board standard, plus legal and PR review of claims such as liquidity or guidance. |
| Read-ahead or report deck | Every page self-explanatory, so enough text to stand alone. |
| Documentation | Most text and detail; must make sense years later with no author present. |

Formal decks are often never projected: they are handed out, then forwarded to
people who were not in the room, and they outlive the team that made them. That is
why a consulting page carries more than a keynote slide, and why it must survive
being pulled out of the deck on its own (V17 t=05:30, V23 t=01:00).

## Step 2: Write the storyline before building any page

1. **Sketch the whole deck first**, one box per page: a draft action title and a
   rough sketch of the chart or layout. Consultants call this a Mickey Mouse
   master, or strawman (V07 t=01:00). It takes minutes.
2. **Align on the sketch** with whoever asked for the deck, before building. The
   classic failure is a week spent alone on a polished deck that turns out to be
   the wrong one (V19 t=00:15, V07 t=05:15).
3. **Test the storyline by reading only the titles.** They must make the whole
   argument on their own: the horizontal logic. Each page's body then proves its
   title: the vertical logic (V01 t=01:00, t=02:30).

A typical arc (V07 t=02:45): the situation (the market is growing), the
complication (our share is falling to competitors), the consequence (profit falls
by a stated amount), the answer (three areas to act on), backup pages for each,
then the plan and timeline.

### Open with situation, complication, solution

For the executive summary, the first page, or a document's introduction (V13):

- **Situation:** a few sentences everyone in the room agrees with. Uncontroversial,
  but interesting enough to read on.
- **Complication:** something went wrong, could go wrong, changed, could change; a
  different point of view; three alternatives. It need not be a problem. It ends in
  the reader's most obvious next question, and answers "why act now".
- **Solution:** the answer to that question, then a preview of the structure in
  ideas, not section names. Not "we also cover enablers", but the most important
  enabler, named.

Scale it to the document: a paragraph for a short memo, a page or two for a long
report (V13 t=02:30).

**On a slide, the executive summary is still a table.** Use three rows labelled
Situation, Complication, Solution (or one row per key message), with the label in
a narrow left column and de-worded statements on the right, the key words in bold.
Sentences are allowed here, kept short, because this page must read alone. It
counts as one of the deck's pages: if the user asks for five slides, the executive
summary is slide 1 of the five unless they say otherwise. *(Layout not from the
videos; V13 gives the content, not the page.)*

## Step 3: Build each slide in five steps

The same five steps appear independently in two videos (V15 t=13:15, V19 t=03:30):
**messaging, structure, data and graphics, supporting text, polishing.** Do them in
that order. The most common mistake is to start arranging boxes before knowing what
the slide says.

### 3.1 Messaging: one message, written as an action title

An action title is a header that summarises the slide as a complete sentence
(V01 t=03:00). One message per slide, overview pages excepted (V15 t=00:30).

- Run the **so-what test**: what does this mean for the problem at hand? If there
  is no so-what, the slide belongs in the appendix or nowhere (V01 t=03:30).
- **Specific and quantified** whenever numbers exist (V01 t=06:30, V16 t=08:30).
- **Results, not process.** "When conducting analysis and interviews we learned a
  lot" says what you did, not what you found (V01 t=06:45).
- **No general truths** ("managing risk is important") and **no absolutes** (all,
  never, always, every, none): one counterexample from the room sinks the slide
  (V01 t=05:00). Restrictive words such as "only" are fine when they state a fact
  or a condition you control ("pilot in two branches only, scale on approval"),
  and not fine when they claim something about the world you cannot prove
  ("the only option").
- **Two lines at most**, telegraphic style allowed: drop articles and filler
  (V01 t=07:30, t=11:30).
- **Keep title numbers live.** When the analysis changes, the title goes stale
  first. Re-check every title number in the polishing pass (V15 t=10:45).

The full ladder from a topic label to a target title is in
`references/verbatim-assets.md`.

### 3.2 Structure: every slide is a table

Think of every page as rows and columns, not as an inserted table (V06 t=01:00).
**Different types of information go in different columns** (measure, rationale,
example, impact, timing); **the items they describe go in rows** (V06 t=02:15).

A plain list of bullets is a **clothesline**: it reads like a brainstorm dump, and
the reader cannot trust it is complete or ranked (V18 t=01:45). Fix it in this
order: cluster the bullets into two or three named groups, add separators, give the
set a header naming what the items are, then split it into columns by information
type (V18 t=02:30 to t=04:15).

Use a known blueprint rather than inventing a layout (V06 t=00:00). The four that
cover most pages, with variants, are in `references/blueprints.md`:

- **Qualitative:** columns by information type, rows by item.
- **Chart with implications:** chart left, so-what right. About half of all his
  consulting pages (V06 t=07:15).
- **Integrated:** the chart built into the table, so the reader never has to jump
  between bullets and a separate chart (V06 t=09:15).
- **Options:** one column per option, the same rows for each.

### 3.3 Data and graphics

Choose the chart from the comparison it makes, then strip it down. Details in
`references/charts.md`.

- Every chart compares something: **component** (shares of a total), **absolute**
  (sizes), **time series**, **distribution**, **correlation** (V04 t=06:30,
  V15 t=06:30).
- **Colour carries meaning or it goes.** Grey everything; put the accent colour on
  the point the title makes (V04 t=01:30, V16 t=02:00).
- **Data-to-ink:** delete gridlines, connector lines, background fills, and the
  axis when the bars carry their values (V04 t=04:00, V14 t=04:00).
- **Point the chart at the message:** a difference arrow or shading on the part
  that matters, and quote that number in the title (V04 t=03:15, V09 t=10:30).
- **Self-explanatory:** chart title, unit for every dimension, **percent of what**,
  the date or period, a legend for any coding, the source, any qualifier such as
  survey geography (V23 t=04:00 to t=08:30).

Same data, different audience, different story: highlight what *this* audience
needs to see, and title it accordingly (V09 t=04:15).

### 3.4 Supporting text

- **De-word.** Bullets, not sentences; drop articles. "The value of this
  information depends on the trust within the network" becomes "Information value
  depends on network trust" (V05 t=08:45).
- **Selective bold:** the few words in each bullet that carry it, in the deck's
  main colour (V15 t=10:00, V16 t=07:45).
- **Parallel items get identical structure.** Three programmes are each described
  with the same sub-headings, ideally named once as row labels (V10 t=07:30).
- **Repeated sets keep their order and their icons** everywhere in the deck: the
  same regions, products or channels, always in the same sequence (V02 t=22:00).
  This beats sorting by size. Sort a chart by value only when the set appears once,
  or when ranking is the message; then say so in the title.
- **Introduce terms before using them,** and say whether a number is good or bad
  (V05 t=07:45).

### 3.5 Polishing

Look and feel is judged before content is read. Run the checklist in
`references/polish-checklist.md`. The core of it:

- **Margins:** the action title's left edge and the footnote's right edge bound the
  page. Nothing crosses them (V02 t=08:45).
- **One body font size,** title and footnotes excepted. One deliberate exception
  per page at most, for a single headline number (V05 t=02:45, V02 t=10:45).
  "Body" means everything else on the page: column headers, row labels, chart
  labels and bar values, callouts and tables. Make headers stand out with bold or
  colour, not a bigger size. The linter reports two body sizes as a NOTE, because
  the second may be the allowed hero number, and three or more as an ERROR. Treat
  a NOTE as an ERROR unless the second size is that one number.
- **No jitter:** title, body and footer sit in exactly the same place on every
  page. Flip through the PDF and nothing should move (V05 t=03:45).
- **Alignment:** as few alignment lines as possible, everything snapped to them,
  groups evenly distributed (V14 t=06:30, V20 t=01:00).
- **Consistent notation:** one way to write negatives, ISO currency codes instead
  of "$", one number format (V14 t=05:30, t=06:15).
- **Nothing decorative:** no SmartArt, no 3D or glossy charts, no animations or
  transitions, no screenshots of charts (V08, V04 t=12:00, V05 t=07:30, t=11:15).

## When an AI built the deck, check what AI gets wrong

AI slide tools, Claude for PowerPoint included, fail in specific and repeatable
ways (V10 t=05:15 to t=13:15). Written feedback rarely fixed them (V10 t=08:30),
so check every generated deck mechanically and by eye:

- an accent bar or box running into the footer;
- text or bars not aligned with the title's left edge;
- bullets with no space between bullet and text;
- a template element copied without the content that justified it;
- an inverted colour hierarchy (darker colours should mark higher levels);
- parallel items described with different sub-headings;
- the title not in the template's title style, or font sizes drifting.

Run the linter on any `.pptx` before you show it, fix every ERROR and WARN, and say
what it cannot check:

```
python3 .claude/skills/slide-writer/scripts/lint_pptx.py deck.pptx
```

It needs only the Python standard library, and checks:
- 16:9 aspect ratio;
- whether titles exist and read as sentences;
- elements crossing the title's edges or running into the footer (footer
  placeholders, or text boxes in the bottom fifth that start with "Source" or
  "Note");
- body font sizes;
- text box margins and bullet indents;
- currency notation;
- SmartArt, 3D charts, large pies and animations;
- title jitter between slides.

Slide 1 is skipped only when it looks like a cover. Text inside charts (axis
labels, data labels) is not read, so check chart font sizes, units, period and
source by eye. It cannot judge the message, the chart choice or the storyline. *(The linter is not
from the videos; it automates their rules.)*

## Decision rules

- **Topic given, no message:** draft the storyline as action titles and get
  agreement before building pages (V19 t=01:00).
- **A slide with no so-what:** appendix or cut (V01 t=04:30).
- **Simple chart, general takeaways:** chart plus implications column. **Complex
  chart, or bullets that each point at one part of it:** integrate (V06 t=07:15,
  t=09:15).
- **Shares of a whole, more than about five parts:** a sorted bar chart, not a pie
  (V04 t=05:00).
- **A bridge, a P&L, a build-up to a total:** waterfall (V04 t=10:45, V19 t=06:45).
- **Three numeric dimensions:** bubble chart, every dimension labelled with its unit
  (V04 t=07:30, V16 t=01:30).
- **Legend or not:** always, unless the action title itself explains the highlight
  (V05 t=03:30, V23 t=07:30).
- **Bridge versus integrated:** when the numbers build to a total (a bridge, a
  P&L), the waterfall is the chart; if each bar also needs a comment, put the
  comments in a row aligned under the bars, which is integrating the waterfall.
- **Number circles:** only as a secondary dimension inside an integrated layout,
  never instead of a chart (V15 t=06:30, V06 t=11:00).
- **Board in the room:** basic language, larger type, detail in the appendix.
  **Sent without you:** enough text to stand alone (V21 t=11:00, V17 t=06:30).
- **Boardroom audience:** consulting style, not dense banking pages or
  football-field valuation charts (V05 t=12:15).
- **One slide, several messages:** rewrite the slide around the one message the
  title can carry, and show where each other message goes: its own page, or the
  appendix (V15 t=00:30). If the user insists on a single page, keep the main
  layout and fold the rest into one extra column such as "Implication for us",
  then write the title as the combined conclusion. Never solve it with a bullet
  block under the chart.
- **The deck asks for a decision:** end the storyline with a decision page whose
  title states the ask ("Approve AED [number needed] for a two-branch pilot from
  Q3"), with the options, cost and payback, risks and next steps as rows or
  columns. Put an investment or payback page before it when money is requested.
  *(Not from the videos.)*

## Known gotchas

- **Text boxes will not line up even with Align.** PowerPoint's default text box
  has internal margins that alignment ignores. Zero them and set as default
  (V12, V20 t=06:30).
- **Distribute stacks elements on top of each other.** Group each row first, then
  distribute the groups (V20 t=03:45).
- **Icons used alone or on every page.** Icons go only beside their label, sparingly,
  best as markers that recur through the deck (V11 t=06:45, t=08:00).
- **Ambiguous figures.** "+7% YoY, +9% FX-adjusted" without saying which one the
  bars show forces the reader to do arithmetic (V14 t=09:00).
- **Implied links.** A pie that shares a colour with an unrelated bar implies a
  relationship that is not there (V14 t=09:45).

## Output format

**Storyline or "build me a deck" requests.** One line stating the occasion and any
assumption. Then the executive summary, written as situation, complication,
solution. Then the storyline as a table:

```
| # | Action title | Blueprint | Content and chart | Data still needed |
```

Close with the open questions that would change the storyline.

**Review requests.** Lead with a one-line verdict. Then list the defects grouped as
message, structure, charts, text and polish, most damaging first. Then the rewrite:
the new action title, the new layout described column by column, and what moved to
the appendix.

**Building a file.** Build with the presentation tool, lint, fix, and report the
lint result alongside what still needs a human read.

## Outside the videos *(not from the videos; verify)*

- **Right-to-left decks (Arabic):** mirror the grid. The title's right edge becomes
  the leading boundary, and all alignment rules apply in mirror. Use one numeral
  system consistently on a page, and check the template's text direction setting.
  Do not mix left- and right-aligned body text on one page.
- **Accessibility:** a grey and accent scheme must still have enough contrast.
  Never let colour alone carry the meaning; the label or legend should too, which
  the self-explanatory rule already requires.
- **The appendix:** everything that supports but does not advance the argument:
  methodology, full data tables, text-heavy measure lists (V06 t=03:30).
- **Live delivery:** be in the room 30 minutes early for important meetings, carry
  display adapters, a clicker and spare speakerphones, and dial in before the start
  (V22, the one logistics video in the playlist).

## Worked example

Input: a logistics director wants to recommend closing two of three regional
warehouses. It is a board meeting, presented in the room and circulated afterwards.

- **Occasion:** board. Basic language, larger type, every page self-standing,
  detail in the appendix.
- **Situation:** order volumes have grown steadily for three years and the network
  has not changed.
- **Complication:** two of the three sites now run below half capacity, while
  rents rise this year. Should we keep paying for three sites?
- **Solution:** consolidate into the central site, then preview the cost case, the
  service-level risk, and the 12-month plan.
- **Titles, read alone:**
  1. "Two of three warehouses run below 50% capacity while rents rise 12% this
     year"
  2. "Consolidating into the central site saves [number needed] a year from year
     two"
  3. "Delivery times stay within the 48-hour promise for 96% of customers"
  4. "Twelve-month plan closes the northern site first, with no customer-facing
     disruption"
- **Blueprints:** page 1 is chart with implications (capacity by site, accent on
  the two). Page 2 is a waterfall from today's cost to the new cost. Page 3 is
  integrated (a coverage map, then the details and assessment columns). Page 4 is
  a qualitative timeline.

The savings figure stays `[number needed]` until the finance team supplies it.
Never invent it to make the title quantified.

## References

- `references/blueprints.md`: the layout blueprints with column and row structures.
- `references/charts.md`: chart selection, formatting, and the self-explanatory
  checklist.
- `references/polish-checklist.md`: the full pre-send checklist.
- `references/verbatim-assets.md`: the title ladder, the SCS example, the
  frameworks, word for word.
- `references/source-notes.md`: per-video notes with timestamps, and the
  cross-video merge.
- `scripts/lint_pptx.py`: the `.pptx` checker.
