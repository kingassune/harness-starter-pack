# Project 05 — my notes

## The experiment
Same feature (`filterDocs(docs, q)`), built three ways, scored by ONE shared,
objective evaluator (`compare.js`, 5 test cases):

| Variant | Roles | Score |
|---------|-------|-------|
| 1 | single agent (plan+build+self-review) | **1/5** |
| 2 | generator + independent evaluator | **3/5** |
| 3 | planner + generator + evaluator (vs contract) | **5/5** |

(Mirrors the course's reference scores 1.6 → 3.3 → 4.9.)

## What each role adds
- **Single role (1/5):** you can't catch your own blind spots. Self-review
  confirms the happy path and declares victory. It shipped 3 real bugs.
- **+ Independent evaluator (3/5):** a second set of eyes with no ego in the
  code catches obvious defects (case-sensitivity, missing-query). Big jump.
- **+ Planner / contract (5/5):** the evaluator can only check what it thinks
  to check — unless a contract enumerates the requirements. The planner turns
  "filter documents" into 5 explicit criteria, so the evaluator reviews against
  a checklist and nothing slips.

## Why this works (the two gaps)
1. **Self-review gap** — author grades own homework → fixed by an independent reviewer.
2. **Unwritten-requirements gap** — reviewer misses what nobody specified → fixed
   by a planner writing the contract first.

V3 closes both: requirements made explicit, "done" made provable.

## Takeaway
Quality isn't only about the model — it's about **how many independent
perspectives** the work passes through and **whether "done" is defined before
building**. Separate the roles and the score climbs on its own.
