"""Level 3 — the "Hello, Harness" milestone.

A single-agent harness that autonomously completes a task by running the full
loop: observe -> plan -> act -> verify. It:
  - writes/updates PLAN.md every turn (the plan)
  - gates destructive tools behind a permission check (write/run_command)
  - runs the test after every change; feeds only a SUMMARY line back to context
  - logs full output to a file (harness/logs/harness-run.log)
  - verifies the test actually passes before accepting "finish"

Demo task: the sandbox ships a broken mathlib.py; the harness must fix it until
`python test_mathlib.py` passes.

Run:
  python hello_harness.py            # full autonomous run (needs ANTHROPIC_API_KEY)
  python hello_harness.py --selfcheck  # prove the permission gate (no API key)
"""
import json
import os
import subprocess
import sys

from anthropic import Anthropic

import hlog
import htools
from htools import WORKSPACE, TOOLS, check_permission

MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")
MAX_STEPS = 12
PLAN_FILE = os.path.join(WORKSPACE, "PLAN.md")
VERIFY_CMD = "python test_mathlib.py"

SYSTEM = (
    "You are a coding harness agent. Complete the task using the loop: "
    "(1) call update_plan with milestones, (2) inspect with read_file/run_command, "
    "(3) fix code with write_file. After every write_file the harness runs the test "
    "and returns the result — use it. When the test passes, call finish. "
    "Only edit files inside the sandbox."
)

BROKEN_MATHLIB = "def add(a, b):\n    return a - b  # bug: should be a + b\n"
TEST_MATHLIB = (
    "from mathlib import add\n\n"
    "def main():\n"
    "    cases = [((2, 3), 5), ((0, 0), 0), ((-1, 1), 0), ((10, 5), 15)]\n"
    "    for (a, b), expected in cases:\n"
    "        got = add(a, b)\n"
    "        assert got == expected, f'add({a},{b})={got}, expected {expected}'\n"
    "    print('all tests passed')\n\n"
    "if __name__ == '__main__':\n"
    "    main()\n"
)


def seed_workspace():
    os.makedirs(WORKSPACE, exist_ok=True)
    with open(os.path.join(WORKSPACE, "mathlib.py"), "w") as fh:
        fh.write(BROKEN_MATHLIB)
    with open(os.path.join(WORKSPACE, "test_mathlib.py"), "w") as fh:
        fh.write(TEST_MATHLIB)


def run_verify():
    """VERIFY stage: run the test, log full output, return (passed, summary)."""
    proc = subprocess.run(
        VERIFY_CMD, shell=True, capture_output=True, text=True, cwd=WORKSPACE
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    hlog.log("verify", cmd=VERIFY_CMD, exit=proc.returncode, output=out)
    passed = proc.returncode == 0
    return passed, ("PASS: " + hlog.summarize(out)) if passed else ("FAIL: " + hlog.summarize(out))


def write_plan(milestones):
    lines = ["# PLAN.md", ""]
    for m in milestones:
        lines.append(f"- [{'x' if m.get('done') else ' '}] {m.get('step', '')}")
    with open(PLAN_FILE, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    hlog.log("plan.update", milestones=milestones)


def dispatch(name, args):
    """Run a tool through the permission gate. Returns (text_for_context)."""
    allowed, reason = check_permission(name, args)
    hlog.log("permission", tool=name, allowed=allowed, reason=reason, args=args)
    if not allowed:
        return f"DENIED: {reason}"

    if name == "update_plan":
        write_plan(args["milestones"])
        return f"plan updated ({len(args['milestones'])} milestones)"
    if name == "read_file":
        content = htools.read_file(args["path"])
        hlog.log("read_file", path=args["path"], content=content)
        return hlog.summarize(content, 400)
    if name == "write_file":
        msg = htools.write_file(args["path"], args["content"])
        hlog.log("write_file", path=args["path"], content=args["content"])
        # test-after-every-change: run verify and hand back only the summary
        passed, summary = run_verify()
        return f"{msg}\nverify -> {summary}"
    if name == "run_command":
        out = htools.run_command(args["command"])
        hlog.log("run_command", command=args["command"], output=out)
        return hlog.summarize(out, 400)
    return f"error: unknown tool {name}"


def run(client):
    seed_workspace()
    hlog.log("startup", task="fix mathlib.add so the test passes", workspace=WORKSPACE)
    messages = [{"role": "user", "content": "Fix mathlib.py so `python test_mathlib.py` passes."}]

    for step in range(1, MAX_STEPS + 1):
        resp = client.messages.create(
            model=MODEL, max_tokens=1500, system=SYSTEM, tools=TOOLS, messages=messages
        )
        hlog.log("model", step=step, stop=resp.stop_reason,
                 content=[b.model_dump() for b in resp.content])
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            break

        results = []
        finished = False
        for block in resp.content:
            if block.type != "tool_use":
                continue
            if block.name == "finish":
                passed, summary = run_verify()  # verified-finish gate
                if passed:
                    finished = True
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": "accepted: " + summary})
                else:
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": "REJECTED, test still failing: " + summary})
            else:
                out = dispatch(block.name, block.input)
                print(f"[step {step}] {block.name} -> {out.splitlines()[0] if out else ''}")
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})

        messages.append({"role": "user", "content": results})
        if finished:
            passed, summary = run_verify()
            print(f"\nDONE — {summary}")
            return 0 if passed else 1

    print("stopped without a verified finish")
    return 1


def selfcheck():
    """Prove the permission gate is not vacuous (no API key needed)."""
    cases = [
        ("write_file", {"path": os.path.join(WORKSPACE, "ok.py")}, True),
        ("write_file", {"path": "/etc/passwd"}, False),
        ("run_command", {"command": "grep -n add mathlib.py"}, True),
        ("run_command", {"command": "rm -rf /"}, False),
    ]
    ok = True
    for name, args, expected in cases:
        allowed, reason = check_permission(name, args)
        mark = "PASS" if allowed == expected else "FAIL"
        if allowed != expected:
            ok = False
        print(f"{mark}  {name}({list(args.values())[0]}) -> allowed={allowed} ({reason})")
    print("selfcheck:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    hlog.start()
    if "--selfcheck" in sys.argv[1:]:
        return selfcheck()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY not set (or use --selfcheck)", file=sys.stderr)
        return 2
    return run(Anthropic())


if __name__ == "__main__":
    raise SystemExit(main())
