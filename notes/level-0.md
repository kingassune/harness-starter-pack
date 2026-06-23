# Level 0 — Orientation (my answers)

## What is a harness? (my definition)
A harness is a framework around a model, giving it the ability to do things
that the model can't yet accomplish. The harness gives it abilities that the
model will soon have. Instead of going back and forth with the complexities of
things it just can't do.

## The loop
Observe → Plan → Act → Verify

## The 5 primitives (from memory)
1. Filesystem
2. Code Execution
3. Memory
4. Sandbox
5. Context Management

> Note: the repo's `HARNESS_CHECKLIST.md` expands these into ~12 named
> primitives (agent loop, planning, context, tools, permissions, memory,
> orchestration, verification, observability, sandbox, HITL, feedback hygiene).
> Revisit at Level 2.

## BUILD decisions
- **Task my first harness will tackle:** something simple — verify a
  vulnerability. (To be sharpened into one specific, verifiable check by Level 3.)
- **Stack:** Claude (Claude Agent SDK) — already most used to it.

## Exit criterion
> You can explain what a harness is and why every component is temporary.

Met: a harness wraps a model with abilities it doesn't have *yet*; each
component is a temporary crutch that gets removed as the model gains those
abilities on its own.
