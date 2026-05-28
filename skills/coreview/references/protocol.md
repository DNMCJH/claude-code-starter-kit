# Coreview Protocol Reference

Use this reference when a review needs stricter coordination than the short workflow in `SKILL.md`.

## State Meanings

- `review`: agents may inspect and write findings.
- `fixing`: an agent has claimed at least one item and is editing.
- `awaiting_user`: a Hard Critical finding exists; automatic edits must stop.
- `counter_review`: one agent has appended fixes and the other should inspect.
- `final_gate`: all blocking issues are resolved or explicitly deferred.

## Claim Rules

- Claim by finding id, not by broad feature area.
- Include touched files.
- The state script rejects overlapping active claims (`claimed` or `fixing`) by another agent.
- Run `prune --max-age 30m` before taking over stale work; use 30 minutes unless the review file records a different threshold.
- Release claims as `done`, `deferred`, or `abandoned`.
- If a claim is stale, append a note in the review file before taking over.

## Critical Decision Format

Use this in `CRITICAL_AWAITING_USER.md`:

```markdown
## C1 - Hard Critical

- Agent:
- Files:
- Impact:
- Options:
- Recommendation:

### Needed From User

- [ ] approve option A
- [ ] approve option B
- [ ] reject / defer
```

## Unattended Decision Policy

- Agents may choose the safest reversible local code fix without user input.
- Agents may defer product/infra/security decisions and keep working on unrelated safe items.
- Agents must not perform server sync, deploy, secret rotation, database migration, destructive filesystem operations, or remote overwrites without explicit user approval.
- If unattended mode ends with deferred Critical items, final gate cannot be `Approved for local-to-server sync`.
- The final response must include what was decided automatically, what was deferred, and what still needs user approval.

## Final Checklist

Before approval:

- Review tail read after all edits.
- `git status --short` checked.
- Local verification commands recorded.
- Deferred items named with owner/rationale.
- Server sync not performed unless the user explicitly confirmed.
