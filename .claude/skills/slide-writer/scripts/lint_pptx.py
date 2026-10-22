#!/usr/bin/env python3
"""Check a .pptx against the slide-writer rules. Standard library only.

Usage:
  python3 lint_pptx.py deck.pptx [--json] [--strict]

A .pptx is a zip of XML parts, so this reads them directly instead of depending
on python-pptx. It checks the things that can be checked mechanically, which are
exactly the things AI-built slides get wrong (see SKILL.md, "When an AI built
the deck"):

  deck     16:9 aspect ratio; title position identical on every content slide
  titles   present, a sentence rather than a topic label, under about two lines,
           no absolute words
  layout   nothing left of the title's left edge or right of its right edge,
           nothing running into the footer, nothing off the slide
  text     at most one body font size (a second one is flagged as a deliberate
           exception to confirm), text boxes with zero internal margins,
           bullets with a hanging indent, ISO currency codes instead of "$"
  objects  no SmartArt, no 3D charts, pie charts of five slices or fewer,
           no animations or transitions
  charts   gridlines noted for removal

It cannot judge content: whether the title is the right message, whether the
chart type fits the comparison, whether the storyline holds. Those stay manual.

Exit status is 1 when any ERROR is found (or any WARN with --strict), else 0.
"""
import argparse
import json
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
R_ID = "{%s}id" % NS["r"]
EMU_PER_INCH = 914400
TOL = int(0.04 * EMU_PER_INCH)          # alignment tolerance, about 1 mm
DEFAULT_INSET = 91440                    # PowerPoint's default text box margin, 0.1 inch
TITLE_TYPES = {"title", "ctrTitle"}
FOOTER_TYPES = {"ftr", "sldNum", "dt"}
SKIP_TITLE_WORDS = re.compile(r"^(agenda|contents?|table of contents|appendix|back-?up|"
                              r"thank you|thanks|questions|q&a|contact|next steps)\b", re.I)
ABSOLUTE = re.compile(r"\b(all|always|never|every|none|nobody|everyone|everything)\b", re.I)
DOLLAR = re.compile(r"(?<![A-Z])\$\s?\d|\d\s?\$(?!\w)")
THREE_D = ("bar3DChart", "line3DChart", "pie3DChart", "area3DChart",
           "surfaceChart", "surface3DChart")


def q(tag):
    pre, name = tag.split(":")
    return "{%s}%s" % (NS[pre], name)


class Deck:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.names = set(self.z.namelist())
        self._xml = {}

    def xml(self, part):
        if part not in self._xml:
            self._xml[part] = ET.fromstring(self.z.read(part)) if part in self.names else None
        return self._xml[part]

    def rels(self, part):
        d, f = posixpath.split(part)
        rp = posixpath.join(d, "_rels", f + ".rels")
        root = self.xml(rp)
        out = {}
        if root is None:
            return out
        for rel in root.findall("rel:Relationship", NS):
            target = rel.get("Target")
            if rel.get("TargetMode") == "External":
                continue
            out[rel.get("Id")] = (rel.get("Type", "").rsplit("/", 1)[-1],
                                  posixpath.normpath(posixpath.join(d, target)))
        return out

    def rel_of_type(self, part, kind):
        return next((t for k, t in self.rels(part).values() if k == kind), None)

    def slides(self):
        pres = self.xml("ppt/presentation.xml")
        rels = self.rels("ppt/presentation.xml")
        for sid in pres.find("p:sldIdLst", NS) or []:
            yield rels[sid.get(R_ID)][1]

    def size(self):
        s = self.xml("ppt/presentation.xml").find("p:sldSz", NS)
        return int(s.get("cx")), int(s.get("cy"))


def ph_info(sp):
    ph = sp.find("./*/p:nvPr/p:ph", NS)
    if ph is None:
        return None
    return ph.get("type", "body"), ph.get("idx")


