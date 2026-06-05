---
name: executing-plans
description: Use when you have a written implementation plan to execute. Loads the plan, reviews it critically, runs each task with verification, and stops to ask rather than guessing when blocked.
---

# Executing Plans

## Overview

Load the plan, review it critically, execute every task with verification, report when complete. Plans pair with [[writing-plans]], which produces the bite-sized task structure this skill runs.

## The Process

### Step 1 — Load and Review

1. Read the plan file end to end.
2. Review it critically — identify any questions, gaps, or concerns *before* touching code.
3. If you have concerns, raise them with the user first.
4. If not, create a TodoWrite from the tasks and proceed.

### Step 2 — Execute Tasks

For each task:
1. Mark it in_progress.
2. Follow each step exactly — the plan's steps are deliberately bite-sized.
3. Run the verifications the step specifies. Don't skip them.
4. Mark it completed only after verification passes. (See [[verification-before-completion]].)

### Step 3 — Complete

After all tasks pass: run the full test suite once more, summarize what changed, and hand back to the user for review / merge. If the project uses a code-review step, trigger [[requesting-code-review]] here.

## When to Stop and Ask

Stop executing immediately when:
- You hit a blocker — missing dependency, failing test, unclear instruction.
- The plan has a critical gap that prevents starting a task.
- You don't understand an instruction.
- A verification fails repeatedly.

Ask for clarification rather than guessing. A wrong guess compounds across later tasks.

## When to Revisit the Review

Return to Step 1 when:
- The user updates the plan based on your feedback.
- The fundamental approach needs rethinking.

Don't force through a blocker — stop and ask.

## Remember

- Review the plan critically before starting.
- Follow the steps exactly; the plan owns the decisions.
- Don't skip verifications.
- Stop when blocked, don't guess.
- Never start implementation on `main`/`master` without explicit user consent — branch first.

## Related

- [[writing-plans]] — produces the plan this skill executes.
- [[verification-before-completion]] — the bar each task's verification must clear.
- [[requesting-code-review]] — review after each task or at checkpoints.
- [[systematic-debugging]] — when a task's verification fails and you need the root cause.
