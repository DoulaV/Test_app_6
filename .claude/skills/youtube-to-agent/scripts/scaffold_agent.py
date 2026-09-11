#!/usr/bin/env python3
"""Scaffold a Claude Code skill from a youtube-to-agent spec.json.

Usage:
  python3 scaffold_agent.py <spec.json> [--dest .claude/skills] [--analysis analysis.md]
                            [--force] [--no-gitignore]

Creates <dest>/<name>/ with SKILL.md, references/source-notes.md,
references/verbatim-assets.md and evals/evals.json. Refuses to overwrite an
existing skill directory unless --force is passed.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "skill-template.md"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = ["name", "description", "capability", "procedure"]


def evidence(item):
    ev = item.get("evidence") or []
    return f" (see source-notes: {', '.join(ev)})" if ev else ""


def render_list(items, empty="- None recorded."):
    if not items:
        return empty
    return "\n".join(f"- {i}" for i in items)


def render_procedure(steps):
    if not steps:
        return "1. (no steps recorded)"
    out = []
    for n, s in enumerate(steps, 1):
        if isinstance(s, str):
            out.append(f"{n}. {s}")
            continue
        line = f"{n}. **{s.get('step', '').strip()}**"
        if s.get("why"):
            line += f" {s['why'].strip()}"
        line += evidence(s)
        out.append(line)
        for cmd in s.get("commands") or []:
            out.append(f"   ```\n   {cmd}\n   ```")
    return "\n".join(out)


def render_rules(rules):
    if not rules:
        return "- None recorded in the source. Add rules as you discover decision points."
    return "\n".join(f"- When {r.get('when', '?')}: {r.get('do', '?')}{evidence(r)}" for r in rules)


def render_gotchas(gotchas):
    if not gotchas:
        return "- None recorded."
    return "\n".join(f"- {g.get('issue', '?')} Fix: {g.get('fix', '?')}{evidence(g)}" for g in gotchas)


def render_gaps(gaps):
    if not gaps:
        return "- The video appeared to cover everything needed. Treat that with suspicion."
    return "\n".join(f"- {g} (not shown in the video)" for g in gaps)


def render_source_notes(spec, analysis_text):
    src = spec.get("source", {})
    head = [
        f"# Source notes: {src.get('title') or spec['name']}",
        "",
        f"- Source: {src.get('url_or_path', 'unknown')}",
        f"- Author: {src.get('author', 'unknown')}",
        f"- Duration: {src.get('duration', 'unknown')}",
        "",
        "Every claim below carries a timestamp so it can be verified by scrubbing to it.",
        "",
    ]
    if analysis_text:
        head += [analysis_text.strip(), ""]
    else:
        head += [
            "## Procedure evidence",
            "",
        ]
        for s in spec.get("procedure", []):
            if isinstance(s, dict):
                head.append(f"- {s.get('step', '')}: {', '.join(s.get('evidence') or ['no timestamp'])}")
        head.append("")
        head.append("(No analysis.md was supplied. Re-run scaffold_agent.py with --analysis to include the beat sheet.)")
    return "\n".join(head) + "\n"


def render_assets(spec):
    assets = spec.get("verbatim_assets") or []
    lines = ["# Verbatim assets", "", "Copied exactly from the screen. Do not paraphrase these.", ""]
    if not assets:
        lines.append("None recorded.")
    for a in assets:
        kind = a.get("kind", "asset")
        ev = ", ".join(a.get("evidence") or [])
        lines += [f"## {kind}" + (f" (t={ev})" if ev else ""), "", "```", a.get("text", "").rstrip(), "```", ""]
    return "\n".join(lines) + "\n"


def title_from(name):
    return " ".join(w.capitalize() for w in name.split("-"))


def add_gitignore(repo_root):
    gi = repo_root / ".gitignore"
    entry = ".youtube-to-agent/"
    existing = gi.read_text() if gi.is_file() else ""
    if entry in existing.splitlines():
        return False
    with gi.open("a") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(f"\n# youtube-to-agent working directories (frames, audio, transcripts)\n{entry}\n")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--dest", default=".claude/skills")
    ap.add_argument("--analysis", help="analysis.md to embed in references/source-notes.md")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-gitignore", action="store_true", help="do not add .youtube-to-agent/ to the repo .gitignore")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    missing = [k for k in REQUIRED if not spec.get(k)]
    if missing:
        sys.exit(f"spec is missing required fields: {', '.join(missing)}")
    name = spec["name"]
    if not NAME_RE.match(name):
        sys.exit(f"name must be kebab-case (lowercase letters, digits, hyphens): {name!r}")

    dest = Path(args.dest).expanduser()
    skill_dir = dest / name
    if skill_dir.exists() and not args.force:
        sys.exit(f"{skill_dir} already exists. Pass --force to overwrite it.")
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (skill_dir / "evals").mkdir(parents=True, exist_ok=True)

    src = spec.get("source", {})
    template = TEMPLATE.read_text()
    fields = {
        "name": name,
        "description": spec["description"].strip().replace("\n", " "),
        "title": spec.get("title") or title_from(name),
        "capability": spec["capability"].strip(),
        "source_title": src.get("title") or "source video",
        "source_ref": src.get("url_or_path") or "unknown source",
        "prerequisites": render_list(spec.get("prerequisites"), "- None beyond a working Claude Code session."),
        "procedure": render_procedure(spec.get("procedure")),
        "decision_rules": render_rules(spec.get("decision_rules")),
        "gotchas": render_gotchas(spec.get("gotchas")),
        "gaps": render_gaps(spec.get("gaps")),
    }
    body = template
    for k, v in fields.items():
        body = body.replace("{{" + k + "}}", v)
    (skill_dir / "SKILL.md").write_text(body)

    analysis_text = Path(args.analysis).read_text() if args.analysis else ""
    (skill_dir / "references" / "source-notes.md").write_text(render_source_notes(spec, analysis_text))
    (skill_dir / "references" / "verbatim-assets.md").write_text(render_assets(spec))

    evals = {
        "skill_name": name,
        "evals": [
            {"id": i, "prompt": p, "expected_output": "Completes the task following the procedure in SKILL.md.", "files": []}
            for i, p in enumerate(spec.get("test_prompts") or [], 1)
        ],
    }
    (skill_dir / "evals" / "evals.json").write_text(json.dumps(evals, indent=2) + "\n")

    if not args.no_gitignore:
        # Walk up from dest to find the repo root (a directory containing .git).
        for parent in [dest.resolve(), *dest.resolve().parents]:
            if (parent / ".git").exists():
                if add_gitignore(parent):
                    print(f"Added .youtube-to-agent/ to {parent / '.gitignore'}")
                break

    print(f"Scaffolded {skill_dir}")
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(skill_dir)}")
    print("Next: edit SKILL.md by hand (add the why behind each step, fill the gaps), then run the evals.")


if __name__ == "__main__":
    main()