def partial_xfrm(el):
    """(x, y, cx, cy) with None for any part the element does not set itself.
    Generators such as python-pptx often write only <a:off> when they move a
    placeholder, leaving the size to the layout, so a partial result is common."""
    x = el.find("./p:spPr/a:xfrm", NS)
    if x is None:
        x = el.find("./p:xfrm", NS)            # graphicFrame
    if x is None:
        x = el.find("./p:grpSpPr/a:xfrm", NS)  # group
    if x is None:
        return (None, None, None, None)
    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
    xy = (int(off.get("x")), int(off.get("y"))) if off is not None else (None, None)
    wh = (int(ext.get("cx")), int(ext.get("cy"))) if ext is not None else (None, None)
    return xy + wh


def xfrm_of(el):
    box = partial_xfrm(el)
    return box if None not in box else None


def resolve_box(deck, slide_part, el, ph):
    """The element's own geometry, completed from its layout or master where it is silent."""
    own = partial_xfrm(el)
    if None not in own:
        return own
    inherited = inherited_xfrm(deck, slide_part, ph) if ph else None
    if inherited is None:
        return None
    return tuple(o if o is not None else i for o, i in zip(own, inherited))


def inherited_xfrm(deck, slide_part, ph):
    """Resolve a placeholder's position from its layout, then its master."""
    ptype, idx = ph
    layout = deck.rel_of_type(slide_part, "slideLayout")
    chain = [layout, deck.rel_of_type(layout, "slideMaster") if layout else None]
    for part in chain:
        root = deck.xml(part) if part else None
        if root is None:
            continue
        for sp in root.iter(q("p:sp")):
            info = ph_info(sp)
            if not info:
                continue
            same = (idx is not None and info[1] == idx) or info[0] == ptype or (
                ptype in TITLE_TYPES and info[0] in TITLE_TYPES)
            if same and xfrm_of(sp):
                return xfrm_of(sp)
    return None


def text_of(el):
    return " ".join(t.text or "" for t in el.iter(q("a:t"))).strip()


