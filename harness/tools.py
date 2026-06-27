"""Level 2 — tool definitions + dispatch.

Three tools with strict schemas:
  - read_file / run_command  -> give the model HANDS to gather evidence
  - report_finding           -> a STRUCTURED VOICE for the verdict; this is the
                                structured-output enforcement (we read a
                                validated dict, never hand-parse JSON).

Each schema sets additionalProperties:false and lists required fields so the
model can't return loose/ambiguous arguments.
"""
import subprocess

MAX_OUTPUT = 4000  # cap tool output so it never floods the context window

# ---- schemas ---------------------------------------------------------------

READ_FILE = {
    "name": "read_file",
    "description": (
        "Read a UTF-8 text file from disk and return its contents with line "
        "numbers. Use this to inspect source before judging it. Read-only — "
        "never modifies anything."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to read.",
            },
        },
        "required": ["path"],
        "additionalProperties": False,
    },
}

RUN_COMMAND = {
    "name": "run_command",
    "description": (
        "Run a read-only shell command (grep, cat, ls, etc.) to gather evidence "
        "about the code. Returns combined stdout/stderr, truncated. Do NOT use "
        "it to modify, delete, or move files."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute.",
            },
        },
        "required": ["command"],
        "additionalProperties": False,
    },
}

REPORT_FINDING = {
    "name": "report_finding",
    "description": (
        "Deliver the final verdict on whether the target contains a "
        "vulnerability. Call this exactly once, when investigation is complete. "
        "This ends the task."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "vulnerable": {
                "type": "boolean",
                "description": "True if a real, exploitable vulnerability is present.",
            },
            "vulnerability_type": {
                "type": "string",
                "description": "Short name, e.g. 'SQL injection'. Use 'none' if not vulnerable.",
            },
            "severity": {
                "type": "string",
                "enum": ["none", "low", "medium", "high", "critical"],
                "description": "Severity rating; 'none' if not vulnerable.",
            },
            "location": {
                "type": "string",
                "description": "Where the issue is, as file:line. Use 'n/a' if not applicable.",
            },
            "evidence": {
                "type": "string",
                "description": "The exact code or command output that proves the finding.",
            },
            "explanation": {
                "type": "string",
                "description": "Why it is (or isn't) exploitable.",
            },
            "recommendation": {
                "type": "string",
                "description": "Concrete fix, or 'none'.",
            },
        },
        "required": [
            "vulnerable",
            "vulnerability_type",
            "severity",
            "location",
            "evidence",
            "explanation",
            "recommendation",
        ],
        "additionalProperties": False,
    },
}

TOOLS = [READ_FILE, RUN_COMMAND, REPORT_FINDING]

# ---- implementations -------------------------------------------------------


def _truncate(text):
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n...[truncated {len(text) - MAX_OUTPUT} chars]"


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError) as err:
        return f"error reading {path}: {err}"
    numbered = "".join(f"{i:>4} | {line}" for i, line in enumerate(lines, 1))
    return _truncate(numbered) or "(empty file)"


def run_command(command):
    try:
        proc = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=20
        )
    except subprocess.TimeoutExpired:
        return "error: command timed out after 20s"
    out = (proc.stdout or "") + (proc.stderr or "")
    return _truncate(out) or "(no output)"


def dispatch(name, args):
    """Run a side-effecting tool by name. report_finding is terminal and is
    handled by the loop, not here."""
    if name == "read_file":
        return read_file(args["path"])
    if name == "run_command":
        return run_command(args["command"])
    return f"error: unknown tool {name!r}"
