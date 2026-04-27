"""
Claude Code PostToolUse hook for Edit/Write.
Runs lightweight syntax/type checks on modified code files.
Outputs warnings but never blocks (exit 0).
"""
import json
import sys
import subprocess
import os

CHECKERS = {
    ".py": [["python", "-m", "py_compile", "{file}"]],
    ".js": [["node", "--check", "{file}"]],
    ".ts": None,
    ".tsx": None,
    ".jsx": [["node", "--check", "{file}"]],
}


def find_project_root(file_path: str) -> str:
    d = os.path.dirname(os.path.abspath(file_path))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "package.json")) or os.path.exists(os.path.join(d, "pyproject.toml")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(file_path))


def check_typescript(file_path: str) -> str | None:
    root = find_project_root(file_path)
    tsconfig = os.path.join(root, "tsconfig.json")
    if not os.path.exists(tsconfig):
        return None
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    try:
        r = subprocess.run(
            [npx, "tsc", "--noEmit", "--pretty", file_path],
            capture_output=True, text=True, timeout=15, cwd=root
        )
        if r.returncode != 0:
            return r.stdout[:500] or r.stderr[:500]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path or not os.path.exists(file_path):
        sys.exit(0)

    ext = os.path.splitext(file_path)[1].lower()

    if ext in (".ts", ".tsx"):
        err = check_typescript(file_path)
        if err:
            print(f"TYPE ERROR in {os.path.basename(file_path)}:\n{err}")
        sys.exit(0)

    commands = CHECKERS.get(ext)
    if not commands:
        sys.exit(0)

    for cmd_template in commands:
        cmd = [part.replace("{file}", file_path) for part in cmd_template]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                output = (r.stderr or r.stdout)[:500]
                print(f"SYNTAX ERROR in {os.path.basename(file_path)}:\n{output}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