def lint(path):
    deck = Deck(path)
    W, H = deck.size()
    findings = []
    ratio = W / H

    def add(slide, sev, msg, title=""):
        findings.append({"slide": slide, "severity": sev, "title": title, "message": msg})

    if abs(ratio - 4 / 3) < 0.02:
        add(0, "ERROR", "Slides are 4:3. Use 16:9 for more space and no black bars (V14 t=03:00).")
    elif abs(ratio - 16 / 9) > 0.02:
        add(0, "NOTE", f"Unusual aspect ratio {ratio:.2f}; 16:9 is the standard.")

    title_positions = {}
    slide_parts = list(deck.slides())
    for n, part in enumerate(slide_parts, 1):
        root = deck.xml(part)
        tree = root.find("p:cSld/p:spTree", NS)
        title_text, title_box, footer_top = "", None, None
        shapes = []
        for el in tree:
            tag = el.tag.split("}")[1]
            if tag not in ("sp", "pic", "graphicFrame", "grpSp", "cxnSp"):
                continue
            ph = ph_info(el)
            box = resolve_box(deck, part, el, ph)
            shapes.append((el, tag, ph, box))
            if ph and ph[0] in TITLE_TYPES:
                title_text, title_box = text_of(el), box
            if ph and ph[0] in FOOTER_TYPES and box and text_of(el):
                footer_top = box[1] if footer_top is None else min(footer_top, box[1])

        label = (title_text[:60] + "...") if len(title_text) > 60 else title_text
        is_cover = n == 1
        skip_title = is_cover or bool(SKIP_TITLE_WORDS.match(title_text))

        # Titles (V01)
        if not is_cover:
            words = title_text.split()
            if not title_text:
                add(n, "WARN", "No title. Every content slide needs an action title (V01 t=00:00).")
            elif not skip_title:
                if len(words) < 5:
                    add(n, "WARN", f"Title has {len(words)} words; it reads like a topic label, not "
                                   "an action title. Write the conclusion as a sentence (V01 t=09:00).", label)
                if len(title_text) > 110:
                    add(n, "WARN", f"Title is {len(title_text)} characters, likely more than two lines "
                                   "(V01 t=07:30).", label)
                m = ABSOLUTE.search(title_text)
                if m:
                    add(n, "NOTE", f"Absolute word '{m.group(0)}' in the title; one counterexample sinks it "
                                   "(V01 t=05:30).", label)
            if title_box and not skip_title:
                title_positions[n] = title_box

        # Layout boundaries (V02 t=08:45, V14 t=06:30, V10 t=05:15)
        left = title_box[0] if title_box else None
        right = title_box[0] + title_box[2] if title_box else None
        for el, tag, ph, box in shapes:
            if box is None:
                continue
            x, y, cx, cy = box
            name = (el.find("./*/p:cNvPr", NS).get("name") if el.find("./*/p:cNvPr", NS) is not None
                    else tag)
            if x < -TOL or y < -TOL or x + cx > W + TOL or y + cy > H + TOL:
                add(n, "WARN", f"'{name}' extends off the slide (V15 t=11:45).", label)
                continue
            full_bleed = cx >= 0.95 * W
            if is_cover or full_bleed or (ph and (ph[0] in TITLE_TYPES or ph[0] in FOOTER_TYPES)):
                continue
            if left is not None and x < left - TOL:
                add(n, "WARN", f"'{name}' starts {(left - x) / EMU_PER_INCH:.2f} in left of the action "
                               "title's left edge, the page boundary (V02 t=08:45, V10 t=05:30).", label)
            if right is not None and x + cx > right + TOL:
                add(n, "WARN", f"'{name}' ends {(x + cx - right) / EMU_PER_INCH:.2f} in right of the title's "
                               "right edge (V02 t=08:45).", label)
            if footer_top is not None and y + cy > footer_top + TOL:
                add(n, "WARN", f"'{name}' runs into the footer area (V10 t=05:30).", label)

        # Text: font sizes, insets, bullets, currency (V02 t=08:00, V05 t=02:45, V20 t=06:30, V14 t=06:15)
        body_sizes = set()
        for sp in root.iter(q("p:sp")):
            ph = ph_info(sp)
            box = resolve_box(deck, part, sp, ph)
            txt = sp.find("p:txBody", NS)
            if txt is None or not text_of(sp):
                continue
            nm = sp.find("./p:nvSpPr/p:cNvPr", NS).get("name", "shape")
            is_title = ph is not None and ph[0] in TITLE_TYPES
            is_footer = (ph is not None and ph[0] in FOOTER_TYPES) or (box is not None and box[1] > 0.85 * H)
            if not (is_title or is_footer or is_cover):
                for rpr in sp.iter(q("a:rPr")):
                    if rpr.get("sz"):
                        body_sizes.add(int(rpr.get("sz")) / 100)
            cnv = sp.find("./p:nvSpPr/p:cNvSpPr", NS)
            if cnv is not None and cnv.get("txBox") == "1":
                bp = txt.find("a:bodyPr", NS)
                l = int(bp.get("lIns", DEFAULT_INSET)) if bp is not None else DEFAULT_INSET
                r = int(bp.get("rIns", DEFAULT_INSET)) if bp is not None else DEFAULT_INSET
                if l > 0 or r > 0:
                    add(n, "WARN", f"Text box '{nm}' has internal margins ({l / EMU_PER_INCH:.2f} in / "
                                   f"{r / EMU_PER_INCH:.2f} in), so its text will not line up with other "
                                   "elements. Set them to zero (V20 t=06:30).", label)
            for para in txt.findall("a:p", NS):
                ppr = para.find("a:pPr", NS)
                if ppr is not None and (ppr.find("a:buChar", NS) is not None or
                                        ppr.find("a:buAutoNum", NS) is not None):
                    if int(ppr.get("marL", "0")) == 0 or int(ppr.get("indent", "0")) >= 0:
                        add(n, "WARN", f"Bullets in '{nm}' have no hanging indent, so text sits against the "
                                       "bullet (V10 t=05:30).", label)
                        break
            if DOLLAR.search(text_of(sp)):
                add(n, "NOTE", f"'$' in '{nm}'. Use a three-letter currency code (USD, AED, EUR) "
                               "(V14 t=06:15).", label)
        if len(body_sizes) >= 3:
            add(n, "ERROR", f"{len(body_sizes)} body font sizes ({', '.join(f'{s:g}' for s in sorted(body_sizes))} pt). "
                            "One size for the whole body (V05 t=02:45).", label)
        elif len(body_sizes) == 2:
            add(n, "NOTE", f"Two body font sizes ({', '.join(f'{s:g}' for s in sorted(body_sizes))} pt). "
                           "Fine only if the second is one deliberate hero number (V02 t=10:45).", label)

        # Objects: SmartArt, charts, animation
        for gf in root.iter(q("p:graphicFrame")):
            gd = gf.find(".//a:graphicData", NS)
            uri = gd.get("uri", "") if gd is not None else ""
            if "diagram" in uri:
                add(n, "ERROR", "SmartArt found. Rebuild it from basic shapes (V08 t=03:00).", label)
            if uri.endswith("/chart"):
                ref = gd.find("c:chart", NS)
                target = deck.rels(part).get(ref.get(R_ID), (None, None))[1] if ref is not None else None
                croot = deck.xml(target) if target else None
                if croot is None:
                    continue
                for kind in THREE_D:
                    if croot.find(".//c:" + kind, NS) is not None or croot.find(".//c:view3D", NS) is not None:
                        add(n, "ERROR", "3D chart. Use a flat chart (V04 t=12:00).", label)
                        break
                for pie in list(croot.iter(q("c:pieChart"))) + list(croot.iter(q("c:doughnutChart"))):
                    pts = pie.find(".//c:val//c:ptCount", NS)
                    if pts is not None and int(pts.get("val", "0")) > 5:
                        add(n, "WARN", f"Pie or doughnut with {pts.get('val')} slices. Over about five, "
                                       "use a sorted bar chart (V04 t=05:00).", label)
                if croot.find(".//c:majorGridlines", NS) is not None:
                    add(n, "NOTE", "Chart has gridlines. Remove them unless they carry information "
                                   "(data-to-ink, V04 t=04:00).", label)
        timing = root.find("p:timing", NS)
        if timing is not None and timing.find(".//p:par", NS) is not None:
            add(n, "WARN", "Animations present. Consulting decks have none (V05 t=11:15).", label)
        if root.find("p:transition", NS) is not None:
            add(n, "NOTE", "Slide transition set. Remove it (V15 t=11:45).", label)

    # Jitter: the title must sit in the same place on every content slide (V05 t=03:45)
    if len(title_positions) >= 2:
        positions = list(title_positions.values())
        ref = max(set(positions), key=positions.count)
        for n, box in title_positions.items():
            if any(abs(a - b) > TOL for a, b in zip(box, ref)):
                add(n, "WARN", "Title position differs from the other slides, so it jitters when paging "
                               "through (V05 t=03:45).")

    return {"file": path, "slides": len(slide_parts), "aspect": f"{ratio:.2f}", "findings": findings}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    args = ap.parse_args()
    try:
        res = lint(args.pptx)
    except FileNotFoundError:
        sys.exit(f"No such file: {args.pptx}")
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
        sys.exit(f"Not a readable .pptx: {e}")
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"{res['file']}: {res['slides']} slides, aspect {res['aspect']}")
        last = None
        for f in sorted(res["findings"], key=lambda f: (f["slide"], f["severity"] != "ERROR")):
            if f["slide"] != last:
                head = "Deck" if f["slide"] == 0 else f"Slide {f['slide']}"
                print(f"\n{head}" + (f'  "{f["title"]}"' if f["title"] else ""))
                last = f["slide"]
            print(f"  {f['severity']:<5}  {f['message']}")
        counts = {s: sum(1 for f in res["findings"] if f["severity"] == s) for s in ("ERROR", "WARN", "NOTE")}
        print(f"\n{counts['ERROR']} errors, {counts['WARN']} warnings, {counts['NOTE']} notes. "
              "Content (the message, the chart choice, the storyline) still needs a human read.")
    bad = any(f["severity"] == "ERROR" or (args.strict and f["severity"] == "WARN") for f in res["findings"])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
