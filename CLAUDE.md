# CLAUDE.md

## User Context
<!-- Describe yourself so Claude can calibrate explanations and suggestions -->
<!-- 描述你自己，让 Claude 能调整解释的深度和建议的方向 -->
CS student learning software development. Explain concepts concretely, don't skip steps.

## Communication
- Respond in the language the user uses (usually Chinese for conversation, English for code)
- Code comments: English, concise, professional — no filler comments
- Commit messages: English, conventional commits format (`feat:`, `fix:`, `docs:`)
- When facing multiple approaches: list options, let user decide

## Code Style
- Minimal code — only what's needed to solve the problem
- No premature abstractions, no speculative features
- Comments only when WHY is non-obvious

## Token Efficiency
<!-- Token = 钱，下面这些规则帮你省 token。Claude 会在每次任务开头告诉你建议的 effort level -->
- **Every non-trivial task must start with:** "建议：{effort level}，{thinking mode on/off}" — no exceptions
  - Simple Q&A / reading output → low, no thinking
  - Code edits / bug fixes → medium or high
  - Code generation / complex analysis → high or extra high
  - Architecture decisions / deep reasoning → extra high + thinking mode
- Prefer dedicated tools (Read/Grep/Glob) over Bash equivalents (cat/grep/find)
- Use subagents for large searches to protect main context
- Avoid reading entire large files — use targeted reads with offset/limit
- When web searching: prefer WebSearch over firecrawl for simple queries (firecrawl has limited credits)

## Context Management
Proactively monitor context health. Suggest user run `/compact` when ANY of these triggers hit:
- Topic switch: user moves to a completely different task
- Stage complete: a multi-step task finishes (all todos done)
- Heavy tool use: 5+ consecutive tool-heavy turns (large reads, multi-file edits, searches)
- Conversation length: ~20 turns since last compact or session start
When suggesting compact, provide a 2-3 line summary of what's worth preserving.

## Workflow
- Simplicity first: native tools > code solutions
- Safety guard hook active: dangerous commands and token-wasteful commands are auto-blocked
- Pre-write checklist and post-write syntax check hooks are active
