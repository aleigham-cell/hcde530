from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RULES_FILE = REPO_ROOT / ".cursorrules"

START_MARKER = "## Directory structure (auto-generated)\n<!-- TREE:START -->\n"
END_MARKER = "<!-- TREE:END -->\n"

EXCLUDE_NAMES = {
    ".git",
    ".cursor",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    ".DS_Store",
}

INCLUDE_FILE_SUFFIXES = {".py", ".csv", ".md", ".txt", ".gitignore", ".cursorrules"}


def should_include(path: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return False
    if path.is_dir():
        return True
    return path.suffix in INCLUDE_FILE_SUFFIXES or path.name in INCLUDE_FILE_SUFFIXES


def build_tree(root: Path) -> list[str]:
    lines: list[str] = []

    def walk(dir_path: Path, prefix: str = "") -> None:
        items = sorted(
            [p for p in dir_path.iterdir() if should_include(p)],
            key=lambda p: (p.is_file(), p.name.lower()),
        )

        for idx, p in enumerate(items):
            is_last = idx == len(items) - 1
            branch = "└── " if is_last else "├── "
            lines.append(f"{prefix}{branch}{p.name}{'/' if p.is_dir() else ''}")

            if p.is_dir():
                extension = "    " if is_last else "│   "
                walk(p, prefix + extension)

    lines.append(f"{root.name}/")
    walk(root)
    return lines


def update_rules_file() -> None:
    existing = RULES_FILE.read_text(encoding="utf-8") if RULES_FILE.exists() else ""

    tree_block = "```\n" + "\n".join(build_tree(REPO_ROOT)) + "\n```\n"
    new_section = START_MARKER + tree_block + END_MARKER

    if "<!-- TREE:START -->" in existing and "<!-- TREE:END -->" in existing:
        before = existing.split("<!-- TREE:START -->", 1)[0]
        after = existing.split("<!-- TREE:END -->", 1)[1]

        # Keep the header line that precedes the start marker.
        # We rebuild everything from the "Directory structure" header.
        if "## Directory structure (auto-generated)" in before:
            before = before.split("## Directory structure (auto-generated)", 1)[0]

        updated = before.rstrip() + "\n\n" + new_section + after.lstrip()
    else:
        updated = existing.rstrip() + "\n\n" + new_section

    RULES_FILE.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    update_rules_file()
