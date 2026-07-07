"""Level 4 — Scale & Orchestrate.

A long-running harness that fixes a MULTI-feature task across sessions:
  - Sandbox      : all work happens in .run/, writes gated (from htools)
  - Checkpoint   : progress persisted to .state/checkpoint.json after each feature
  - Resume       : a fresh process re-reads the checkpoint + sandbox and continues
                   the pending features — no lost progress (survives a hard kill)
  - Second agent : an ISOLATED verifier subagent (fresh context) independently
                   confirms each feature is done before it's marked complete

This mirrors Anthropic's long-running-agents pattern: state lives in a progress
file + the workspace, not in one context window.

Run:
  python scale_harness.py           # start (or resume) the task
  python scale_harness.py --status  # print checkpoint state
Env:
  HARNESS_CRASH_AFTER=N             # hard-exit after N features (to test resume)
"""
import json
import os
import subprocess
import sys

from anthropic import Anthropic

import hlog
import htools
from htools import WORKSPACE, check_permission

MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")
STATE_DIR = os.path.join(os.path.dirname(__file__), ".state")
CKPT = os.path.join(STATE_DIR, "checkpoint.json")

FEATURES = [
    {"id": "add", "test": "test_add.py", "hint": "add should return a + b"},
    {"id": "sub", "test": "test_sub.py", "hint": "sub should return a - b"},
    {"id": "mul", "test": "test_mul.py", "hint": "mul should return a * b"},
]

BUILDER_SYS = (
    "You are a coding agent fixing ONE function at a time. Use read_file, "
    "write_file (sandbox only), run_command. After each write the harness runs "
    "the target test and returns the result. Change ONLY the target function; "
    "keep the other functions intact. Call finish when the target test passes."
)
BUILDER_TOOLS = [t for t in htools.TOOLS if t["name"] in {"read_file", "write_file", "run_command", "finish"}]

