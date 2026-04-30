"""
Claude Code PreToolUse safety guard for Bash commands.
Reads tool_input from stdin JSON, blocks dangerous patterns, allows everything else.
Exit 0 = allow, Exit 2 + JSON stdout = block.
"""
import json
import sys
import re

DANGEROUS_PATTERNS = [
    # --- Destructive file operations ---
    (r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?(-[a-zA-Z]*r[a-zA-Z]*\s+)?\s*/($|\s|;)",
     "rm -rf on root directory"),
    (r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+)?(-[a-zA-Z]*f[a-zA-Z]*\s+)?\s*/($|\s|;)",
     "rm -rf on root directory"),
    (r"rm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+/\*",
     "rm -rf on root wildcard"),
    (r"rm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\s+/\*",
     "rm -rf on root wildcard"),
    (r"rm\s+.*\s+~/?($|\s|;|\*)",
     "rm on home directory"),
    (r"rm\s+.*\s+[A-Z]:\\\\?($|\s|;|\*)",
     "rm on Windows drive root"),

    # --- Git dangerous operations ---
    (r"git\s+push\s+.*--force",
     "git force push"),
    (r"git\s+push\s+.*-f\b",
     "git force push (-f)"),
    (r"git\s+reset\s+--hard",
     "git reset --hard"),
    (r"git\s+clean\s+.*-f",
     "git clean -f (removes untracked files)"),
    (r"git\s+branch\s+-D\s+(main|master)\b",
     "delete main/master branch"),
    (r"git\s+push\s+.*--delete\s+(main|master)\b",
     "delete remote main/master"),

    # --- Database destruction ---
    (r"(?i)DROP\s+(DATABASE|TABLE|SCHEMA)\s+",
     "DROP DATABASE/TABLE"),
    (r"(?i)TRUNCATE\s+(TABLE\s+)?\w+",
     "TRUNCATE TABLE"),
    (r"(?i)DELETE\s+FROM\s+\w+\s*;",
     "DELETE FROM without WHERE clause"),

    # --- System-level danger ---
    (r"mkfs\b",
     "format filesystem"),
    (r"dd\s+if=",
     "dd raw disk write"),
    (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;?\s*:",
     "fork bomb"),
    (r"\bshutdown\b",
     "system shutdown"),
    (r"\breboot\b",
     "system reboot"),
    (r"\binit\s+0\b",
     "system halt"),

    # --- Sensitive data exfiltration ---
    (r"curl\s+.*\.(env|pem|key|credentials|id_rsa|token)",
     "curl with sensitive file"),
    (r"curl\s+.*-d\s+.*(\$\{?[A-Z_]*(TOKEN|KEY|SECRET|PASSWORD|CREDENTIAL)[A-Z_]*\}?)",
     "curl posting secrets"),

    # --- Package/supply chain ---
    (r"\bpip\s+install\s+--index-url\s+(?!https://pypi\.org)",
     "pip install from non-PyPI source"),
    (r"\bnpm\s+publish\b",
     "npm publish (accidental package publish)"),
]

TOKEN_WASTE_PATTERNS = [
    (r"\bcat\s+.+\.(log|csv|sql|dump|dat|tsv|parquet|json|xml)\b",
     "cat on likely large data file — use head/tail instead",
     "Use: head -100 <file> or tail -100 <file>"),
    (r"\bcat\s+.+\bnode_modules\b",
     "cat inside node_modules — huge output",
     "Use: head -50 <file>"),
    (r"\bfind\s+/\s+",
     "find from root — will produce massive output",
     "Add -maxdepth or narrow the path"),
    (r"\bfind\s+\.\s+(?!.*-maxdepth)",
     "find without -maxdepth — may produce huge output",
     "Add -maxdepth 3 or pipe to head"),
    (r"\bgit\s+log\b(?!.*(-n\s*\d|--oneline|-\d+|HEAD~|\.\.|\s+--\s))",
     "git log without limit — entire history",
     "Add -n 20 or --oneline"),
    (r"\bnpm\s+list\b(?!.*--depth)",
     "npm list without --depth — full dependency tree",
     "Add --depth=0"),
    (r"\bdocker\s+logs\b(?!.*--tail)",
     "docker logs without --tail — may dump entire log",
     "Add --tail 100"),
    (r"\bpip\s+list\b.*\|?\s*$",
     "pip list dumps all packages — usually unnecessary",
     "Use: pip show <package> for specific info"),
    (r"\btree\b(?!.*-L\s)",
     "tree without depth limit — may produce huge output",
     "Add -L 3 to limit depth"),
]


def check_command(command: str) -> tuple[bool, str]:
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return True, reason
    return False, ""


def check_token_waste(command: str) -> tuple[bool, str, str]:
    for pattern, reason, fix in TOKEN_WASTE_PATTERNS:
        if re.search(pattern, command):
            return True, reason, fix
    return False, "", ""


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    is_dangerous, reason = check_command(command)
    if is_dangerous:
        result = {
            "decision": "block",
            "reason": f"BLOCKED by safety guard: {reason}\nCommand: {command}"
        }
        print(json.dumps(result))
        sys.exit(2)

    is_wasteful, reason, fix = check_token_waste(command)
    if is_wasteful:
        result = {
            "decision": "block",
            "reason": f"TOKEN GUARD: {reason}\n{fix}\nCommand: {command}"
        }
        print(json.dumps(result))
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
