#!/usr/bin/env python3
"""Install the coreview skill into each coding agent's discovery path.

Source of truth is the skill directory this script lives in (one level up from
`scripts/`). Targets are agent-specific skill discovery roots:

    Claude Code: ~/.claude/skills/coreview/
    Codex CLI:   already discovers `.agents/skills/coreview/` in-project,
                 so no install action is needed for Codex by default.

Idempotent: if the target already points at the canonical source, exit 0 quietly.
If a different file/directory is in the way, refuse — never silently clobber.

Windows uses a directory junction (`mklink /J`) which does not require admin
or developer mode. POSIX uses a symlink.

Usage:
    python scripts/install.py                    # install for all detected agents
    python scripts/install.py --target ~/.claude/skills/coreview
    python scripts/install.py --uninstall        # remove installed links
    python scripts/install.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SKILL_NAME = "coreview"
SOURCE = Path(__file__).resolve().parent.parent  # .agents/skills/coreview/


def claude_target() -> Path:
    return Path.home() / ".claude" / "skills" / SKILL_NAME


def is_link_to(target: Path, source: Path) -> bool:
    """True if `target` is a symlink / junction pointing at `source`."""
    if not target.exists() and not target.is_symlink():
        return False
    try:
        return target.resolve(strict=False) == source.resolve(strict=False)
    except OSError:
        return False


def create_link(target: Path, source: Path, *, dry_run: bool) -> str:
    """Create a directory link from `target` to `source`. Returns a status word."""
    if target.exists() or target.is_symlink():
        if is_link_to(target, source):
            return "already-installed"
        return "conflict"

    target.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        return "would-create"

    if os.name == "nt":
        # `mklink /J` makes a directory junction — no admin or dev mode needed.
        # `cmd /c` is required because mklink is a cmd built-in, not an .exe.
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
    if os.name == "nt":
        # Junctions are removed with rmdir, not del.
        os.rmdir(target)
    else:
        target.unlink()
    return "removed"


def _is_junction(p: Path) -> bool:
    """Windows-only: check if a directory is a junction (reparse point)."""
    if os.name != "nt":
        return False
    try:
        return bool(p.lstat().st_file_attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    except (AttributeError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", type=Path, action="append",
                        help="Override target path. Repeat for multiple. Default: ~/.claude/skills/coreview")
    parser.add_argument("--uninstall", action="store_true", help="Remove the link(s) instead of creating.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without changing anything.")
    args = parser.parse_args()

    targets = args.target or [claude_target()]

    print(f"source: {SOURCE}")
    print(f"action: {'uninstall' if args.uninstall else 'install'}{' (dry run)' if args.dry_run else ''}")
    print()

    any_conflict = False
    for target in targets:
        try:
            if args.uninstall:
                status = remove_link(target, dry_run=args.dry_run)
            else:
                status = create_link(target, SOURCE, dry_run=args.dry_run)
        except Exception as e:
            print(f"  ERROR  {target}  ({e})")
            any_conflict = True
            continue

        marker = {
            "created": "OK    ",
            "would-create": "DRY   ",
            "already-installed": "SKIP  ",
            "removed": "OK    ",
            "would-remove": "DRY   ",
            "not-installed": "SKIP  ",
            "conflict": "CONFL ",
            "not-a-link": "REFUSE",
        }.get(status, "?     ")
        print(f"  {marker} {target}  ({status})")
        if status in ("conflict", "not-a-link"):
            any_conflict = True

    if any_conflict:
        print()
        print("One or more targets had conflicts. Resolve manually and re-run.")
        print("  conflict   = something else exists at the target path")
        print("  not-a-link = target is a real directory, --uninstall refuses to delete it")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