VERIFIER_SYS = (
    "You are an INDEPENDENT verifier with no memory of how the code was written. "
    "Given a feature, the current file, and the test result, decide whether the "
    "feature is genuinely, correctly complete. Be skeptical."
)
VERDICT_TOOL = {
    "name": "verdict",
    "description": "Report the independent verification verdict.",
    "input_schema": {
        "type": "object",
        "properties": {
            "done": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["done", "reason"],
        "additionalProperties": False,
    },
}

MATHLIB = (
    "def add(a, b):\n    return a - b  # bug\n\n\n"
    "def sub(a, b):\n    return a + b  # bug\n\n\n"
    "def mul(a, b):\n    return a + b  # bug\n"
)
TESTS = {
    "test_add.py": "from mathlib import add\nassert add(2, 3) == 5, add(2, 3)\nassert add(0, 0) == 0\nprint('add ok')\n",
    "test_sub.py": "from mathlib import sub\nassert sub(5, 3) == 2, sub(5, 3)\nassert sub(0, 0) == 0\nprint('sub ok')\n",
    "test_mul.py": "from mathlib import mul\nassert mul(2, 3) == 6, mul(2, 3)\nassert mul(5, 0) == 0\nprint('mul ok')\n",
}

CURRENT_TEST = None


# ---- checkpoint ------------------------------------------------------------
def load_ckpt():
    return json.load(open(CKPT)) if os.path.exists(CKPT) else None


def save_ckpt(ck):
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump(ck, open(CKPT, "w"), indent=2)


def seed_workspace():
    os.makedirs(WORKSPACE, exist_ok=True)
    with open(os.path.join(WORKSPACE, "mathlib.py"), "w") as fh:
        fh.write(MATHLIB)
    for name, body in TESTS.items():
        with open(os.path.join(WORKSPACE, name), "w") as fh:
            fh.write(body)


# ---- verify ----------------------------------------------------------------
def run_test(test):
    proc = subprocess.run(f"python {test}", shell=True, capture_output=True, text=True, cwd=WORKSPACE)
    out = (proc.stdout or "") + (proc.stderr or "")
    hlog.log("verify", test=test, exit=proc.returncode, output=out)
    return proc.returncode == 0, ("PASS: " + hlog.summarize(out)) if proc.returncode == 0 else ("FAIL: " + hlog.summarize(out))


def dispatch(name, args):
    allowed, reason = check_permission(name, args)
    hlog.log("permission", tool=name, allowed=allowed, reason=reason)
    if not allowed:
        return f"DENIED: {reason}"
    if name == "read_file":
        return hlog.summarize(htools.read_file(args["path"]), 400)
    if name == "write_file":
        msg = htools.write_file(args["path"], args["content"])
        _, summary = run_test(CURRENT_TEST)
        return f"{msg}\nverify -> {summary}"
    if name == "run_command":
        return hlog.summarize(htools.run_command(args["command"]), 400)
    return f"error: unknown tool {name}"


# ---- builder (per feature) -------------------------------------------------
def build_feature(client, feature):
    global CURRENT_TEST
    CURRENT_TEST = feature["test"]
    messages = [{"role": "user", "content": f"Fix the `{feature['id']}` function in mathlib.py so `python {feature['test']}` passes. {feature['hint']}."}]
    for _ in range(8):
        resp = client.messages.create(model=MODEL, max_tokens=1200, system=BUILDER_SYS, tools=BUILDER_TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            break
        results = []
        for b in resp.content:
            if b.type != "tool_use":
                continue
            if b.name == "finish":
                passed, summary = run_test(feature["test"])
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": ("accepted " + summary) if passed else ("rejected " + summary)})
                if passed:
                    messages.append({"role": "user", "content": results})
                    return True
            else:
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": dispatch(b.name, b.input)})
        messages.append({"role": "user", "content": results})
    return run_test(feature["test"])[0]


# ---- verifier subagent (isolated context) ----------------------------------
def verify_feature(client, feature):
    content = htools.read_file("mathlib.py")
    _, summary = run_test(feature["test"])
    resp = client.messages.create(
        model=MODEL, max_tokens=300, system=VERIFIER_SYS,
        tools=[VERDICT_TOOL], tool_choice={"type": "tool", "name": "verdict"},
        messages=[{"role": "user", "content": f"Feature '{feature['id']}' ({feature['hint']}).\nTest result: {summary}\n\nmathlib.py:\n{content}\n\nIs this feature genuinely complete?"}],
    )
    for b in resp.content:
        if b.type == "tool_use":
            return b.input
    return {"done": False, "reason": "no verdict"}


# ---- orchestration ---------------------------------------------------------
def run():
    ck = load_ckpt()
    if ck is None:
        seed_workspace()
        ck = {"features": [{"id": f["id"], "status": "pending"} for f in FEATURES]}
        save_ckpt(ck)
        hlog.log("start", mode="fresh")
        print("fresh start — 3 features pending")
    else:
        done = [f["id"] for f in ck["features"] if f["status"] == "done"]
        hlog.log("start", mode="resume", done=done)
        print(f"RESUMING — already done: {done or 'none'}")

    client = Anthropic()
    crash_after = int(os.environ.get("HARNESS_CRASH_AFTER", "0"))
    built_this_run = 0

    for i, feature in enumerate(FEATURES):
        if ck["features"][i]["status"] == "done":
            print(f"  skip {feature['id']} (done)")
            continue
        print(f"  building {feature['id']} …")
        ok = build_feature(client, feature)
        verdict = verify_feature(client, feature)  # isolated 2nd agent
        if ok and verdict.get("done"):
            ck["features"][i]["status"] = "done"
            save_ckpt(ck)  # checkpoint after each feature
            built_this_run += 1
            print(f"  {feature['id']} DONE + verifier agrees ({verdict.get('reason', '')[:60]})")
        else:
            ck["features"][i]["status"] = "failed"
            save_ckpt(ck)
            print(f"  {feature['id']} FAILED (builder={ok}, verifier={verdict})")

        if crash_after and built_this_run >= crash_after:
            print(f"  !! injected crash after {built_this_run} feature(s) — process dies")
            os._exit(137)

    remaining = [f["id"] for f in ck["features"] if f["status"] != "done"]
    if not remaining:
        print("ALL FEATURES COMPLETE ✅")
        return 0
    print(f"stopped with pending: {remaining}")
    return 1


def status():
    ck = load_ckpt()
    print(json.dumps(ck, indent=2) if ck else "(no checkpoint)")
    return 0


def main():
    hlog.start()
    if "--status" in sys.argv[1:]:
        return status()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
