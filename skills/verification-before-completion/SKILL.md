---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing — before committing or opening a PR. Requires running the verification command and reading its output before making any success claim. Evidence before assertions, always.
---

# Verification Before Completion

## Overview

Claiming work is done without verifying it is dishonesty, not efficiency. A false "it passes" costs more than the minute it takes to check.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute the full command, fresh and complete.
3. **READ** — Full output, check exit code, count failures.
4. **VERIFY** — Does the output confirm the claim?
   - If NO: state the actual status with evidence.
   - If YES: state the claim with the evidence attached.
5. **THEN** — Make the claim.

Skipping any step is guessing, not verifying.

## Claim → Required Evidence

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | A previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs "look fine" |
| Bug fixed | Re-test the original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Subagent done | VCS diff shows the changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verifying ("Great!", "Perfect!", "Done!")
- About to commit / push / open a PR without verification
- Trusting a subagent's success report without checking the diff
- Relying on a partial check
- Thinking "just this once" — or "I'm tired, ship it"
- Any wording that implies success without having run the command

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification. |
| "I'm confident" | Confidence is not evidence. |
| "Just this once" | No exceptions. |
| "Linter passed" | Linter ≠ compiler. |
| "Agent said success" | Verify independently against the diff. |
| "Partial check is enough" | Partial proves nothing about the rest. |

## Key Patterns

**Tests**
```
✅ [run test command] [see: 34/34 pass] → "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression test (TDD red-green)**
```
✅ Write test → run (pass) → revert fix → run (MUST FAIL) → restore → run (pass)
❌ "I wrote a regression test" (without seeing it fail without the fix)
```

**Build**
```
✅ [run build] [see: exit 0] → "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Subagent delegation**
```
✅ Agent reports success → check VCS diff → verify changes → report actual state
❌ Trust the agent's report
```

## Related

- See `/tdd` for the red-green discipline this skill verifies.
- Pairs with [[systematic-debugging]] (Phase 4 ends with a verified fix).

## The Bottom Line

Run the command. Read the output. Then claim the result.
