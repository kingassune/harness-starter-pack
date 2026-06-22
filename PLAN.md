# PLAN.md

> Task planning artifact. Created at the **start** of a task; updated as
> milestones are reached. The agent updates this file **throughout** execution,
> not just at the end. Mark each milestone `[x]` the moment it is complete and
> its verification gate passes.
>
> This file is the agent's durable memory of the task. If the session resets or
> compacts, this is what lets a fresh session resume without losing progress.

---

## Task

<!-- One or two sentences. What are we actually trying to accomplish? -->

**Goal:**

**Out of scope (explicitly NOT doing):**
-

**Success looks like:**
<!-- The observable, verifiable end state. How will we KNOW it's done? -->
-

## Context the next session needs

<!-- The 3–5 facts a fresh agent must know to pick this up cold. Files,
     constraints, prior decisions, gotchas. Keep it tight. -->
-

## Milestones

> Each milestone has a **verification gate** — the concrete check that proves
> it's actually done. No gate, no checkmark. Work top to bottom.

- [ ] **M1 — <name>**
  - Steps:
  - **Gate:** <!-- e.g. `npm test passes`, `endpoint returns 200`, `file exists` -->
- [ ] **M2 — <name>**
  - Steps:
  - **Gate:**
- [ ] **M3 — <name>**
  - Steps:
  - **Gate:**
- [ ] **M-final — Verify & clean up**
  - Steps: run full verify command; remove scratch code; update `IMPLEMENT.md`.
  - **Gate:** all of the above pass + Definition of Done in `AGENTS.md` met.

## Current status

<!-- Update this line every working session. One sentence: where am I right now? -->
**Now working on:** M1
**Last verified green at:** <!-- commit hash / timestamp -->

## Replan log

<!-- Only touch this when the plan CHANGES. Append, don't overwrite. Record
     why you deviated — this is the trail that explains the final shape. -->
- _(none yet)_
