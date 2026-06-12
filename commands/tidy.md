After a debug session, major refactor, or feature completion, run a cleanup sweep on the project. Goal: remove noise, keep the codebase lean.

## Checklist

Work through each item. Report findings as a numbered list with action recommendations.

### 1. Debug residue

- [ ] Search for leftover debug prints/logs (`print(`, `console.log`, `logger.debug`, `[DEBUG-`)
- [ ] Search for commented-out code blocks (more than 2 consecutive commented lines)
- [ ] Search for TODO/FIXME/HACK/XXX comments — flag any that are now resolved
- [ ] Check for temporary test files or scratch scripts (`test_*.py`, `temp_*`, `scratch.*`, `*.bak`)

### 2. Dead code & unused imports

- [ ] Identify unused imports in changed files
- [ ] Identify functions/classes that lost all callers during the change
- [ ] Check for orphaned files (created during the work but no longer imported anywhere)

### 3. Project structure

- [ ] Empty directories that should be removed
- [ ] Files in wrong directories (e.g., utils dumped in root, test files outside test dirs)
- [ ] Duplicate or near-duplicate files
- [ ] Config files with stale entries (unused env vars, dead endpoints)

### 4. Dependency hygiene

- [ ] Packages added during the work but no longer used in code
- [ ] Lockfile consistent with requirements/package.json

### 5. Code quality quick scan

- [ ] Functions that grew too long (>50 lines) during the change
- [ ] Overly broad exception handlers (`except Exception`, bare `except:`)
- [ ] Hardcoded values that should be constants or config
- [ ] Inconsistent naming introduced during the change

### 6. Git hygiene

- [ ] Untracked files that should be gitignored (logs, coverage, build output, `.pyc`, `node_modules`)
- [ ] Sensitive files at risk of being committed (`.env`, credentials, API keys in code)
- [ ] Stale local branches created during debug (`debug-*`, `temp-*`, `wip-*`)

### 7. Test health

- [ ] Temporarily skipped/disabled tests (`@pytest.mark.skip`, `.skip(`, `xit(`, `xdescribe(`) — should any be re-enabled?
- [ ] Run the test suite — any regressions introduced?
- [ ] Test fixtures or mock data added during debug that are no longer needed

### 8. Documentation drift

- [ ] README still accurate after the change? (setup steps, API examples, architecture diagrams)
- [ ] Docstrings on changed public functions — still match behavior?
- [ ] CHANGELOG or migration notes needed?

### 9. Skills & config hygiene

- [ ] Slash commands in `~/.claude/commands/` — any that overlap or should be merged?
- [ ] CLAUDE.md — any rules that contradict each other or are now outdated?
- [ ] Memory files in `~/.claude/projects/*/memory/` — any stale or duplicate entries?
- [ ] Hooks in settings.json — any that no longer apply?

## Output format

For each finding:
```
[category] file:line — what's wrong — suggested action (delete/move/refactor/keep with reason)
```

Ask me before making any deletions. Present the full list first, let me approve.
