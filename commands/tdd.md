# Test-Driven Development

Build features or fix bugs using red-green-refactor, one vertical slice at a time.

## Philosophy

Tests verify BEHAVIOR through public interfaces, not implementation details. A good test reads like a spec and survives refactors.

## Anti-Pattern: Horizontal Slices

DO NOT write all tests first, then all implementation. That produces tests coupled to imagined behavior.

```
WRONG:  RED: test1,test2,test3 → GREEN: impl1,impl2,impl3
RIGHT:  RED→GREEN: test1→impl1 → RED→GREEN: test2→impl2 → ...
```

## Workflow

### 1. Planning (before any code)

- Detect the project's test framework and runner (check package.json, pyproject.toml, pytest.ini, etc.). If none exists, ask me which to set up
- Confirm with me what interface changes are needed
- Confirm which behaviors to test (prioritize — can't test everything)
- List behaviors to test (not implementation steps)
- Get my approval on the plan

### 2. Tracer Bullet

Write ONE test that confirms ONE thing:
```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

### 3. Incremental Loop

For each remaining behavior:
```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:
- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests

### 4. Refactor

After all tests pass:
- Extract duplication
- Apply SOLID where natural
- Run tests after each refactor step
- NEVER refactor while RED — get to GREEN first

## Checklist Per Cycle

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interface only
- [ ] Test would survive internal refactor
- [ ] Code is minimal for this test
- [ ] No speculative features added
