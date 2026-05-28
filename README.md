# Claude Code Starter Kit

A ready-to-use configuration pack for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — includes safety hooks, permission presets, MCP server recommendations, and a project instruction template.

[中文说明](README_CN.md)

## Architecture Overview

This kit reflects a real-world dual-track workflow:

```
Development Track                    Documentation Track
─────────────────                    ───────────────────
VSCode                               Obsidian
├── Claude Code extension            ├── Claudian plugin (Claude + Codex compatible)
├── Codex extension                  └── 闪电说 (voice input)
└── 闪电说 (voice input)

Shared Infrastructure
─────────────────────
├── 5 MCP servers (fetch, time, playwright, gemini-search, firecrawl)
├── 5 custom skills (leetcode-review, paper-note, recording, structural-learning, coreview)
├── 7 slash commands (caveman, diagnose, grill-me, tdd, tidy, html-deck, pptx-design-supplement)
├── 3 safety hooks (bash guard, pre-write think, post-write syntax check)
├── Auto-memory system (persistent cross-session context)
└── Document skills plugin (anthropic-agent-skills marketplace)
```

## What's Inside

```
├── CLAUDE.md                     # Project instructions template
├── global-settings.json          # Global config template (~/.claude/settings.json)
├── skills/
│   └── coreview/                 # Dual-agent code review skill
│       ├── SKILL.md              # Skill definition (triggers, protocol, templates)
│       ├── scripts/
│       │   ├── coreview_state.py # State CLI (init/claim/release/prune/critical/gate)
│       │   └── install.py        # Cross-platform install (junction/symlink)
│       └── references/
│           └── protocol.md       # Detailed protocol spec
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
> Note: Official subscription locks context to 200K. For 1M context, start sessions directly via a relay/proxy from the beginning (mid-session switching won't expand the window).

### 2. Project config

Copy `CLAUDE.md` and `.claude/` into your project root:

```bash
cp CLAUDE.md /path/to/your-project/
cp -r .claude/ /path/to/your-project/.claude/
```

### 3. MCP Servers (recommended)

Register these MCP servers for a complete toolkit:

```bash
claude mcp add fetch -- python -m mcp_server_fetch
claude mcp add time -- python -m mcp_server_time --local-timezone Asia/Shanghai
claude mcp add playwright -- npx @playwright/mcp@latest
claude mcp add gemini-google-search -- npx mcp-gemini-google-search
claude mcp add firecrawl -- npx -y firecrawl-mcp
```

| Server | Purpose | When to use |
| ------ | ------- | ----------- |
| fetch | Raw HTTP requests | API testing, downloading files |
| time | Timezone-aware timestamps | Scheduling, date math |
| playwright | Browser automation | UI testing, screenshots, form filling |
| gemini-google-search | Web search (free tier) | Quick lookups, current info |
| firecrawl | Web scraping/extraction | Deep content extraction (has credit limits) |

### 4. Verify

Start Claude Code in your project directory. Run any bash command — you should see "Safety check..." in the status.

## What the Hooks Do

| Hook | When | What |
|------|------|------|
| `bash_safety_guard.py` | Before any Bash command | Blocks `rm -rf /`, `git push --force`, `DROP TABLE`, fork bombs, etc. Also blocks token-wasteful commands like `cat` on large files or `git log` without limit |
| `pre_write_think.py` | Before Edit/Write on code files | Prints a thinking checklist: minimal change? reuse existing code? break callers? |
| `post_write_check.py` | After Edit/Write on code files | Runs `py_compile` (Python), `node --check` (JS), `tsc --noEmit` (TS) |

## What Makes This Setup Effective

Key design decisions from real daily use:

1. **Three-layer safety** — dangerous commands blocked at hook level (not just permissions), token waste caught before it burns context, syntax verified immediately after writes
2. **MCP over shell** — playwright for browser testing, gemini for search, firecrawl for scraping. Keeps tool calls visible and auditable vs buried in bash
3. **Skills for repeatable workflows** — leetcode review, paper notes, structural learning, recording. Each encapsulates a multi-step SOP that would otherwise require re-explaining every session
4. **Slash commands for modes** — `/caveman` for token-saving terse mode, `/grill-me` for design interrogation, `/tdd` for test-first flow. Mode switches without losing context
5. **Auto-memory for continuity** — cross-session persistent memory with typed categories (user/feedback/project/reference). Eliminates "remind me what we did last time"
6. **Permission allowlist + deny** — broad dev commands pre-allowed to reduce prompt fatigue; specific dangerous tools (file_upload) explicitly denied
7. **Dual-track separation** — development in VSCode (Claude Code + Codex), documentation in Obsidian (Claudian). Voice input (闪电说) bridges both

## Coreview Skill — Dual-Agent Code Review

The `skills/coreview/` directory contains a protocol for coordinating two coding agents (e.g. Claude Code + Codex) reviewing the same codebase.

**Install:**

```bash
python skills/coreview/scripts/install.py
```

This creates a junction/symlink at `~/.claude/skills/coreview/` pointing to the skill source. Codex discovers it in-project automatically.

**Usage:**

Say `"coreview <scope>"` or `"针对 xxx 进行 coreview"` to either agent. The flow is:

1. One agent reviews → writes findings to `reviews/YYYY-MM-DD_<scope>.md`
2. Hard Critical findings freeze edits and surface to you for approval
3. Non-critical findings are claimed by file and fixed in parallel
4. Counter-review by the other agent → verify → gate approval

The agents communicate through you — after each round, one agent outputs a message for you to relay to the other. No shared runtime or daemon needed.

**Key features:**
- Append-only audit trail (review markdown)
- Hard Critical = mandatory human gate
- Claim-by-file prevents parallel edit conflicts
- 30-minute staleness timeout for abandoned claims
- Atomic JSON state writes (no torn files)

See [SKILL.md](skills/coreview/SKILL.md) for the full protocol and [protocol.md](skills/coreview/references/protocol.md) for state machine details.

## Permission Presets

The project `settings.json` auto-allows common dev commands (git, npm, pip, python, file ops, docker, ssh, etc.) so you don't get prompted every time. Review and adjust to your needs.

## Customization

- Edit `CLAUDE.md` to describe your background, coding style, and project context
- Add/remove commands in `.claude/settings.json` permissions as needed
- Add more patterns to `bash_safety_guard.py` for your workflow
- Add custom skills in `~/.claude/skills/` for your repeatable workflows
- Add slash commands in `~/.claude/commands/` for mode switches

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (for hook scripts)
- Node.js (for MCP servers and JS/TS syntax checking)

## License

[MIT](LICENSE)
