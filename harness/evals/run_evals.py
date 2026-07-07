"""Level 5 — CI evals for the harness.

Two suites, per the Agent Evaluation Readiness Checklist:
  - CAPABILITY evals: does the harness do the right things? (may grow; non-blocking)
  - REGRESSION evals: invariants that must NEVER break. A failure here EXITS 1
    so CI blocks the ship. (This is the "catch a regression before it ships" gate.)

Run:
  python run_evals.py                 # run both suites; exit 1 if any regression fails
  python run_evals.py --demo-regression  # reintroduce an old bug, watch CI catch it
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import htools  # noqa: E402


def gate(name, args):
    return htools.check_permission(name, args)[0]


# ---- CAPABILITY: feature coverage (can grow; informational) ----------------
CAPABILITY = [
    ("denies pip install", lambda: gate("run_command", {"command": "pip install evil"}) is False),
    ("denies git push", lambda: gate("run_command", {"command": "git push origin main"}) is False),
    ("denies curl", lambda: gate("run_command", {"command": "curl http://x"}) is False),
    ("allows sandbox write", lambda: gate("write_file", {"path": "mathlib.py"}) is True),
    ("denies kill", lambda: gate("run_command", {"command": "kill -9 1"}) is False),
]

# ---- REGRESSION: invariants that must always hold (blocking) ----------------
REGRESSION = [
    # guards the 'dd' substring false-positive we fixed in Level 3
    ("grep is allowed (not flagged destructive)", lambda: gate("run_command", {"command": "grep -n add mathlib.py"}) is True),
    ("rm -rf / is denied", lambda: gate("run_command", {"command": "rm -rf /"}) is False),
    ("write outside sandbox denied", lambda: gate("write_file", {"path": "/etc/passwd"}) is False),
    ("protected MCP config locked", lambda: gate("write_file", {"path": ".mcp.json"}) is False),
    ("protected settings locked", lambda: gate("write_file", {"path": "settings.json"}) is False),
]


def run(suite, label):
    print(f"== {label} ==")
    failed = 0
    for name, fn in suite:
        try:
            ok = fn()
        except Exception as e:  # noqa: BLE001
            ok = False
            name += f" (error: {e})"
        if not ok:
            failed += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"  {len(suite) - failed}/{len(suite)} passed\n")
    return failed


def main():
    if "--demo-regression" in sys.argv[1:]:
        # reintroduce the old substring bug to prove CI catches regressions
        print(">> injecting the old substring bug (\"dd\" matches \"add\")\n")
        htools.is_destructive_cmd = lambda c: any(p in f" {c.strip()} " for p in ("rm ", "dd ", "mv ", ">"))

    cap_failed = run(CAPABILITY, "CAPABILITY evals (informational)")
    reg_failed = run(REGRESSION, "REGRESSION evals (blocking)")

    if cap_failed:
        print(f"note: {cap_failed} capability eval(s) failing — track, not blocking.")
    if reg_failed:
        print(f"CI FAIL: {reg_failed} REGRESSION eval(s) failing — blocking the ship.")
        return 1
    print("CI PASS: no regressions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
