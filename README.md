# Claude Code Starter Kit

A ready-to-use configuration pack for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — includes safety hooks, permission presets, and a project instruction template.

[中文说明](README_CN.md)

## What's Inside

```
├── CLAUDE.md                     # Project instructions template
├── global-settings.json          # Global config template (~/.claude/settings.json)
└── .claude/
    ├── settings.json             # Project-level permissions + hooks
    └── scripts/
        ├── bash_safety_guard.py  # Blocks dangerous & token-wasteful commands
        ├── pre_write_think.py    # Thinking checklist before code changes
        └── post_write_check.py   # Auto syntax check after code changes
```

## Quick Start

### 1. Global config

Copy `global-settings.json` to your Claude config directory:

- Windows: `C:\Users\<username>\.claude\settings.json`
- Mac/Linux: `~/.claude/settings.json`

Fill in your API credentials:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<your-key>",
    "ANTHROPIC_BASE_URL": "<your-api-url>"
  }
}
```

> Using official Anthropic subscription (Max plan)? Remove the `env` block entirely — it's not needed.

### 2. Project config

Copy `CLAUDE.md` and `.claude/` into your project root:

```bash
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### 3. Verify

Start Claude Code in your project directory. Run any bash command — you should see "Safety check..." in the status.

## What the Hooks Do

| Hook | When | What |
|------|------|------|
| `bash_safety_guard.py` | Before any Bash command | Blocks `rm -rf /`, `git push --force`, `DROP TABLE`, fork bombs, etc. Also blocks token-wasteful commands like `cat` on large files or `git log` without limit |
| `pre_write_think.py` | Before Edit/Write on code files | Prints a thinking checklist: minimal change? reuse existing code? break callers? |
| `post_write_check.py` | After Edit/Write on code files | Runs `py_compile` (Python), `node --check` (JS), `tsc --noEmit` (TS) |

## Permission Presets

The project `settings.json` auto-allows common dev commands (git, npm, pip, python, file ops, etc.) so you don't get prompted every time. Review and adjust to your needs.

## Customization

- Edit `CLAUDE.md` to describe your background, coding style, and project context
- Add/remove commands in `.claude/settings.json` permissions as needed
- Add more patterns to `bash_safety_guard.py` for your workflow

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (for hook scripts)
- Node.js (optional, for JS/TS syntax checking)

## License

[MIT](LICENSE)
