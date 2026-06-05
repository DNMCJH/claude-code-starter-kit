---
name: receiving-code-review
description: Use when receiving code-review feedback, before implementing the suggestions — especially if feedback is unclear or technically questionable. Requires technical evaluation and verification, not performative agreement or blind implementation.
---

# Receiving Code Review

## Overview

Code review feedback is input to evaluate, not orders to follow. Review requires technical judgment, not emotional performance.

**Core principle:** verify before implementing, ask before assuming, technical correctness over social comfort.

## The Response Pattern

1. **READ** — the complete feedback, without reacting.
2. **UNDERSTAND** — restate each requirement in your own words (or ask).
3. **VERIFY** — check it against the actual codebase.
4. **EVALUATE** — is it technically sound for *this* codebase?
5. **RESPOND** — technical acknowledgment, or reasoned pushback.
6. **IMPLEMENT** — one item at a time, test each.

## Skip the Performance

Don't open with "You're absolutely right!", "Great point!", or "Let me implement that now" (before verifying). Don't thank the reviewer. The code itself shows you heard the feedback.

Instead: restate the requirement, ask if unclear, push back with reasoning if it's wrong, or just start working. When feedback is correct: `"Fixed — [what changed]"` or `"Good catch, [issue]. Fixed in [location]."`

## Unclear Feedback

If any item is unclear, stop — implement nothing yet — and ask about the unclear items first. Items are often related; partial understanding produces the wrong implementation.

```
Reviewer: "Fix items 1–6"
You understand 1,2,3,6 but not 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
❌ Implement 1,2,3,6 now, ask about 4,5 later.
```

## By Source

**From the user (trusted):** implement after understanding. Still ask if scope is unclear. No performative agreement — just act or give a technical acknowledgment.

**From an external reviewer (skeptical):** before implementing, check —
1. Technically correct for *this* codebase?
2. Does it break existing functionality?
3. Is there a reason the current implementation is the way it is?
4. Does it hold on all platforms / versions you support?
5. Does the reviewer have the full context?

If it seems wrong, push back with technical reasoning. If you can't verify it, say so: *"I can't verify this without [X]. Investigate, ask, or proceed?"* If it conflicts with the user's prior architectural decisions, stop and raise it with the user first.

## YAGNI Check

If a reviewer suggests "implementing this properly," grep the codebase for actual usage first.
- Unused → *"Nothing calls this. Remove it (YAGNI)?"*
- Used → implement it properly.

## When to Push Back

Push back when the suggestion breaks existing functionality, the reviewer lacks context, it violates YAGNI, it's wrong for this stack, legacy/compat reasons exist, or it conflicts with an architectural decision. Use technical reasoning, reference working tests/code, involve the user if it's architectural.

If you pushed back and turned out wrong, state the correction factually and move on: *"You were right — I checked [X], it does [Y]. Implementing now."* No long apology, no defending why you pushed back.

## Implementation Order

For multi-item feedback: clarify everything unclear first, then implement blocking issues (breaks, security) → simple fixes (typos, imports) → complex fixes (refactors, logic). Test each fix individually; verify no regressions. (See [[verification-before-completion]].)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State the requirement, or just act. |
| Blind implementation | Verify against the codebase first. |
| Batch without testing | One at a time, test each. |
| Assuming the reviewer is right | Check whether it breaks things. |
| Avoiding pushback | Technical correctness over comfort. |
| Partial implementation | Clarify all items first. |
| Can't verify, proceed anyway | State the limitation, ask for direction. |

## GitHub Threads

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## Related

- [[requesting-code-review]] — the other side of the loop.
- [[verification-before-completion]] — verify each fix before claiming it's done.
