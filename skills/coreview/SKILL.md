---
name: coreview
description: Coordinate multi-agent code review and fix loops between Codex, Claude Code, or another coding agent. Use when the user asks for /coreview, /co-review, coreview, co-review, unattended coreview, autonomous co-review, counter-review, cross-agent review, dual-agent review, "针对 ... 进行 coreview", "双 agent 互审", "跨 agent 复审", "让 Claude 和 Codex 一起 review", "无人值守 coreview", or wants two agents to converge on code fixes with Critical findings shown to the user first, append-only review logs, local verification, final gate, and human audit checklist.
---

# Coreview

## Purpose

Run an append-only, multi-agent review loop that lets two coding agents independently inspect, fix, counter-review, and converge without losing the human decision points. Treat this as a protocol, not a fully autonomous runtime.

Use project-local `reviews/` files as the source of truth. Use `reviews/.coreview/` for machine-readable state.

## Required User Update

If `AGENTS.md` mandates a preface format, follow it. Otherwise start directly. State which project/scope you are reviewing and that Critical findings will be shown before fixes.

If the user asks for unattended/autonomous mode, say that local reversible fixes can proceed without interruption, but destructive production/data/secret decisions will be deferred into the final human audit checklist instead of being executed.

## Directory Contract

Use these files under the project root:

```text
reviews/
  README.md
  YYYY-MM-DD_<scope>.md
  .coreview/
    state.json
    claims.json
    CRITICAL_AWAITING_USER.md
    decisions.md
    activity.log
```

Create them with `scripts/coreview_state.py init --scope <scope> --agent <agent-id>` when missing. If the script is not available, create the same files manually.

## Severity Gates

Classify every finding before fixing:

- **Hard Critical**: security/data loss/production deployment/irreversible migration/auth boundary. Stop automatic code edits, write `CRITICAL_AWAITING_USER.md`, summarize to the user, and wait for explicit approval or rejection.
- **Soft Critical**: API compatibility, schema change, large behavior change, or high blast radius. Continue unrelated non-critical work, but do not fix that item until the user approves.
- **Important**: fix or defer with rationale; peer review required.
- **Minor**: fix when low-risk and local; otherwise record.

Never bury Critical decisions inside a long review file. Surface them in chat and in `CRITICAL_AWAITING_USER.md`.

## Unattended Mode

Use unattended mode when the user says they want to start both sides and then leave, sleep, eat, or otherwise avoid manual relay until the final result.

In unattended mode:

1. Do not ask the user to copy/paste peer messages. Communicate only through `reviews/` and `reviews/.coreview/`.
2. Continue non-critical local work automatically: review, claim, fix, counter-review, verify, and update gates.
3. For Hard Critical findings, choose the safest reversible local path only when it has no external side effects and does not require product/infra ownership.
4. Never execute destructive or external actions without explicit user approval: server sync, secret rotation, database migration, data deletion, payment/provider changes, production deploys, or overwriting remote files.
5. If a Hard Critical needs human judgment, write it to `CRITICAL_AWAITING_USER.md`, continue unrelated safe work, and include it in the final answer and human audit checklist. Do not repeatedly interrupt the user mid-run unless they explicitly requested live interruptions.
6. If the final gate depends on a deferred Hard Critical, use `Not approved for sync` or `Approved for next local batch`, not `Approved for local-to-server sync`.
7. Before the final response, read the review tail and state one last time to catch concurrent peer writes.

## Core Loop

1. **Initialize**
   - Read `AGENTS.md`, project review workflow, `reviews/README.md`, and current `git status`.
   - Reuse the same review file for same date/scope.
   - Initialize `.coreview` state.

2. **Independent Review**
   - Inspect code and write findings to the review file.
   - Include concrete `file:line` references.
   - Do not fix Hard Critical findings before user approval.

3. **Claim Work**
   - Before editing, claim each non-critical item in `claims.json`.
   - Include `files: list[str]`; the state script rejects overlapping active claims by another agent.
   - Do not edit files already claimed by the peer unless the claim is stale and you record why.
   - Keep claims narrow: finding id, files, owner, status.

4. **Fix Pass**
   - Apply targeted fixes.
   - Append fix implementation notes; do not only tick checkboxes.
   - Preserve unrelated user/peer changes.

5. **Counter-review**
   - Read the peer's latest appended section and current diff.
   - Accept, reject, or add blockers with concrete locations.
   - Answer any explicit peer questions.

6. **Verification**
   - Run local verification appropriate to the stack.
   - At minimum for Python: `python -m py_compile` over touched app files.
   - Run tests when collection is expected to work.
   - Record exact commands and results in the review file.

