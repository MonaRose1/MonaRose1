#!/usr/bin/env python3
"""Check relative Markdown links and in-page anchors. No network, no dependencies."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def anchors(path: Path) -> set:
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADING.match(line)
        if m:
            out.add(slug(m.group(2)))
    return out


def main() -> int:
    files = [ROOT / "README.md"] + sorted((ROOT / "docs").rglob("*.md"))
    problems = []
    for f in files:
        if not f.exists():
            problems.append((f, "", "missing file"))
            continue
        body = f.read_text(encoding="utf-8")
        anchors_here = anchors(f)
        for target in LINK.findall(body):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                if target.startswith("#"):
                    if target[1:] not in anchors_here:
                        problems.append((f, target, "missing anchor"))
                continue
            path_part, _, anchor = target.partition("#")
            dest = (f.parent / path_part).resolve()
            if not dest.exists():
                problems.append((f, target, "missing file"))
            elif anchor and dest.suffix == ".md":
                if anchor not in anchors(dest):
                    problems.append((f, target, "missing anchor"))
    for f, target, why in problems:
        print(f"{f.relative_to(ROOT)}: {why}: {target}")
    print(f"\nchecked {len(files)} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
