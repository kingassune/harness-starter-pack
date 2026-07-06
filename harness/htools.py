"""Level 3 harness tools + permission gate.

Tools: update_plan, read_file, write_file, run_command, finish.
Gate:  write_file and run_command are DESTRUCTIVE and must pass a permission
       check before they run — writes are confined to the sandbox workspace,
       and dangerous shell commands are denied.
"""
import os
import re
import subprocess

# The sandbox: the harness may only write inside here.
WORKSPACE = os.path.join(os.path.dirname(__file__), ".run")

# Destructive command NAMES, matched as whole tokens (not substrings — so "dd"
# never matches inside "add").
DESTRUCTIVE_TOKENS = {
    "rm", "rmdir", "mv", "dd", "mkfs", "chmod", "chown", "sudo",
    "curl", "wget", "pip", "npm", "kill", "reboot", "shutdown",
}


def is_destructive_cmd(command):
    c = command.strip()
    if ">" in c or ":(){" in c:  # redirection writes files; fork bomb
        return True
    tokens = re.split(r"[\s|;&()]+", c)
    if "git" in tokens and "push" in tokens:
        return True
    return any(tok in DESTRUCTIVE_TOKENS for tok in tokens)


def resolve(path):
    """Relative paths are resolved against the sandbox, so all tools agree."""
    return path if os.path.isabs(path) else os.path.join(WORKSPACE, path)


def within_workspace(path):
    ap = os.path.abspath(resolve(path))
    return ap == WORKSPACE or ap.startswith(WORKSPACE + os.sep)


# ---- permission gate -------------------------------------------------------
def check_permission(name, args):
    """Return (allowed: bool, reason: str). This is the harness's guardrail."""
    if name == "write_file":
        if not within_workspace(args.get("path", "")):
            return False, f"write outside sandbox {WORKSPACE} denied"
        return True, "write within sandbox allowed"
    if name == "run_command":
        if is_destructive_cmd(args.get("command", "")):
            return False, "destructive command denied by permission gate"
        return True, "read-only command allowed"
    return True, "non-destructive tool"


# ---- schemas ---------------------------------------------------------------
TOOLS = [
    {
        "name": "update_plan",
        "description": "Write/update the milestone plan. Call this FIRST and whenever the plan changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "milestones": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step": {"type": "string"},
                            "done": {"type": "boolean"},
                        },
                        "required": ["step", "done"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["milestones"],
            "additionalProperties": False,
        },
    },
    {
        "name": "read_file",
        "description": "Read a text file and return its contents. Read-only.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "write_file",
        "description": "Overwrite a file with new contents. DESTRUCTIVE — gated; only allowed inside the sandbox.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
    },
    {
        "name": "run_command",
        "description": "Run a read-only shell command for inspection. DESTRUCTIVE commands are denied.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
            "additionalProperties": False,
        },
    },
    {
        "name": "finish",
        "description": "Declare the task complete. The harness verifies the test passes before accepting.",
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"],
            "additionalProperties": False,
        },
    },
]


# ---- implementations -------------------------------------------------------
def read_file(path):
    try:
        with open(resolve(path), "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as err:
        return f"error: {err}"


def write_file(path, content):
    full = resolve(path)
    os.makedirs(os.path.dirname(os.path.abspath(full)), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return f"wrote {len(content)} chars to {path}"


def run_command(command):
    try:
        proc = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=20, cwd=WORKSPACE
        )
    except subprocess.TimeoutExpired:
        return "error: timed out"
    return (proc.stdout or "") + (proc.stderr or "") or "(no output)"
