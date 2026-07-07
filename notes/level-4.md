# Level 4 — Scale & Orchestrate (notes + exit)

## READ
- *Choosing the Right Multi-Agent Architecture* (LangChain) + Anthropic's
  multi-agent research system: multi-agent beat single-agent ~90% on their
  evals, BUT only add agents when isolation/parallelism earns it — not when all
  agents need the same context.
- *Effective Harnesses for Long-Running Agents*: an initializer writes
  feature_list + init.sh; a coding agent is woken repeatedly, does ONE feature,
  tests, leaves a progress note, commits. State from progress file + git, not a
  single context window. (We'd already built this shape in Projects 3–6.)
- Protocol map: MCP (agent↔tools), A2A (agent↔agent), AG-UI (agent↔human) —
  complementary layers, like TCP/HTTP/HTML.

## BUILD — `harness/scale_harness.py`
A long-running harness that fixes a 3-feature task (add/sub/mul, each seeded
buggy with its own test).

| BUILD item | How | Evidence |
|-----------|-----|----------|
| Sandbox for code execution | all work in `.run/`, writes gated to the sandbox, destructive commands denied (from `htools`) | reused L3 gate |
| Second specialized agent (only if it earns it) | an **isolated verifier subagent** with a fresh context independently confirms each feature before it's marked done | "verifier agrees" logged per feature |
| Checkpoint-resume | progress persisted to `.state/checkpoint.json` after each feature; a fresh process re-reads it + the sandbox and continues | see the kill/resume run below |

## The kill/resume proof (the exit)
1. Fresh run: built `add`, verifier agreed, **checkpointed**.
2. **`kill -9` mid-task** while it was building `sub`. Checkpoint = `add:done,
   sub:pending, mul:pending`; the `add` fix persisted in `.run/mathlib.py`.
3. Fresh process: `RESUMING — already done: ['add']` → skipped `add`, built
   `sub` + `mul` (verifier agreed each) → **ALL FEATURES COMPLETE**.

Zero progress lost across a hard process death.

## Why the verifier "earns it"
It has a **fresh context** — no memory of how the code was written — so it can't
inherit the builder's blind spots (P05), and its reasoning never pollutes the
builder's context window (isolation). That's the bar from the reading: add an
agent for isolation/parallelism value, not for its own sake.

## Exit
> The harness handles a task bigger than one context window without losing
> progress. ✅  The multi-feature task completed across TWO processes (a kill +
> restart) with no lost work — state carried by the checkpoint + sandbox.
