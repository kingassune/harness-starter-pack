# Project 06 — Complete Harness (Capstone)

**Harness lesson:** assemble all five mechanisms into one observable system, then
prove with a benchmark + ablation which parts actually move the needle.

## Background
Synthesizes Projects 01–05 across a full product slice: document import,
indexing, Q&A with citations, runtime observability, and repo state management.

## Objective
"Assemble everything learned in the first five projects, run a full benchmark,
then do a cleanup pass to verify quality is maintainable."

## Step-by-step tasks
1. **Baseline assessment** — run the weak-harness starter; document baseline.
2. **Full harness integration** — apply all five prior mechanisms (readable
   workspace, multi-session continuity, feedback control, self-verification,
   role separation).
3. **Benchmark execution** — run `benchmark.sh` against weak vs. strong harness.
4. **Cleanup verification** — run `cleanup-scanner.sh` for maintainable state.
5. **Ablation study** — remove components one at a time to see which matter.

## Starter / what you create
Harness surface files: `AGENTS.md`, `CLAUDE.md`, `feature_list.json`, `init.sh`,
`session-handoff.md`, `clean-state-checklist.md`; plus `scripts/benchmark.sh` and
`scripts/cleanup-scanner.sh`.

## Success criteria
- Quantifiable improvement between baseline and optimized harness.
- Reproducible benchmark results with evidence.
- Clean-state verification passes.
- Ablation shows 2–3 components with measurable impact.
- Codebase is maintainable and handoff-ready.

---
*This is the Level 3 "Hello, Harness" milestone in disguise — your own
`harness/` agent is a fine substrate to benchmark. Record results in `NOTES.md`.*
