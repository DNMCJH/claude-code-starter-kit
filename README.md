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

### Option 1: Let Claude Code install it for you (easiest)

If you already have Claude Code running, just send it this message:

```
Help me install the Claude Code starter kit.
Repo: https://github.com/DNMCJH/claude-code-starter-kit
Please read the README from this repo, then:
1. Write the global-settings.json contents to my ~/.claude/settings.json (keep my existing env config)
2. Copy CLAUDE.md and .claude/ folder to my current project root
3. Update the User Context section in CLAUDE.md with my background
4. Verify the hooks work
```

Claude Code will read the repo, download files, and set everything up for you.

### Option 2: Manual setup

### Step 1: Global config

Copy the contents of `global-settings.json` to your Claude config file:

- Windows: `C:\Users\<username>\.claude\settings.json`
- Mac/Linux: `~/.claude/settings.json`

Fill in your API credentials:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<your-key>",
    "ANTHROPIC_BASE_URL": "<your-api-url>"
  },
  "model": "sonnet",
  "effortLevel": "medium",
  "includeCoAuthoredBy": false
}
```

> Using official Anthropic subscription (Max plan)? Remove the `env` block entirely — it's not needed.

### Step 2: Project config

Copy `CLAUDE.md` and `.claude/` into your project root:

```bash
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### Step 3: Edit CLAUDE.md

Open `CLAUDE.md` in your project and update the `User Context` section to describe yourself:

```markdown
## User Context
CS junior, familiar with Python and MATLAB, working on digital watermarking.
```

### Step 4: Verify

Start Claude Code in your project directory and try these:

1. Ask Claude to run `ls` — you should see "Safety check..." flash in the status bar
2. Ask Claude to run `rm -rf /` — it should be **blocked** by the safety guard
3. Ask Claude to edit a `.py` file — you should see "Think before write..." then "Checking syntax..."

If all three work, you're good to go.

## What the Hooks Do

| Hook | When | What |
|------|------|------|
| `bash_safety_guard.py` | Before any Bash command | Blocks `rm -rf /`, `git push --force`, `DROP TABLE`, fork bombs, etc. Also blocks token-wasteful commands like `cat` on large files or `git log` without limit |
| `pre_write_think.py` | Before Edit/Write on code files | Prints a thinking checklist: minimal change? reuse existing code? break callers? |
| `post_write_check.py` | After Edit/Write on code files | Runs `py_compile` (Python), `node --check` (JS), `tsc --noEmit` (TS) |

## What CLAUDE.md Does

`CLAUDE.md` is the project instruction file that Claude reads at the start of every conversation. The template includes:

- **User Context** — Tell Claude your skill level so it calibrates explanations
- **Communication** — Language preferences, commit message format
- **Code Style** — Minimal code, no premature abstractions
- **Token Efficiency** — Effort level suggestions, tool preferences, context management
- **Workflow** — Hook status reminders

Edit it to match your background and project needs.

## Permission Presets

The project `settings.json` auto-allows common dev commands so you don't get prompted every time:

- **Git**: all standard operations (add, commit, push, pull, branch, etc.)
- **Package managers**: npm, pnpm, pip
- **Runtimes**: node, npx, python, python3
- **File ops**: mkdir, cp, mv, rm, touch, chmod, curl
- **Utilities**: ls, find, cat, head, tail, wc, echo, pwd, which, diff, grep
- **Editors**: code (VS Code)
- **Tools**: Write, Edit (file editing)

Need more? Add `"Bash(docker *)"`, `"Bash(ssh *)"`, etc. to the `allow` list in `.claude/settings.json`.

## Global Settings Explained

| Field | What | Options |
|-------|------|---------|
| `env.ANTHROPIC_AUTH_TOKEN` | API key (proxy users only) | Your API key |
| `env.ANTHROPIC_BASE_URL` | API endpoint (proxy users only) | Your proxy URL |
| `model` | Default model | `sonnet`, `opus`, `haiku`, or with context: `opus[1m]` |
| `effortLevel` | Response effort | `low`, `medium`, `high` |
| `includeCoAuthoredBy` | Add co-author tag to commits | `true` / `false` |

## Customization Guide

### For beginners
1. Edit `CLAUDE.md` — change the User Context section to describe yourself
2. Fill in API credentials in `~/.claude/settings.json`
3. Start using Claude Code

### For intermediate users
4. Add/remove commands in `.claude/settings.json` permissions
5. Add more blocked patterns to `bash_safety_guard.py`
6. Add language-specific checkers to `post_write_check.py`

### For advanced users
7. Add MCP tool permissions (Playwright, Firecrawl, etc.) to `.claude/settings.json`
8. Add custom hooks (e.g., firecrawl crawl limit, browser URL safety check)
9. Create custom slash commands in `~/.claude/commands/`

## Troubleshooting

**"Safety check..." doesn't appear when running commands**
- Make sure `.claude/scripts/` exists in your project root
- Check that Python 3.10+ is installed: `python --version`
- On Mac/Linux, ensure scripts are executable: `chmod +x .claude/scripts/*.py`

**Permission prompts still appear for allowed commands**
- Check that `.claude/settings.json` is in the project root (not a subdirectory)
- Verify the command pattern matches — `Bash(git *)` covers `git status`, `git add .`, etc.

**Syntax check hook doesn't work for TypeScript**
- Ensure `tsconfig.json` exists in your project
- Install TypeScript: `npm install -D typescript`

**"python: command not found" on Mac**
- The hooks already try `python3` first, then fall back to `python`. If neither works, install Python 3: `brew install python`

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (for hook scripts)
- Node.js (optional, for JS/TS syntax checking)

## License

[MIT](LICENSE)
