#!/usr/bin/env python3
"""Install the slash commands into Claude Code's discovery path.

Two kinds of artifact live next to this script:

  commands/*.md       -> copied into ~/.claude/commands/<name>.md
  ../html-deck/        -> junctioned to ~/.claude/html-deck/ (assets the
                          html-deck command references at that absolute path)

Command files are copied (small, standalone, cross-platform safe). The
html-deck asset tree is large, so it is linked rather than duplicated:
Windows uses a directory junction (`mklink /J`, no admin/dev mode needed),
POSIX uses a symlink.

Idempotent: an up-to-date copy or a link already pointing at the canonical
source is skipped. A different real file/directory in the way is a conflict —
never silently clobbered.

Usage:
    python install_commands.py            # install all
    python install_commands.py --uninstall
    python install_commands.py --dry-run
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # the commands/ directory
REPO = HERE.parent                              # repo root
HTML_DECK_SRC = REPO / "html-deck"              # asset tree linked at ~/.claude/html-deck


def commands_root() -> Path:
    return Path.home() / ".claude" / "commands"


def html_deck_target() -> Path:
    return Path.home() / ".claude" / "html-deck"


# ---------- file copy (command .md) ----------

def copy_command(src: Path, dst: Path, *, dry_run: bool) -> str:
    if dst.exists():
        if dst.is_dir():
            return "conflict"                    # a directory where a file should go
        if filecmp.cmp(src, dst, shallow=False):
            return "already-installed"
        if dry_run:
            return "would-update"
        shutil.copy2(src, dst)
        return "updated"
    if dry_run:
        return "would-create"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "created"


def remove_command(dst: Path, *, dry_run: bool) -> str:
    if not dst.exists():
        return "not-installed"
    if dst.is_dir():
        return "not-a-file"                      # refuse to delete a directory
    if dry_run:
        return "would-remove"
    dst.unlink()
    return "removed"


# ---------- directory link (html-deck assets) ----------

def _is_junction(p: Path) -> bool:
    if os.name != "nt":
        return False
    try:
        return bool(p.lstat().st_file_attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    except (AttributeError, OSError):
        return False


def is_link_to(target: Path, source: Path) -> bool:
    if not target.exists() and not target.is_symlink():
        return False
    try:
        return target.resolve(strict=False) == source.resolve(strict=False)
    except OSError:
        return False


def create_link(target: Path, source: Path, *, dry_run: bool) -> str:
    if target.exists() or target.is_symlink():
        return "already-installed" if is_link_to(target, source) else "conflict"
    if dry_run:
        return "would-create"
    target.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
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
        return "not-a-link"
    if dry_run:
        return "would-remove"
    os.rmdir(target) if os.name == "nt" else target.unlink()
    return "removed"


MARKERS = {
    "created": "OK    ", "updated": "OK    ", "would-create": "DRY   ",
    "would-update": "DRY   ", "already-installed": "SKIP  ", "removed": "OK    ",
    "would-remove": "DRY   ", "not-installed": "SKIP  ", "conflict": "CONFL ",
    "not-a-link": "REFUSE", "not-a-file": "REFUSE",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--uninstall", action="store_true",
                        help="Remove installed commands and the html-deck link.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without changing anything.")
    args = parser.parse_args()

    cmd_files = sorted(HERE.glob("*.md"))
    cmd_root = commands_root()

    print(f"commands source: {HERE}")
    print(f"commands target: {cmd_root}")
    print(f"html-deck source: {HTML_DECK_SRC}")
    print(f"html-deck target: {html_deck_target()}")
    print(f"action: {'uninstall' if args.uninstall else 'install'}"
          f"{' (dry run)' if args.dry_run else ''}\n")

    any_conflict = False

    for src in cmd_files:
        dst = cmd_root / src.name
        try:
            status = (remove_command(dst, dry_run=args.dry_run) if args.uninstall
                      else copy_command(src, dst, dry_run=args.dry_run))
        except Exception as e:
            print(f"  ERROR  {src.name}  ({e})")
            any_conflict = True
            continue
        print(f"  {MARKERS.get(status, '?     ')} {src.name}  ({status})")
        if status in ("conflict", "not-a-file"):
            any_conflict = True

    # html-deck asset tree
    target = html_deck_target()
    try:
        if args.uninstall:
            status = remove_link(target, dry_run=args.dry_run)
        elif not HTML_DECK_SRC.is_dir():
            status = "not-a-link"
            print(f"  ERROR  html-deck/  (source missing: {HTML_DECK_SRC})")
        else:
            status = create_link(target, HTML_DECK_SRC, dry_run=args.dry_run)
        print(f"  {MARKERS.get(status, '?     ')} html-deck/  ({status})")
        if status in ("conflict", "not-a-link"):
            any_conflict = True
    except Exception as e:
        print(f"  ERROR  html-deck/  ({e})")
        any_conflict = True

    if any_conflict:
        print("\nSome targets had conflicts — resolve manually and re-run.")
        print("  conflict   = something else already exists at the target")
        print("  not-a-link = html-deck target is a real directory; --uninstall won't delete it")
        print("  not-a-file = a command target is a directory; resolve manually")
        return 1

    print("\nDone. Restart Claude Code so it rediscovers the commands.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
