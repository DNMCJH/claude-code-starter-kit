# CLAUDE.md

## User Context

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

- Prefer dedicated tools (Read/Grep/Glob) over Bash equivalents
- Avoid reading entire large files — use targeted reads with offset/limit
- When web searching: prefer gemini-google-search over firecrawl for simple queries (firecrawl has limited credits)
- When using Read tool on PDFs: always provide a real page range, never pass empty `pages` field

## Context Management

Proactively suggest /compact when:

- Topic switch: user moves to a completely different task
- Stage complete: a multi-step task finishes
- Heavy tool use: 5+ consecutive tool-heavy turns
- Conversation length: ~20 turns since last compact

## Workflow

- Simplicity first: native tools > code solutions
- Safety guard hook active: dangerous commands and token-wasteful commands are auto-blocked
- Pre-write checklist and post-write syntax check hooks are active
- After completing a repeatable multi-step workflow (3+ steps, likely to recur), ask if user wants to package it as a skill
