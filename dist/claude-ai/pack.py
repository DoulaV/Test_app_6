import re, shutil, yaml, zipfile
from pathlib import Path

SHORT = {
 "brand-architect": "Define and audit a personal brand: associations kept and refused, positioning, brand story, core topic, off-band budget, and what to sell first. Use for positioning, collabs and monetising.",
 "algorithm-strategist": "Plan and audit content strategy with the sampling model: one avatar, a narrow topic band, the four engagement attributes, flop diagnosis, comment stances. Use for low reach and what to post next.",
 "brand-idea-miner": "Mine validated video ideas from outliers in your niche and shape them with the five obsession elements. Use for reel ideas, competitor research, remixes, or auditing an idea before you make it.",
 "hook-writer": "Write, rewrite and grade scroll-stopping hooks using the three-step formula: context lean, scroll stop, contrarian snapback, plus on-screen text and speed to value. Use for intros and openings.",
 "story-loop-writer": "Structure and audit story and script bodies with the four-step addiction loop: stakes, big question, head fake, re-hook. Use when content is flat, loses people mid-way, or needs retention.",
 "copy-sharpener": "Research your audience's own words, then make any copy clear, concise, concrete, conversational and rhythmic. Use for captions, bios, ads, emails, landing pages, headlines and calls to action.",
 "higgsfield": "Write production-ready Higgsfield AI video and image prompts: model choice (Kling, Veo, Seedance, Soul), camera and motion presets, Soul ID consistency, Cinema Studio, troubleshooting.",
 "humanizer": "Rewrite AI-sounding text so it reads like the writer, without changing what it says. English and Egyptian Arabic, separate pattern sets. Removes AI tells; restores Masri grammar and particles.",
 "satori": "Wisdom companion for your own inner life: grief, meaning, hard personal questions. Also explains a character's psychology on request. Not for writing content or brand decisions.",
 "youtube-to-agent": "Turn any YouTube tutorial or shared video into a working skill: ingest, beat sheet, spec, scaffold, fill the gaps, test. Use when someone shares a video and wants Claude to learn from it.",
}

src_root = Path(".claude/skills")
out = Path("dist/claude-ai")
build = Path("/tmp/claude-0/build")
if build.exists(): shutil.rmtree(build)
out.mkdir(parents=True, exist_ok=True)

def split_frontmatter(text):
    """Return (list of (key, value) pairs, body). Handles | and > block scalars."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm, body = m.group(1), text[m.end():]
    pairs, nested, lines, i = [], set(), fm.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^(\S[^:]*):\s?(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2)
        i += 1
        if val.strip() in ("|", ">", "|-", ">-"):
            chunk = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                chunk.append(lines[i].strip())
                i += 1
            val = " ".join(c for c in chunk if c)
        elif val == "":
            # nested mapping (e.g. metadata:); keep its lines verbatim
            chunk = [line]
            while i < len(lines) and lines[i].startswith((" ", "\t")):
                chunk.append(lines[i])
                i += 1
            nested.add(key)
            pairs.append((key, "\n".join(chunk[1:])))
            continue
        pairs.append((key, val))
    return pairs, nested, body



TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".html"}
NESTED_NAME = "SUBSKILL.md"


def flatten_nested_skills(dst):
    """claude.ai accepts exactly one SKILL.md per zip. A multi-skill package keeps
    one SKILL.md per sub-skill folder, so rename the nested ones and rewrite every
    path that points at them. Returns the number of files renamed."""
    nested = [f for f in dst.rglob("*")
              if f.is_file() and f.name.lower() == "skill.md" and f.parent != dst]
    if not nested:
        return 0
    dirs = sorted({f.parent.name for f in nested}, key=len, reverse=True)
    pattern = re.compile(r"(?<![A-Za-z0-9_-])(" + "|".join(map(re.escape, dirs)) + r")/SKILL\.md")
    for f in nested:
        f.rename(f.with_name(NESTED_NAME))
    for f in dst.rglob("*"):
        if f.is_file() and f.suffix in TEXT_SUFFIXES:
            t = f.read_text(encoding="utf-8")
            new = pattern.sub(lambda m: f"{m.group(1)}/{NESTED_NAME}", t)
            if new != t:
                f.write_text(new, encoding="utf-8")
    return len(nested)

for name, short in SHORT.items():
    assert len(short) <= 200, (name, len(short))
    src = src_root / name
    dst = build / name
    shutil.copytree(src, dst)
    renamed = flatten_nested_skills(dst)
    p = dst / "SKILL.md"
    pairs, nested, body = split_frontmatter(p.read_text())
    d = dict(pairs)
    long_desc = d.get("description", "")
    # keep every other key (license, metadata, ...) so vendored skills stay attributed
    extra = [f"{k}:\n{v}" if k in nested else f"{k}: {v}"
             for k, v in pairs if k not in ("name", "description")]
    # block scalar: a plain description containing ": " is not valid YAML
    fm = "\n".join([f"name: {name}", "description: |", f"  {short}", *extra])
    h1 = re.match(r"\n*(# .*\n)", body)
    body = body[:h1.end()] + f"\n## When to use this\n\n{long_desc}\n" + body[h1.end():]
    if renamed:
        note = (f"\n> **Packaging note.** claude.ai allows one `SKILL.md` per upload, so in this "
                f"package each sub-skill's main file is named `{NESTED_NAME}`. Upstream calls it "
                f"`SKILL.md`. Wherever a file here refers to a sub-skill's `SKILL.md`, open that "
                f"sub-skill's `{NESTED_NAME}`. Plain `SKILL.md` on its own means this file.\n")
        body = body[:h1.end()] + note + body[h1.end():]
    p.write_text(f"---\n{fm}\n---\n{body}")
    check = yaml.safe_load(fm)          # must be valid YAML for the uploader
    assert check["name"] == name and len(check["description"]) <= 200
    skill_mds = [f for f in dst.rglob("*") if f.is_file() and f.name.lower() == "skill.md"]
    assert skill_mds == [dst / "SKILL.md"], f"{name}: claude.ai needs exactly one SKILL.md, found {len(skill_mds)}"
    z = out / f"{name}.zip"
    if z.exists(): z.unlink()
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(dst.rglob("*")):
            if f.is_file():
                # fixed timestamp so an unchanged skill rebuilds to identical bytes
                info = zipfile.ZipInfo(str(f.relative_to(build)), date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, f.read_bytes())
    extra_note = f"  ({renamed} sub-skills renamed to {NESTED_NAME})" if renamed else ""
    print(f"{name:22} desc={len(short):3}  {z.stat().st_size//1024} KB{extra_note}")
