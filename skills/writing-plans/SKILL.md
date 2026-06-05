---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step coding task, before touching code. Produces a task-by-task implementation plan with exact file paths and complete code — no placeholders.
---

# Writing Plans

## Overview

Write the plan as if the engineer who executes it has zero context for this codebase. Document everything they need: which files to touch per task, the actual code, how to test it, what to commit. Assume a skilled developer who knows almost nothing about this toolset or problem domain.

Principles the plan should embody: DRY, YAGNI, TDD, frequent commits.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (or wherever the project keeps them).

## Scope Check

If the spec spans multiple independent subsystems, suggest splitting it into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure First

Before defining tasks, map out which files get created or modified and what each is responsible for. This locks in the decomposition.

- One clear responsibility per file. Smaller, focused files over large ones that do too much.
- Files that change together live together. Split by responsibility, not by technical layer.
- In an existing codebase, follow established patterns. Don't unilaterally restructure — but if a file you're already modifying has grown unwieldy, a split is reasonable.

## Bite-Sized Tasks

Each step is one action, 2–5 minutes. A typical task is a TDD cycle:

- Write the failing test — step
- Run it, confirm it fails — step
- Write the minimal code to pass — step
- Run tests, confirm they pass — step
- Commit — step

## Plan Header

Every plan starts with:

```markdown
# [Feature Name] Implementation Plan

> Execute this plan task-by-task with [[executing-plans]]. Steps use `- [ ]` checkboxes for tracking.

**Goal:** [one sentence — what this builds]
**Architecture:** [2–3 sentences on the approach]
**Tech Stack:** [key libraries / tools]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**
```python
def test_specific_behavior():
    assert function(input) == expected
```

- [ ] **Step 2: Run it, confirm it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL — "function not defined"

- [ ] **Step 3: Minimal implementation**
```python
def function(input):
    return expected
```

- [ ] **Step 4: Run it, confirm it passes**
Run: `pytest tests/path/test.py::test_name -v` — Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step contains the actual content the engineer needs. These are plan failures — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "handle edge cases" (without showing how)
- "Write tests for the above" (without the actual test code)
- "Similar to Task N" (repeat the code — tasks may be read out of order)
- References to types/functions/methods not defined in any task

## Self-Review

After writing the full plan, re-read the spec with fresh eyes and check the plan against it:

1. **Spec coverage** — for each requirement in the spec, can you point to a task that implements it? List any gaps and add tasks for them.
2. **Placeholder scan** — search the plan for the red flags above. Fix them.
3. **Type consistency** — do the names, signatures, and properties used in later tasks match what earlier tasks defined? (`clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.)

Fix issues inline; no need to re-review.

## Execution Handoff

After saving, offer the user two ways to execute:

1. **Subagent-driven** — dispatch a fresh subagent per task, review between tasks. Higher quality, needs subagent support. Pair with [[requesting-code-review]] after each task.
2. **Inline** — execute in this session with [[executing-plans]], checkpoints for review.

## Related

- [[executing-plans]] — runs the plan this skill produces.
- `/grill-me` — pressure-test the design *before* writing the plan.
- `/tdd` — the red-green discipline each task is built around.