7. **Final Gate**
   - Update `reviews/README.md`.
   - Final statuses:
     - `Not approved for sync`
     - `Approved for local-to-server sync`
     - `Approved for next local batch`
   - Include human audit checklist when sync/deploy is next.

## Polling / Continue Mode

When the user says `/coreview continue`, `coreview`, `co-review`, or asks you to check again:

1. Read `reviews/.coreview/state.json`, `claims.json`, review tail, and `git status`.
2. If `CRITICAL_AWAITING_USER.md` has unresolved Hard Critical items, do not edit code. Summarize the pending decisions.
3. If the peer appended new fixes/review since your last section, counter-review them.
4. If no new peer work exists, run verification and update the gate if the state changed.
5. Before final response, read the review file tail one more time to catch concurrent peer writes.

Thirty-second polling can be simulated by repeated invocations. Do not start a background daemon unless the user explicitly asks.

Recommended unattended launch:

```text
Claude Code: /loop 50s coreview continue
Codex: run /coreview <scope> once, then use any available loop/continue mechanism; if no loop exists, the user can later say "coreview continue" and the shared files will preserve state.
```

If both runtimes support a loop command and share the same working directory, start both loops and let them converge through the state files. If only one side supports loops, that side can keep counter-reviewing automatically while the other side advances on the next user-triggered continue.

Each loop tick should:

1. Read `state.json`, `claims.json`, `CRITICAL_AWAITING_USER.md`, and the review tail.
2. Run `prune --max-age 30m` before taking new claims.
3. If blocked by Hard Critical, only do unrelated safe review/fix work.
4. If peer work changed, counter-review it.
5. If local safe work is available, claim and fix it.
6. Run verification when the state reaches a candidate gate.
7. Append a concise section only when something changed.

## State Script

Use `scripts/coreview_state.py` for mechanical state operations:

```bash
python <skill>/scripts/coreview_state.py init --scope security-hardening --agent codex
python <skill>/scripts/coreview_state.py status
python <skill>/scripts/coreview_state.py claim --id I1 --agent codex --files backend/app/api/match.py
python <skill>/scripts/coreview_state.py prune --agent codex --max-age 30m
python <skill>/scripts/coreview_state.py critical --id C1 --severity hard --agent codex --title "Weak production secret"
python <skill>/scripts/coreview_state.py resolve-critical --id C1 --decision approve --agent human
python <skill>/scripts/coreview_state.py new-round --agent codex --phase counter_review
python <skill>/scripts/coreview_state.py gate --status "Approved for local-to-server sync" --agent codex
```

Prefer the script for JSON updates. If another agent uses YAML, preserve its file and also keep the JSON state current; the review markdown remains authoritative for humans.

## Review Section Templates

Use concise append-only sections:

```markdown
## Review - <Agent> - <date>

### Critical
- [ ] **[file:line]** Description - why it matters -> fix: suggestion

### Important
- [ ] **[file:line]** Description

### Verification
- Not run yet.
```

```markdown
## Fix Pass - <Agent> - <date>

### Applied
- [x] **ID** Files changed and why

### Deferred
- [ ] **ID** Rationale and owner

### Verification
- `<command>`: passed/failed
```

```markdown
## Co-review - <Agent> - <date>

### Accepted
- [x] **ID** Reason

### Blocking
- [ ] **[file:line]** Issue

### Gate
- Status: **Approved for local-to-server sync** / **Not approved for sync**
```

## Human Audit Checklist

For a final approved sync/deploy gate, include:

```markdown
## Human Audit Checklist

- [ ] Review all Hard Critical decisions and accepted deferrals.
- [ ] Confirm production `.env` secrets are real non-placeholder values.
- [ ] Confirm database migrations or data-impacting operations are backed up.
- [ ] Confirm server backup path before overwriting remote files.
- [ ] Confirm remote verification commands to run after sync.
```

For unattended mode, also include:

```markdown
## Unattended Decisions Made

- [ ] Local reversible decisions made by agents:
- [ ] Critical decisions deferred to user:
- [ ] External actions not executed:
```

## Design Notes

Borrow useful ideas without importing a heavy runtime:

- Hermes-style session lineage: keep round ids, parent ids, and sign-off table in the review file/state.
- Hermes-style skill memory: after repeated successful runs, update this skill or project review conventions.
- OpenClaw-style visible agent state: keep state files readable and small so the user can inspect progress.
- OpenClaw-style guardrails: use explicit claims, Critical freeze, and human approval for risky actions.

Do not add autonomous background agents, external services, or broad filesystem watchers unless the user asks. The default implementation must stay local, append-only, and auditable.
