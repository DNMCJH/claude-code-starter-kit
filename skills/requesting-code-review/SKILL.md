---
name: requesting-code-review
description: Use when completing a task, finishing a major feature, or before merging. Dispatches a code-reviewer subagent over a git range to catch issues before they cascade.
---

# Requesting Code Review

Dispatch a code-reviewer subagent to catch issues before they compound. The reviewer gets a precise, self-contained brief — never your session history — so it focuses on the work product, and your own context stays free for continued work.

**Core principle:** review early, review often.

> For a heavier dual-agent loop (Claude + Codex, append-only audit trail, Critical gates), use the `coreview` skill instead. This skill is the lightweight single-reviewer version.

## When to Request

**Do:**
- After each task in subagent-driven development
- After completing a major feature
- Before merging to main

**Worth it:**
- When stuck (a fresh perspective)
- Before a refactor (baseline check)
- After fixing a complex bug

## How to Request

**1. Get the git range:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)   # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch the reviewer** with the Agent tool (`general-purpose` type), filling the template in `code-reviewer.md`. Placeholders: `{DESCRIPTION}`, `{PLAN_OR_REQUIREMENTS}`, `{BASE_SHA}`, `{HEAD_SHA}`.

**3. Act on the feedback:**
- Fix Critical immediately.
- Fix Important before proceeding.
- Note Minor for later.
- Push back with reasoning if the reviewer is wrong — see [[receiving-code-review]].

## Red Flags

- Skipping review because "it's simple"
- Ignoring a Critical finding
- Proceeding with unfixed Important findings
- Arguing with valid technical feedback instead of fixing

## Related

- `code-reviewer.md` — the reviewer prompt template (in this folder).
- [[receiving-code-review]] — how to evaluate what comes back.
- [[executing-plans]] — calls this at task checkpoints.
- `coreview` — the heavier dual-agent alternative.