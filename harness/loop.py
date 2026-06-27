"""Level 2 build — a tool-using verification agent.

Grows the Level 1 loop into an agent with HANDS and a STRUCTURED VOICE:
  - tools (read_file, run_command) let it gather concrete evidence
  - report_finding forces the verdict through a strict schema -> structured
    output, no ad-hoc JSON parsing
  - prompt caching on the system prompt + tool defs keeps repeated calls cheap

Loop stages it touches: observe (tool results) -> act (tool calls) per turn.
Plan/verify get built out at Level 3.

Run:
  python loop.py <path>      # verify a file, print the structured finding
  python loop.py --smoke     # run on the bundled vulnerable example (verify gate)
"""

import json
import os
import sys

from anthropic import Anthropic

from tools import TOOLS, dispatch

MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 2048
MAX_STEPS = 12
EXAMPLE = os.path.join(os.path.dirname(__file__), "examples", "vulnerable_login.py")

SYSTEM = (
    "You are a security verification agent. Given a target file, determine "
    "whether it contains a real, exploitable vulnerability. Use read_file and "
    "run_command to gather concrete evidence before deciding — do not guess. "
    "When confident, call report_finding exactly once to deliver your verdict. "
    "Be precise about the vulnerability type, location (file:line), and severity."
)


def require_key():
    """Fail fast and friendly if the API key is missing."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "error: ANTHROPIC_API_KEY is not set.\n"
            "  cp .env.example .env, paste your key, then:\n"
            "  export $(grep -v '^#' .env | xargs)",
            file=sys.stderr,
        )
        raise SystemExit(2)


def cached_system():
    """System prompt as a cacheable block (prompt caching)."""
    return [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}]


def cached_tools():
    """Tool defs with a cache breakpoint on the last one -> the whole tools
    array gets cached and reused across steps."""
    tools = [dict(t) for t in TOOLS]
    tools[-1] = {**tools[-1], "cache_control": {"type": "ephemeral"}}
    return tools


def run_agent(task, verbose=True):
    """The agent loop: model -> tool calls -> tool results -> repeat, until it
    reports a finding (or we hit MAX_STEPS). Returns the finding dict or None."""
    client = Anthropic()
    messages = [{"role": "user", "content": task}]
    finding = None

    for step in range(1, MAX_STEPS + 1):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=cached_system(),
            tools=cached_tools(),
            messages=messages,
        )
        if verbose:
            u = resp.usage
            print(
                f"[step {step}] stop={resp.stop_reason} "
                f"in={u.input_tokens} out={u.output_tokens} "
                f"cache_read={getattr(u, 'cache_read_input_tokens', 0)} "
                f"cache_write={getattr(u, 'cache_creation_input_tokens', 0)}"
            )

        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            if verbose:
                for block in resp.content:
                    if block.type == "text" and block.text.strip():
                        print("claude>", block.text.strip())
            break

        tool_results = []
        for block in resp.content:
            if block.type == "text" and verbose and block.text.strip():
                print("think>", block.text.strip())
            if block.type != "tool_use":
                continue
            if block.name == "report_finding":
                finding = dict(block.input)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": "recorded"}
                )
            else:
                if verbose:
                    print(f"call> {block.name}({json.dumps(block.input)})")
                result = dispatch(block.name, block.input)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                )

        messages.append({"role": "user", "content": tool_results})
        if finding is not None:
            break

    return finding


REQUIRED_KEYS = {k for k in TOOLS[-1]["input_schema"]["required"]}


def validate_finding(finding):
    """Light structured-output check: confirm every required field is present.
    Catches a malformed verdict instead of trusting it blindly."""
    if not finding:
        return False, "no finding produced"
    missing = REQUIRED_KEYS - set(finding)
    if missing:
        return False, f"missing fields: {sorted(missing)}"
    return True, "ok"


def main():
    require_key()
    smoke = "--smoke" in sys.argv[1:]
    positional = [a for a in sys.argv[1:] if not a.startswith("-")]
    target = EXAMPLE if (smoke or not positional) else positional[0]

    print(f"target: {target}\n")
    finding = run_agent(f"Verify whether the file '{target}' contains a vulnerability.")

    print("\n=== FINDING ===")
    print(json.dumps(finding, indent=2) if finding else "(no structured finding produced)")

    valid, why = validate_finding(finding)
    if smoke:
        ok = valid and finding.get("vulnerable") is True
        print(f"\n{'PASS' if ok else 'FAIL'}: schema {why}, vulnerable={finding.get('vulnerable') if finding else None}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
