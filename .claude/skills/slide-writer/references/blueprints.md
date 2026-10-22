# Layout blueprints

Every slide is a table: types of information in columns, the items they describe in
rows (V06 t=01:00). These are the blueprints the playlist uses. Each starts from the
same page frame.

## The page frame (every slide)

- **Action title** at the top, at most two lines. Its left edge is the page's left
  boundary (V02 t=08:45).
- **Footnote and source** at the bottom. Its right edge is the page's right boundary.
- **Column headers**: a short text element with a thin line under it, grouped
  together, in bold black (V02 t=05:30, t=10:00).
- **Body** in one font size. Emphasis inside it in bold, in the deck's main colour
  (V02 t=10:00).
- **Separators**: light grey dashed lines between rows, and a heavier solid line
  between major sections (V02 t=12:30).
- 16:9 (V14 t=03:00).

## 1. Qualitative: columns by information type, rows by item

```
| [Item]        | [Detail]            | [Impact]   | [Timing]   |
|---------------|---------------------|------------|------------|
| Measure A     | what it involves    | EUR 12m    | Q1 to Q2   |
| Measure B     | ...                 | ...        | ...        |
```

- The commonest error is one bullet list mixing a principle, an example and a
  suggestion. Separate them into columns (V06 t=02:15).
- Variants: Measures | Rationale (V06 t=03:30); Recommendation | Details | EBIT
  impact | Roadmap (V06 t=04:00); Measure | Description | Example (V18 t=04:15).
- The column headers can instead be timeline phases or process chevrons
  (V06 t=04:45). Build chevrons from basic shapes, never SmartArt (V08 t=11:45).
- Text-heavy versions belong in the appendix (V06 t=03:30).

## 2. Chart with implications ("the mother of all quantitative layouts")

```
| [Methodology] (optional) | [Chart]                     | [Implications]       |
|--------------------------|-----------------------------|----------------------|
| how it was measured      | the visual                  | 3 to 4 so-what bullets |
```

- About half of all his consulting pages followed a version of this (V06 t=07:15).
- Usually drop the methodology column and give the chart the space (V06 t=07:45).
- If the chart explains itself, drop the implications column and add a callout:
  a text box with two short lines pointing at the element (V06 t=08:45).
- The implications must connect to each other, not be random points (V09 t=10:45).

## 3. Integrated: the chart inside the table

```
| [Label]   | [Chart, one bar per row] | [Details]       | [Assessment]    |
|-----------|--------------------------|-----------------|-----------------|
| Region A  | ██████████               | what drives it  | invest          |
| Region B  | ████                     | ...             | hold            |
```

- Use it when the chart is complex, or when each bullet refers to a specific part
  of it. A separate bullet column forces the reader to jump back and forth and costs
  cognitive effort (V06 t=09:15).
- A callout is simply another column (V06 t=10:30).
- Shade the part of the chart that the right-hand column discusses (V06 t=11:00).
- A secondary number dimension can sit as circles in its own column (V06 t=11:00).

## 4. Options: one column per option, identical rows

```
|            | Option 1   | Option 2      | Option 3     |
|------------|------------|---------------|--------------|
| [Row A]    | ...        | ...           | ...          |
| [Row B]    | ...        | ...           | ...          |
| Common     | <---- same for all three, one arrow across ---->   |
| Cost       | EUR ...    | EUR ...       | EUR ...      |
```

- Rows are the same comparison dimensions for every option, so the options are
  actually comparable (V02 t=20:00, V10 t=07:30).
- Something shared by all options spans all columns with an arrow (V02 t=23:00).
- Commercials or cost go in the last row (V02 t=24:30).

## 5. Grids and introductions

- An image grid (for example 12 thumbnails as 3 rows by 4 columns), aligned to the
  page boundaries, each with a thin border (V02 t=16:30).
- An introduction page as two columns, such as audience on the left and the
  presenter on the right, each its own small table (V02 t=05:30).

## Building any of these in PowerPoint

- Build one row, group it (Ctrl+G), duplicate it (Ctrl+Shift+drag keeps the axis
  locked), then align and distribute the groups (V02 t=07:00, V20 t=03:45).
- Give repeated elements identical widths (V02 t=07:45).
- Zero the text box margins first, or none of the alignment will hold (V12, V20
  t=06:30).
