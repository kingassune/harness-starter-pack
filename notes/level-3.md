# Level 3 — Build Your First Harness (notes + exit)

## READ
- Worked the *Learn Harness Engineering* course — all 6 projects in `projects/`.
- Read the smolagents core: the loop lives in `MultiStepAgent._run_stream()`
  (`src/smolagents/agents.py`), with `_step_stream()` as the per-step think-act.
  Planning is gated by `planning_interval` — the "plan" phase I added below.
- Read *Skill Issue* (HumanLayer): weak results are usually harness problems,
  not model problems; a good harness "floats on any model."

## BUILD — the "Hello, Harness" milestone
Files: `harness/hello_harness.py`, `harness/htools.py`, `harness/hlog.py`.
Demo task: fix a seeded bug in `.run/mathlib.py` until `test_mathlib.py` passes.

| Milestone item | How it's done | Evidence |
|----------------|---------------|----------|
| observe → plan → act → verify | read_file (observe) → update_plan (plan) → write_file (act) → run_verify after each write | clean run: 4 steps to a verified PASS |
| writes + updates PLAN.md each turn | `update_plan` tool writes `.run/PLAN.md` | 3 milestones, all checked off at the end |
| destructive tools gated | `check_permission` gates write_file (sandbox only) + run_command (no rm/>/etc.) | `--selfcheck` PASS 4/4; a real out-of-sandbox write was DENIED mid-run |
| test after every change, summaries only | write_file runs the test, returns `verify -> PASS/FAIL` one-liner | full test output only in the log |
| full output to a file | `hlog` writes JSON lines to `harness/logs/harness-run.log` | 42-line log; context sees summaries |
| (bonus) verified finish | `finish` is rejected unless the test actually passes | prevents false "done" |

## A bug the harness process caught
The permission gate's first version flagged `grep -n add mathlib.py` as
destructive — `"dd "` matched inside `"a`**`dd`**` mathlib"`. The `--selfcheck`
(prove-the-gate-isn't-vacuous, from P04) caught it; fixed by matching whole
tokens, not substrings. Lesson reinforced: an assertion you've never seen fail
isn't trustworthy.

## Exit
> A single-agent harness completes a task on its own. ✅
`python harness/hello_harness.py` autonomously fixes the bug and finishes with a
verified test pass — observe→plan→act→verify, gated, logged, PLAN-tracked.
