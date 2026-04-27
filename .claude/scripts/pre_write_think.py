"""
Claude Code PreToolUse hook for Edit/Write.
Outputs a thinking checklist reminder before code changes.
Always exits 0 (non-blocking, advisory only).
"""
import json
import sys

CHECKLIST = """THINK BEFORE YOU WRITE:
- What is the minimal change needed?
- Is there existing code/utility to reuse?
- Will this break any callers or imports?
- How will you verify this works?"""


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    code_extensions = (".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp", ".h")
    if any(file_path.endswith(ext) for ext in code_extensions):
        print(CHECKLIST)

    sys.exit(0)


if __name__ == "__main__":
    main()
