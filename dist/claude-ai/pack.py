import re, shutil, zipfile
from pathlib import Path

SHORT = {
 "brand-architect": "Define and audit a personal brand: the associations you keep and the ones you refuse, positioning, brand story, core topic, and the 80/20 off-band budget. Use for positioning and collab calls.",
 "algorithm-strategist": "Plan and audit content strategy with the sampling model: one avatar, a narrow topic band, the four engagement attributes, flop diagnosis, comment stances. Use for low reach and what to post next.",
 "brand-idea-miner": "Mine validated video ideas from outliers in your niche and shape them with the five obsession elements. Use for reel ideas, competitor research, remixes, or auditing an idea before you make it.",
 "hook-writer": "Write, rewrite and grade scroll-stopping hooks using the three-step formula: context lean, scroll stop, contrarian snapback, plus on-screen text and speed to value. Use for intros and openings.",
 "story-loop-writer": "Structure and audit story and script bodies with the four-step addiction loop: stakes, big question, head fake, re-hook. Use when content is flat, loses people mid-way, or needs retention.",
 "copy-sharpener": "Research your audience's own words, then make any copy clear, concise, concrete, conversational and rhythmic. Use for captions, bios, ads, emails, landing pages, headlines and calls to action.",
 "youtube-to-agent": "Turn any YouTube tutorial or shared video into a working skill: ingest, beat sheet, spec, scaffold, fill the gaps, test. Use when someone shares a video and wants Claude to learn from it.",
}

src_root = Path(".claude/skills")
out = Path("dist/claude-ai")
build = Path("/tmp/claude-0/build")
if build.exists(): shutil.rmtree(build)
out.mkdir(parents=True, exist_ok=True)

for name, short in SHORT.items():
    assert len(short) <= 200, (name, len(short))
    src = src_root / name
    dst = build / name
    shutil.copytree(src, dst)
    p = dst / "SKILL.md"
    s = p.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    fm, body = m.group(1), s[m.end():]
    long_desc = re.search(r"^description: (.*)$", fm, re.M).group(1)
    new_fm = f"name: {name}\ndescription: {short}"
    # keep the full trigger text where the model will still read it
    h1 = re.match(r"\n*(# .*\n)", body)
    insert = f"\n## When to use this\n\n{long_desc}\n"
    body = body[:h1.end()] + insert + body[h1.end():]
    p.write_text(f"---\n{new_fm}\n---\n{body}")
    z = out / f"{name}.zip"
    if z.exists(): z.unlink()
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(dst.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(build))
    print(f"{name:22} desc={len(short):3}  {z.stat().st_size//1024} KB")
