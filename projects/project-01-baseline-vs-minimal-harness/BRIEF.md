# Project 01 — Prompt-Only vs. Rules-First

**Harness lesson:** pre-placed organizational artifacts (rules, checklists,
init scripts) measurably improve agent task completion versus a raw prompt.

## Background
Teaches the practical difference between an unstructured prompt and structured
harness guidance. Same coding task, run twice under different conditions. The
upstream vehicle is an Electron knowledge-base app — but the measurable variable
is the *harness*, not the app.

## Objective
Demonstrate that the same task completes faster / more completely when the agent
is given `AGENTS.md` + `init.sh` + `feature_list.json` versus a prompt alone.

## Step-by-step tasks
1. **Run One (Baseline):** give the agent only `starter/task-prompt.md`. No extra structure.
2. **Measure:** record time and completion depth.
3. **Run Two (With Harness):** give the same task plus `AGENTS.md`, `init.sh`, `feature_list.json`.
4. **Measure:** record time and completion depth again.
5. **Compare:** evaluate the difference in quality and duration.

## Starter (this folder's `starter/`)
- `task-prompt.md` — the raw-prompt scenario (provided).
- You create the harness artifacts for Run Two: `AGENTS.md`, `init.sh`,
  `feature_list.json`, and a `claude-progress.md` capturing evidence.

## Deliverable
Two runs of the same task, plus a short comparison. Evidence lives in
`feature_list.json` (expected artifacts per feature) and `claude-progress.md`.

## Success criteria
1. Both runs produce a functional result.
2. There is a measurable time/quality difference.
3. The harness-guided run is more consistent / more complete.
4. The comparison shows the practical value of structure over prompt-only.

---
*Record your two runs + comparison in `NOTES.md`.*
