#!/usr/bin/env python3
"""Small state helper for the coreview skill.

It intentionally uses only the Python standard library and writes only under
reviews/.coreview in the detected project root.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SKILL_NAME = "coreview"
ACTIVE_CLAIM_STATUSES = {"claimed", "fixing"}
APPROVED_PREFIX = "approved"


def find_project_root(start: Path | None = None) -> Path:
    """Find the review project root from cwd, avoiding accidental subdir state."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".coreview-root").exists():
            return candidate
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "reviews" / ".coreview").exists():
            return candidate
        if (candidate / "reviews").exists() and (
            (candidate / "AGENTS.md").exists()
            or (candidate / "SKILL.md").exists()
            or (candidate / "pyproject.toml").exists()
            or (candidate / "package.json").exists()
        ):
            return candidate
    print(
        f"warning: no project marker found from {cur}; using cwd as coreview root",
        file=sys.stderr,
    )
    return cur


ROOT = find_project_root()
REVIEW_DIR = ROOT / "reviews"
STATE_DIR = REVIEW_DIR / ".coreview"
STATE_FILE = STATE_DIR / "state.json"
CLAIMS_FILE = STATE_DIR / "claims.json"
CLAIM_CONFLICT_FILE = STATE_DIR / "claim_conflicts.jsonl"
CRITICAL_FILE = STATE_DIR / "CRITICAL_AWAITING_USER.md"
DECISIONS_FILE = STATE_DIR / "decisions.md"
LOG_FILE = STATE_DIR / "activity.log"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def parse_duration(value: str) -> timedelta:
    match = re.fullmatch(r"(\d+)([smhd]?)", value.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("duration must look like 30m, 10s, 2h, or 1d")
    amount = int(match.group(1))
    unit = match.group(2) or "s"
    return {
        "s": timedelta(seconds=amount),
        "m": timedelta(minutes=amount),
        "h": timedelta(hours=amount),
        "d": timedelta(days=amount),
    }[unit]


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    """Write JSON via same-directory temp file and os.replace.

    This avoids torn reads and partial files. It does not provide full
    read-modify-write locking, but claim conflict detection catches the common
    multi-agent overlap case before a write.
    """
    ensure_dirs()
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(payload)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    ensure_dirs()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def log(agent: str, action: str, detail: str = "") -> None:
    append_jsonl(LOG_FILE, {"ts": now(), "agent": agent, "action": action, "detail": detail})


def is_approved(status: str) -> bool:
    return status.strip().lower().startswith(APPROVED_PREFIX)


def ensure_lineage(state: dict[str, Any], agent: str) -> None:
    lineage = state.setdefault("session_lineage", [])
    current_round = int(state.get("current_round", 1))
    if any(item.get("round") == current_round for item in lineage):
        return
    lineage.append({
        "round": current_round,
        "parent_round": current_round - 1 if current_round > 1 else None,
        "opened_by": agent,
        "opened_at": now(),
    })


def normalize_files(files: list[str]) -> list[str]:
    return sorted({str(Path(f).as_posix()).strip() for f in files if str(f).strip()})


def find_claim_conflict(
    claims: dict[str, dict[str, Any]],
    claim_id: str,
    agent: str,
    files: list[str],
) -> dict[str, Any] | None:
    wanted = set(normalize_files(files))
    if not wanted:
        return None
    for existing_id, claim in claims.items():
        if existing_id == claim_id:
            continue
        if claim.get("owner") == agent:
            continue
        if claim.get("status") not in ACTIVE_CLAIM_STATUSES:
            continue
        overlap = wanted.intersection(normalize_files(claim.get("files", [])))
        if overlap:
            return {
                "id": claim_id,
                "conflicts_with": existing_id,
                "owner": claim.get("owner"),
                "files": sorted(overlap),
            }
    return None


def cmd_init(args: argparse.Namespace) -> None:
    ensure_dirs()
    date = datetime.now().strftime("%Y-%m-%d")
    review_file = REVIEW_DIR / f"{date}_{args.scope}.md"
    state = read_json(STATE_FILE, {})
    if not state:
        state = {
            "schema_version": 1,
            "scope": args.scope,
            "review_file": str(review_file.relative_to(ROOT)),
            "phase": "review",
            "current_round": 1,
            "current_owner": args.agent,
            "blocked": False,
            "hard_critical_open": False,
            "agents": [args.agent],
            "session_lineage": [],
            "gate": "Not approved for sync",
            "approved": False,
            "created_at": now(),
        }
    else:
        if args.agent not in state.get("agents", []):
            state.setdefault("agents", []).append(args.agent)
        state.setdefault("approved", is_approved(str(state.get("gate", ""))))
    ensure_lineage(state, args.agent)
    state["updated_at"] = now()
    write_json(STATE_FILE, state)
    write_json(CLAIMS_FILE, read_json(CLAIMS_FILE, {}))
    if not CRITICAL_FILE.exists():
        CRITICAL_FILE.write_text("# Critical Awaiting User\n\n", encoding="utf-8")
    if not DECISIONS_FILE.exists():
        DECISIONS_FILE.write_text("# Decisions\n\n", encoding="utf-8")
    log(args.agent, "init", args.scope)
    print(json.dumps(state, indent=2, ensure_ascii=False))


def cmd_status(_args: argparse.Namespace) -> None:
    ensure_dirs()
    payload = {
        "root": str(ROOT),
        "state": read_json(STATE_FILE, {}),
        "claims": read_json(CLAIMS_FILE, {}),
        "critical_file_exists": CRITICAL_FILE.exists(),
        "critical_file_size": CRITICAL_FILE.stat().st_size if CRITICAL_FILE.exists() else 0,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_claim(args: argparse.Namespace) -> None:
    ensure_dirs()
    claims = read_json(CLAIMS_FILE, {})
    files = normalize_files(args.files)
    conflict = find_claim_conflict(claims, args.id, args.agent, files)
    if conflict:
        conflict.update({"ts": now(), "agent": args.agent, "status": args.status})
        append_jsonl(CLAIM_CONFLICT_FILE, conflict)
        print(json.dumps(conflict, indent=2, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
    claims[args.id] = {
        "owner": args.agent,
        "status": args.status,
        "files": files,
        "updated_at": now(),
    }
    write_json(CLAIMS_FILE, claims)
    log(args.agent, "claim", args.id)


def cmd_release(args: argparse.Namespace) -> None:
    ensure_dirs()
    claims = read_json(CLAIMS_FILE, {})
    if args.id in claims:
        claims[args.id]["status"] = args.status
        claims[args.id]["updated_at"] = now()
        claims[args.id]["released_by"] = args.agent
    write_json(CLAIMS_FILE, claims)
    log(args.agent, "release", f"{args.id}:{args.status}")


def cmd_prune(args: argparse.Namespace) -> None:
    ensure_dirs()
    claims = read_json(CLAIMS_FILE, {})
    cutoff = datetime.now(timezone.utc) - args.max_age
    pruned: list[str] = []
    for claim_id, claim in claims.items():
        if claim.get("status") not in ACTIVE_CLAIM_STATUSES:
            continue
        updated = parse_ts(str(claim.get("updated_at", "")))
        if updated is None or updated < cutoff:
            claim["status"] = "abandoned"
            claim["abandoned_by"] = args.agent
            claim["abandoned_at"] = now()
            pruned.append(claim_id)
    write_json(CLAIMS_FILE, claims)
    log(args.agent, "prune", ",".join(pruned) if pruned else "none")
    print(json.dumps({"pruned": pruned}, indent=2, ensure_ascii=False))


def cmd_critical(args: argparse.Namespace) -> None:
    ensure_dirs()
    state = read_json(STATE_FILE, {})
    hard = args.severity.lower() == "hard"
    if hard:
        state["blocked"] = True
        state["hard_critical_open"] = True
        state["phase"] = "awaiting_user"
        state["updated_at"] = now()
        write_json(STATE_FILE, state)
    with CRITICAL_FILE.open("a", encoding="utf-8") as f:
        f.write(f"## {args.id} - {args.severity.title()} Critical\n\n")
        f.write(f"- Agent: {args.agent}\n")
        f.write(f"- Title: {args.title}\n")
        f.write(f"- Created: {now()}\n")
        if args.files:
            f.write(f"- Files: {', '.join(normalize_files(args.files))}\n")
        f.write("\n### Needed From User\n\n- [ ] approve / reject / request alternative\n\n")
    log(args.agent, "critical", f"{args.id}:{args.severity}")


def cmd_resolve_critical(args: argparse.Namespace) -> None:
    ensure_dirs()
    state = read_json(STATE_FILE, {})
    state["blocked"] = False
    state["hard_critical_open"] = False
    state["phase"] = "review"
    state["updated_at"] = now()
    write_json(STATE_FILE, state)
    with DECISIONS_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} {args.agent}: {args.id} -> {args.decision}\n")
    log(args.agent, "resolve-critical", f"{args.id}:{args.decision}")


def cmd_new_round(args: argparse.Namespace) -> None:
    ensure_dirs()
    state = read_json(STATE_FILE, {})
    previous = int(state.get("current_round", 0))
    state["current_round"] = previous + 1
    state["current_owner"] = args.agent
    state["phase"] = args.phase
    state["updated_at"] = now()
    state.setdefault("session_lineage", []).append({
        "round": state["current_round"],
        "parent_round": previous or None,
        "opened_by": args.agent,
        "opened_at": now(),
    })
    write_json(STATE_FILE, state)
    log(args.agent, "new-round", str(state["current_round"]))


def cmd_gate(args: argparse.Namespace) -> None:
    ensure_dirs()
    state = read_json(STATE_FILE, {})
    state["gate"] = args.status
    state["approved"] = is_approved(args.status)
    state["phase"] = "final_gate"
    state["updated_at"] = now()
    write_json(STATE_FILE, state)
    log(args.agent, "gate", args.status)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage project-local coreview state.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--scope", required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("claim")
    p.add_argument("--id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--status", default="claimed")
    p.add_argument("--files", nargs="*", default=[])
    p.set_defaults(func=cmd_claim)

    p = sub.add_parser("release")
    p.add_argument("--id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--status", default="done", choices=["done", "deferred", "abandoned"])
    p.set_defaults(func=cmd_release)

    p = sub.add_parser("prune")
    p.add_argument("--agent", required=True)
    p.add_argument("--max-age", type=parse_duration, default=timedelta(minutes=30))
    p.set_defaults(func=cmd_prune)

    p = sub.add_parser("critical")
    p.add_argument("--id", required=True)
    p.add_argument("--severity", choices=["hard", "soft"], required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--files", nargs="*", default=[])
    p.set_defaults(func=cmd_critical)

    p = sub.add_parser("resolve-critical")
    p.add_argument("--id", required=True)
    p.add_argument("--decision", choices=["approve", "reject", "alternative"], required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_resolve_critical)

    p = sub.add_parser("new-round")
    p.add_argument("--agent", required=True)
    p.add_argument("--phase", default="review")
    p.set_defaults(func=cmd_new_round)

    p = sub.add_parser("gate")
    p.add_argument("--status", required=True)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_gate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
