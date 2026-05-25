#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TEXT_EXTENSIONS = {".md", ".py", ".ts", ".tsx", ".json", ".yml", ".yaml", ".css"}
IGNORED_PARTS = {"node_modules", "build", ".docusaurus", ".git", ".venv", ".pytest_cache"}
REQUIRED_AGENT_SECTIONS = [
    "## 1. Project overview",
    "## 2. Repository map",
    "## 3. Curriculum-wide content standard",
    "## 4. Pedagogical writing style",
    "## 5. Math, diagrams, and examples",
    "## 6. Source material and attribution policy",
    "## 7. Public privacy and safety constraints",
    "## 8. Commands and verification",
    "## 9. Completion checklist",
    "## 10. Repo specialization: Simultaneous Translation Edu",
    "## 11. Maintenance notes for future agents",
]


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in TEXT_EXTENSIONS:
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_readme_empty(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if readme.exists() and readme.read_text(encoding="utf-8") != "":
        errors.append("README.md must stay empty")


def check_privacy_controls(errors: list[str]) -> None:
    robots = ROOT / "static" / "robots.txt"
    if not robots.exists():
        errors.append("static/robots.txt is missing")
    elif read(robots).strip() != "User-agent: *\nDisallow: /":
        errors.append("static/robots.txt must disallow all crawling")
    config = read(ROOT / "docusaurus.config.ts")
    if "noindex,nofollow,noarchive,nosnippet" not in config:
        errors.append("docusaurus.config.ts is missing noindex robots metadata")
    if "sitemap: false" not in config:
        errors.append("docusaurus.config.ts must disable sitemap generation")


def check_source_hygiene(errors: list[str]) -> None:
    for path in iter_text_files():
        rel = path.relative_to(ROOT)
        text = read(path)
        if "\u2014" in text:
            errors.append(f"em dash found in {rel}")
        local_path_patterns = ("/" + "Users" + "/" + "admin", "TuanDung" + "/" + "repos")
        if any(pattern in text for pattern in local_path_patterns):
            errors.append(f"local absolute path found in {rel}")
        if path.is_relative_to(DOCS) and re.search(
            r"private user instructions|hidden constraints|agent memory contents|internal planning files",
            text,
            re.I,
        ):
            errors.append(f"public/internal wording found in {rel}")


def check_agent_guide(errors: list[str]) -> None:
    agent = ROOT / "AGENT.md"
    if not agent.exists():
        errors.append("AGENT.md is missing")
        return
    text = read(agent)
    for section in REQUIRED_AGENT_SECTIONS:
        if section not in text:
            errors.append(f"AGENT.md missing required section: {section}")
    required_phrases = [
        "simultaneous text-to-text translation",
        "READ/WRITE control",
        "noindex,nofollow,noarchive,nosnippet",
        "npm run verify",
        "A better offline model does not remove the need for a timing policy",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"AGENT.md missing required guidance phrase: {phrase}")


def check_sidebar_doc_ids(errors: list[str]) -> None:
    sidebars = read(ROOT / "sidebars.ts")
    ids: list[str] = []
    for block in re.findall(r"items:\s*\[(.*?)\]", sidebars, re.S):
        ids.extend(re.findall(r"'([^']+)'", block))
    for doc_id in ids:
        candidates = [DOCS / f"{doc_id}.md", DOCS / doc_id / "index.md"]
        if not any(candidate.exists() for candidate in candidates):
            errors.append(f"sidebar doc id does not exist: {doc_id}")


def check_absolute_doc_links(errors: list[str]) -> None:
    for path in DOCS.rglob("*.md"):
        text = read(path)
        for match in re.finditer(r"\]\((/docs/[^)#]+)", text):
            doc_id = match.group(1).replace("/docs/", "")
            candidates = [DOCS / f"{doc_id}.md", DOCS / doc_id / "index.md"]
            if not any(candidate.exists() for candidate in candidates):
                errors.append(f"broken absolute docs link in {path.relative_to(ROOT)}: {doc_id}")


def check_frontmatter(errors: list[str]) -> None:
    for path in DOCS.rglob("*.md"):
        text = read(path)
        if not text.startswith("---\n") or "\ntitle:" not in text.split("---", 2)[1]:
            errors.append(f"missing title frontmatter in {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    check_readme_empty(errors)
    check_privacy_controls(errors)
    check_source_hygiene(errors)
    check_agent_guide(errors)
    check_sidebar_doc_ids(errors)
    check_absolute_doc_links(errors)
    check_frontmatter(errors)

    doc_files = list(DOCS.rglob("*.md"))
    total_words = sum(len(read(path).split()) for path in doc_files)
    print(f"Docs: {len(doc_files)} markdown files, {total_words} words")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("QA passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
