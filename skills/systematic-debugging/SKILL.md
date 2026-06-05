---
name: systematic-debugging
description: Use when hitting any bug, test failure, or unexpected behavior — before proposing fixes. Find the root cause first; symptom patches waste time and create new bugs.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches hide the underlying issue and it comes back.

**Core principle:** find the root cause before attempting any fix. A symptom fix is a failure even if it appears to work.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose a fix.

## When to Use

Any technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues.

Especially when it's tempting to skip:
- Under time pressure (emergencies make guessing feel justified)
- "Just one quick fix" looks obvious
- You've already tried multiple fixes and none stuck
- You don't fully understand the issue yet

Simple bugs have root causes too. Systematic is *faster* than guess-and-check thrashing, not slower.

## The Four Phases

Complete each phase before moving to the next.

### Phase 1 — Root Cause Investigation

Before attempting any fix:

1. **Read the error carefully.** Full stack trace, line numbers, file paths, error codes. The message often contains the answer.
2. **Reproduce consistently.** Exact steps. Every time, or intermittent? If you can't reproduce it, gather more data — don't guess.
3. **Check recent changes.** `git diff`, recent commits, new dependencies, config or environment differences.

4. **In multi-component systems, gather evidence at each boundary.** When the system has layers (CI → build → sign, API → service → DB), add diagnostic logging at each boundary *before* proposing a fix: log what enters and exits each component, verify config/env propagation. Run once to see *where* it breaks, then investigate that specific component. Don't theorize about which layer is at fault — instrument and look.

5. **Trace the data flow backward.** When the error is deep in the call stack: where does the bad value originate? What passed it in? Keep tracing up until you find the source. Fix at the source, not at the symptom.

### Phase 2 — Pattern Analysis

1. **Find a working example.** Locate similar code in the same codebase that works. What's different?
2. **Read the reference completely.** If you're following a pattern or reference implementation, read every line — don't skim. Partial understanding guarantees bugs.
3. **List every difference** between working and broken, however small. Don't assume "that can't matter."
4. **Understand the dependencies** — config, environment, assumptions the code makes.

### Phase 3 — Hypothesis and Test

1. **Form a single hypothesis.** State it: "I think X is the root cause because Y." Be specific.
2. **Test it minimally.** The smallest change that proves or disproves it. One variable at a time.
3. **Verify before continuing.** Worked → Phase 4. Didn't work → form a *new* hypothesis; don't stack more fixes on top.
4. **When you don't know, say so.** "I don't understand X" beats pretending. Research or ask.

### Phase 4 — Implementation

1. **Create a failing test first.** Simplest reproduction. Automated if possible, a one-off script if not. You must have it before fixing. (See `/tdd`.)
2. **Implement one fix** — the root cause, one change, no "while I'm here" extras.
3. **Verify** — test passes, nothing else broke, original symptom gone. (See [[verification-before-completion]].)
4. **If the fix doesn't work:** stop. Count your attempts. Under 3 → back to Phase 1 with the new information. **3 or more → stop fixing and question the architecture (below).**

### When 3+ Fixes Fail — Question the Architecture

If each fix reveals a new problem elsewhere, or each requires "massive refactoring," that's not a failed hypothesis — it's a wrong architecture. Stop and ask:
- Is this pattern fundamentally sound, or are we continuing through inertia?
- Should we refactor the architecture instead of patching symptoms?

Discuss with the user before attempting fix #4.

## Red Flags — STOP and Return to Phase 1

If you catch yourself thinking any of these:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add several changes at once, then run tests"
- "Skip the test, I'll verify by hand"
- "It's probably X, let me fix that" (before tracing the data flow)
- "I don't fully understand it but this might work"
- "One more fix attempt" (when you've already tried 2+)
- Each fix reveals a new problem somewhere else

All of these mean: stop, go back to Phase 1. At 3+ failed fixes, question the architecture.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, skip the process" | Simple issues have root causes too — the process is fast for them. |
| "Emergency, no time" | Systematic debugging is faster than guess-and-check thrashing. |
| "Try this first, investigate later" | The first fix sets the pattern. Do it right from the start. |
| "I'll write the test after the fix works" | Untested fixes don't stick. The test first proves it. |
| "Multiple fixes at once saves time" | You can't isolate what worked, and you cause new bugs. |
| "Reference is long, I'll adapt the gist" | Partial understanding guarantees bugs. Read it fully. |
| "I see the problem, let me fix it" | Seeing the symptom ≠ understanding the root cause. |

## Quick Reference

| Phase | Activities | Done when |
|-------|-----------|-----------|
| 1. Root Cause | Read errors, reproduce, check changes, instrument boundaries | You understand WHAT and WHY |
| 2. Pattern | Find working examples, compare, list differences | Differences identified |
| 3. Hypothesis | State one theory, test minimally | Confirmed, or new hypothesis |
| 4. Implementation | Failing test, single fix, verify | Bug resolved, tests pass |

## "No Root Cause Found"

If investigation genuinely shows the issue is environmental, timing-dependent, or external: document what you checked, implement appropriate handling (retry, timeout, clear error), and add logging for next time. But ~95% of "no root cause" cases are incomplete investigation — be sure you actually finished Phase 1.

## Related

- `/diagnose` — your interactive version of this for reported bugs.
- `/tdd` — for writing the Phase 4 failing test.
- [[verification-before-completion]] — verify the fix before claiming it's done.

