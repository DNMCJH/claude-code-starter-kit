#!/usr/bin/env python3
"""Install the workflow skills into Claude Code's discovery path.

Junctions each skill directory next to this script into ~/.claude/skills/<name>.
Source of truth stays in this repo; the link points back here.

Idempotent: a target already pointing at the canonical source is skipped.
A different file/directory in the way is a conflict — never silently clobbered.

Windows uses a directory junction (`mklink /J`) — no admin or developer mode
needed. POSIX uses a symlink.

Usage:
    python install_workflow_skills.py            # install all 6
    python install_workflow_skills.py --uninstall
    python install_workflow_skills.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SKILLS = [
    "writing-plans",
    "executing-plans",
    "systematic-debugging",
    "verification-before-completion",
    "requesting-code-review",
    "receiving-code-review",
]

HERE = Path(__file__).resolve().parent  # the skills/ directory


def claude_skills_root() -> Path:
    return Path.home() / ".claude" / "skills"


def is_link_to(target: Path, source: Path) -> bool:
    if not target.exists() and not target.is_symlink():
        return False
    try:
        return target.resolve(strict=False) == source.resolve(strict=False)
    except OSError:
        return False


def _is_junction(p: Path) -> bool:
    """Windows-only: True if the directory is a junction (reparse point)."""
    if os.name != "nt":
        return False
    try:
        return bool(p.lstat().st_file_attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    except (AttributeError, OSError):
        return False


def create_link(target: Path, source: Path, *, dry_run: bool) -> str:
    if target.exists() or target.is_symlink():
        return "already-installed" if is_link_to(target, source) else "conflict"
    target.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return "would-create"
    if os.name == "nt":
        # mklink /J is a cmd built-in; junction needs no admin or dev mode.
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(source)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"mklink failed: {result.stderr.strip() or result.stdout.strip()}")
    else:
        os.symlink(source, target, target_is_directory=True)
    return "created"


def remove_link(target: Path, *, dry_run: bool) -> str:
    if not target.exists() and not target.is_symlink():
        return "not-installed"
    if not target.is_symlink() and not _is_junction(target):
        return "not-a-link"  # refuse to delete a real directory
    if dry_run:
        return "would-remove"
    os.rmdir(target) if os.name == "nt" else target.unlink()
    return "removed"


MARKERS = {
    "created": "OK    ", "would-create": "DRY   ", "already-installed": "SKIP  ",
    "removed": "OK    ", "would-remove": "DRY   ", "not-installed": "SKIP  ",
    "conflict": "CONFL ", "not-a-link": "REFUSE",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove the links instead of creating them.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without changing anything.")
    args = parser.parse_args()

    root = claude_skills_root()
    print(f"source: {HERE}")
    print(f"target: {root}")
    print(f"action: {'uninstall' if args.uninstall else 'install'}"
          f"{' (dry run)' if args.dry_run else ''}\n")

    any_conflict = False
    for name in SKILLS:
        source, target = HERE / name, root / name
        if not args.uninstall and not source.is_dir():
            print(f"  ERROR  {name}  (source missing: {source})")
            any_conflict = True
            continue
        try:
            status = (remove_link(target, dry_run=args.dry_run) if args.uninstall
                      else create_link(target, source, dry_run=args.dry_run))
        except Exception as e:
            print(f"  ERROR  {name}  ({e})")
            any_conflict = True
            continue
        print(f"  {MARKERS.get(status, '?     ')} {name}  ({status})")
        if status in ("conflict", "not-a-link"):
            any_conflict = True

    if any_conflict:
        print("\nSome targets had conflicts — resolve manually and re-run.")
        print("  conflict   = something else already exists at the target")
        print("  not-a-link = target is a real directory; --uninstall won't delete it")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())


