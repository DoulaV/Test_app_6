# Charts

## 1. Choose by the comparison

Every chart compares something (V15 t=06:30). Name the comparison, then pick the type
(V04 t=06:30):

| Comparison | Use | Avoid |
|---|---|---|
| Components, shares of a total | Sorted bar; stacked column; a pie only at five slices or fewer | Pies with many slices, because people read areas badly (V04 t=05:00) |
| Absolute sizes | Bar or column; waterfall for a build-up or a bridge | |
| A P&L, a bridge, a sum of parts | Waterfall with totals and subtotals; stacked segments inside a bar (V04 t=10:45) | |
| Time series | Line (many points, several series), column (few points) | A 100% stacked column for shares over time; use lines (V09 t=03:30) |
| Distribution | Histogram, column by bucket | |
| Correlation | Scatter; bubble when there is a third dimension (V04 t=07:30) | |

Never use PowerPoint's chart templates with gloss, shadows, 3D or shaded backgrounds,
and never a surface chart (V04 t=12:00). Never paste a screenshot of a chart;
rebuild it from the numbers (V05 t=07:30). Banking's football-field valuation charts
confuse non-bankers (V05 t=13:00).

## 2. Strip it to the data

- **Data-to-ink:** as much data as possible with as little ink as possible
  (V04 t=04:00).
- Delete connector lines between bars, background gridlines, and the y-axis when the
  values sit on the bars (V04 t=02:30).
- Label every bar, not only the first and last; otherwise the reader needs a ruler
  (V14 t=04:30).
- Lighten a heavy black x-axis (V04 t=03:00).
- No background fill inside the chart: it wastes ink and can hide the bars on a
  black-and-white print (V14 t=05:00).
- Round long numbers into millions or thousands (V04 t=11:30, V09 t=09:30).
- Dotted lines should be light and recede, never the heaviest line on the chart
  (V05 t=03:00).

## 3. Point it at the message

- **Colour:** grey everything, then put the accent colour only on what the title is
  about: the latest year, the two regions, the one browser (V04 t=02:00, V09
  t=04:30, V16 t=02:45).
- **Difference arrow:** show the change the title claims (+400% from 2015 to 2021),
  and quote that number in the title (V04 t=03:15).
- **Shading** on the segment that matters (V09 t=12:00).
- **One message per slide:** several charts on one page only when all of them are
  needed for that one message (V04 t=13:15).
- **Same data, different audience, different emphasis:** Chrome's rise for one
  audience, Safari's resilience for another (V09 t=04:15).
- Re-aggregate data into the segmentation the rest of the deck uses (V09 t=13:00).

## 4. Make it self-explanatory

Pull the page out of the deck: a stranger a year from now must still understand it
(V23 t=01:00). Every chart carries:

- [ ] **Chart title:** what am I looking at ("Key metrics for geographical business
      units") (V16 t=05:15, V23 t=04:00)
- [ ] **Unit for every dimension:** on a bubble chart that means x, y and bubble size
      (V23 t=04:15)
- [ ] **Percent of what:** margin as % of revenue; CAGR of revenue or of profit;
      market share by units or by value (V23 t=05:00, V05 t=06:00)
- [ ] **Date or period** of the data (V23 t=06:00)
- [ ] **Legend** for any colour or size coding, unless the title explains the
      highlight (V23 t=07:00)
- [ ] **Source**, internal ones too ("Management Accounting"), because departments
      disagree (V23 t=07:45)
- [ ] **Qualifiers:** survey geography; FX-adjusted or not; trailing or calendar
      (V23 t=08:30, V14 t=09:00)
- [ ] **Consistent notation:** negatives one way; ISO currency codes, not "$"
      (V14 t=05:30, t=06:15)

## 5. Tools

think-cell is the de facto consulting standard for charts in PowerPoint, and most of
the playlist's charts were made with it (V04 t=08:30). It is not required:
PowerPoint's native charts and python-pptx charts can follow every rule above once
the defaults are stripped. *(The python-pptx point is not from the videos.)*
