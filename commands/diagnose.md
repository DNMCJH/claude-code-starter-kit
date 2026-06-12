# Diagnose

Disciplined diagnosis loop for hard bugs. Skip phases only when explicitly justified.

## Phase 1 — Build a feedback loop

**This is the skill.** If you have a fast, deterministic pass/fail signal, you will find the cause. Spend disproportionate effort here.

Try in order (pick the lightest one that works):
1. Failing test (unit/integration/e2e)
2. Curl/HTTP script against dev server
3. CLI invocation with fixture input, diff against known-good
4. Throwaway harness — minimal subset exercising the bug path
5. Bisection harness (`git bisect run`) for "it worked before" bugs
6. For non-deterministic bugs: loop the trigger 100x, raise repro rate until debuggable

Iterate on the loop: make it faster, sharper, more deterministic. A 2-second deterministic loop is a debugging superpower.

**If you cannot build a loop**: stop and say so. List what you tried. Ask me for environment access, captured artifacts, or permission to add temp instrumentation. Do NOT proceed without a loop.

## Phase 2 — Reproduce

Run the loop. Confirm:
- [ ] Failure matches what I described (not a different nearby failure)
- [ ] Reproducible across multiple runs
- [ ] Exact symptom captured (error message, wrong output, timing)

## Phase 3 — Hypothesise

Generate **3-5 ranked hypotheses** before testing any. Each must be falsifiable:

> "If [X] is the cause, then [action] will make the bug disappear / [action] will make it worse."

Show the ranked list to me before testing — I may have domain knowledge that re-ranks instantly.

## Phase 4 — Instrument

Each probe maps to a specific prediction from Phase 3. Change one variable at a time.

1. Debugger/REPL inspection first (one breakpoint beats ten logs)
2. Targeted logs at boundaries that distinguish hypotheses
3. **Tag every debug log** with `[DEBUG-xxxx]` prefix for easy cleanup

For perf regressions: measure first (timing harness, profiler, query plan), then bisect.

## Phase 5 — Fix + regression test

1. Write regression test BEFORE the fix (if a correct seam exists)
2. Watch it fail
3. Apply the fix
4. Watch it pass
5. Re-run Phase 1 loop against original scenario

## Phase 6 — Cleanup

- [ ] Original repro no longer reproduces
- [ ] Regression test passes
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] Root cause stated in commit message

Then ask: what would have prevented this bug?
